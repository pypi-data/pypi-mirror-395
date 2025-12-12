"""
SRML (Solar Radiation Monitoring Laboratory) data downloader.
Unified API version — consistent with MIDC downloader style.

Public API:
    download_srml(site, begin, end, csv_path)

Internal logic:
    _parse_srml_text_to_df()
    _download_one_month_df()
"""

import os
import re
from datetime import datetime
from typing import Dict, List

import pandas as pd
import numpy as np

from necessary_main import (
    http_get_with_retry,
    ensure_dir,
    url_contact,
    tz_localize_safely,
    attach_local_and_offset,
    clip_by_local_date,
)

# ======================================================
# SRML Station Config
# ======================================================

# user inputs "BUO" -> directory=BUO, file prefix="BU"
STATION_MAP: Dict[str, str] = {
    "BUO": "BU",
    "CYW": "CY",
    "EUO": "EU",
    "HEO": "HE",
    "MDO": "MD",
    "PDO": "PD",
    "PSO": "PS",
    "SAO": "SA",
    "SIO": "SI",
    "STW": "ST",
}

# all SRML sites share same timezone
SRML_TZ = "America/Los_Angeles"

# variable code → name
VARIABLE_MAP = {
    "100": "GHI",
    "201": "DNI",
    "300": "DHI",
    "930": "TEMP",
    "933": "RH",
    "931": "DEW",
    "937": "TCELL",
    "920": "WDIR",
    "921": "WSPD",
}

# SRML file type priority
FILETYPE_PRIORITY = ["PO", "RO", "PF", "RF", "PQ", "RQ", "PH", "RH"]

BASE_URL = "http://solardata.uoregon.edu/download/archive"


# ======================================================
# Parser
# ======================================================

def _parse_srml_text_to_df(text: str) -> pd.DataFrame:
    """
    Parse SRML ASCII dataset.
    """
    lines = [ln for ln in text.splitlines() if ln.strip()]
    if not lines:
        raise ValueError("Empty SRML text")

    header = re.split(r"\s+", lines[0].strip())
    year = int(header[1])
    pairs = header[2:]
    if len(pairs) % 2 != 0:
        pairs = pairs[:-1]

    codes = pairs[0::2]
    var_names = []
    from collections import defaultdict
    counter = defaultdict(int)

    for code in codes:
        base = code[:3]
        if base in VARIABLE_MAP:
            name = VARIABLE_MAP[base]
            idx = counter[base]
            counter[base] += 1
            var_names.append(f"{name}_{idx}")
        else:
            var_names.append(f"VAR{code}")

    doy_list, raw_list = [], []
    data = {v: [] for v in var_names}

    for ln in lines[1:]:
        parts = re.split(r"\s+", ln.strip())
        if len(parts) < 2 + 2*len(var_names):
            continue

        doy = int(float(parts[0]))
        hhmm = int(float(parts[1]))
        doy_list.append(doy)
        raw_list.append(hhmm)

        for j, name in enumerate(var_names):
            v = parts[2+2*j]
            f = parts[3+2*j]
            try:
                val = float(v)
            except:
                val = np.nan

            try:
                flag = int(float(f))
            except:
                flag = 0

            if flag == 99:
                val = -999.99

            data[name].append(val)

    # time adjustment
    if len(raw_list) > 1:
        interval = raw_list[1] - raw_list[0]
    else:
        interval = 100

    adj_times = []
    for t in raw_list:
        t_adj = t - interval
        if interval != 100 and (t_adj % 100) > 60:
            t_adj -= 40
        adj_times.append(t_adj)

    timestamps = [
        f"{year}-{doy:03d}-{hhmm:04d}"
        for doy, hhmm in zip(doy_list, adj_times)
    ]

    dt = pd.to_datetime(timestamps, format="%Y-%j-%H%M")
    df = pd.DataFrame(data, index=dt)
    df.index.name = "datetime"
    return df


# ======================================================
# Download a single month
# ======================================================

def _download_one_month_df(site_dir: str, prefix: str, year: int, month: int):
    """
    Try to download one month of SRML data.
    """
    yy = f"{year % 100:02d}"
    mm = f"{month:02d}"

    for ft in FILETYPE_PRIORITY:
        fname = f"{prefix}{ft}{yy}{mm}.txt"

        url = url_contact(
            url_contact(
                url_contact(BASE_URL, site_dir),
                f"{site_dir}_{year}"
            ),
            fname
        )

        print(f"[SRML] Trying: {fname}")

        try:
            text = http_get_with_retry(url)
        except Exception:
            continue

        try:
            df = _parse_srml_text_to_df(text)
            print(f"[SRML] Success → {fname}")
            return df
        except Exception:
            continue

    print(f"[SRML] No valid file for {site_dir} {year}-{month:02d}")
    return None


# ======================================================
# Public unified API
# ======================================================

def download_srml(site: str, begin: str, end: str, csv_path: str):
    """
    Unified SRML download interface.

    Parameters
    ----------
    site : str
        SRML site code, e.g. "BUO" (case-insensitive).
    begin : str
        Start date YYYYMMDD.
    end : str
        End date YYYYMMDD.
    csv_path : str
        Output CSV path (created if needed).
    """
    site = site.upper().strip()
    if site not in STATION_MAP:
        raise ValueError(f"Unknown SRML site: {site}")

    prefix = STATION_MAP[site]
    tz_name = SRML_TZ

    begin_dt = datetime.strptime(begin, "%Y%m%d")
    end_dt = datetime.strptime(end, "%Y%m%d")

    # month list
    months = []
    cur = datetime(begin_dt.year, begin_dt.month, 1)
    last = datetime(end_dt.year, end_dt.month, 1)

    while cur <= last:
        months.append((cur.year, cur.month))
        cur = datetime(cur.year + (cur.month==12), (cur.month % 12) + 1, 1)

    dfs = []
    for y, m in months:
        df_m = _download_one_month_df(site, prefix, y, m)
        if df_m is not None:
            dfs.append(df_m)

    if not dfs:
        print("[SRML] No data available.")
        return

    df = pd.concat(dfs).sort_index()

    # localize
    naive = df.index.to_series()
    local_ts = tz_localize_safely(naive, tz_name)

    # clip
    mask, clipped = clip_by_local_date(local_ts, begin, end, tz_name)
    df = df.loc[mask].reset_index(drop=True)
    clipped = clipped.reset_index(drop=True)

    # add Local_Time + UTC_Offset
    df = attach_local_and_offset(df, clipped)

    # add UTC column
    utc_ts = clipped.dt.tz_convert("UTC")
    df.insert(0, "UTC_Time", utc_ts.dt.strftime("%Y/%m/%d %H:%M:00"))

    # save
    ensure_dir(os.path.dirname(csv_path))
    df.to_csv(csv_path, index=False, encoding="utf-8")
    print(f"[SRML] Saved → {csv_path}")
