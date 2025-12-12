# solrad.py
"""
NOAA SOLRAD radiation data downloader.

This module downloads SOLRAD data from NOAA (GML).
Fully aligned with the official README format used by pvlib.
Behavior:
    - Builds daily URLs for both realtime and archive directories
    - Parses metadata (latitude, longitude, elevation, timezone)
    - Parses SOLRAD fixed-width data rows
    - Performs QC filtering
    - Generates UTC_Time, Local_Time, UTC_Offset
    - Output columns follow: Local_Time, UTC_Time, UTC_Offset, <data fields>, <std fields>
"""

import time
from datetime import datetime, timedelta, timezone
from typing import List, Optional
import pandas as pd

from necessary_main import (
    http_get_with_retry,
    init_date,
    url_contact,
    attach_local_and_offset,
)

# =====================================================
# Field index mapping (strictly follows NOAA README)
# =====================================================

FIELD_MAP = {
    "dw_psp":   (8, 9),   # global PSP
    "direct":   (10, 11), # direct beam
    "diffuse":  (12, 13), # diffuse
    "uvb":      (14, 15), # UV-B
    "uvb_temp": (16, 17), # UV-B temperature
}

STD_FIELDS = {
    "std_dw_psp": 18,
    "std_direct": 19,
    "std_diffuse": 20,
    "std_uvb": 21,
}


# =====================================================
# Metadata parsing
# =====================================================

def _parse_meta_line(line: str) -> dict:
    """
    Parse the 2nd line of SOLRAD .dat file:
        lat lon elev tz version <optional>

    Example:
        40.05 -88.37 213 0 version 1
    """
    parts = line.split()
    if len(parts) < 4:
        raise ValueError(f"Invalid metadata line: {line}")

    meta = {
        "lat": float(parts[0]),
        "lon": float(parts[1]),
        "elev": float(parts[2]),
        "tz_hours": int(parts[3]),
    }

    # Optional version support
    for i, p in enumerate(parts):
        if p.lower().startswith("version") and i + 1 < len(parts):
            meta["version"] = parts[i + 1]

    return meta


# =====================================================
# URL builder
# =====================================================

def _build_solrad_urls(station: str, start, end) -> List[str]:
    """
    Build a list of candidate URLs for SOLRAD dataset.
    It tries both:
        - realtime/<station>/<year>/<file>
        - archive/<station>/<year>/<file>
    """
    base = "https://gml.noaa.gov/aftp/data/radiation/solrad"

    today_utc = datetime.now(timezone.utc).date()
    urls = []

    total_days = (end - start).days + 1

    for i in range(total_days):
        d = start + timedelta(days=i)
        yy = d.strftime("%y")
        year = str(d.year)
        doy = f"{d.timetuple().tm_yday:03d}"
        fname = f"{station}{yy}{doy}.dat"

        # Realtime (last ~48 hours)
        if d >= today_utc - timedelta(days=2):
            u = url_contact(base, "realtime")
            u = url_contact(u, station)
            u = url_contact(u, year)
            u = url_contact(u, fname)
            urls.append(u)

        # Archive
        if d <= today_utc - timedelta(days=1):
            u = url_contact(base, station)
            u = url_contact(u, year)
            u = url_contact(u, fname)
            urls.append(u)

    return urls


# =====================================================
# Data block parsing
# =====================================================

def _parse_data_block(lines: List[str], tz_hours: int) -> pd.DataFrame:
    """
    Parse SOLRAD data rows.
    NOAA SOLRAD file format (22 fields):
        c0  = year
        c1  = Julian day
        c2  = month
        c3  = day
        c4  = hour
        c5  = minute
        c6  = second
        c7+ = data fields
    Time information is already in UTC.
    """
    if not lines:
        return pd.DataFrame()

    rows = []
    for ln in lines:
        parts = ln.split()
        if len(parts) < 22:
            continue
        rows.append(parts[:22])

    if not rows:
        return pd.DataFrame()

    df = pd.DataFrame(rows, columns=[f"c{i}" for i in range(22)])

    # Convert all fields to numeric
    for c in df.columns:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    # -------------------------------------------------
    # Build UTC datetime (SOLRAD timestamps are UTC)
    # -------------------------------------------------
    utc_dt = pd.to_datetime(
        df["c0"].astype(int).astype(str) + "-" +
        df["c2"].astype(int).astype(str) + "-" +
        df["c3"].astype(int).astype(str) + " " +
        df["c4"].astype(int).astype(str) + ":" +
        df["c5"].astype(int).astype(str),
        errors="coerce"
    )

    # Local time = UTC + station TZ
    local_dt = utc_dt + pd.Timedelta(hours=tz_hours)

    df["UTC_Time"] = utc_dt.dt.strftime("%Y/%m/%d %H:%M:%S")

    # -------------------------------------------------
    # Apply QC and map values
    # -------------------------------------------------
    for key, (val_i, qc_i) in FIELD_MAP.items():
        raw = df[f"c{val_i}"]
        qc = df[f"c{qc_i}"]
        df[key] = raw.where((qc == 0) & (raw > -9000), -999.9)

    # Standard deviation fields
    for key, idx in STD_FIELDS.items():
        df[key] = df[f"c{idx}"].astype(float)

    # Insert Local_Time and UTC_Offset via utility function
    df = attach_local_and_offset(
        df,
        local_ts=local_dt.dt.tz_localize(f"Etc/GMT{(-tz_hours):+d}"),
        local_col="Local_Time",
        offset_col="UTC_Offset"
    )

    df = df.sort_values("UTC_Time")
    return df[
        ["Local_Time", "UTC_Time", "UTC_Offset"]
        + list(FIELD_MAP.keys())
        + list(STD_FIELDS.keys())
    ]


# =====================================================
# Public unified API
# =====================================================

def download_solrad(
    site: str,
    start: str,
    end: str,
    output_csv: Optional[str] = None,
):
    """
    Public high-level SOLRAD download function (replaces fetch_solrad_data).

    Steps:
        - Convert date strings
        - Build all candidate URLs
        - Download each daily file
        - Parse metadata and data block
        - Merge, drop duplicates, sort
        - Save CSV

    Parameters
    ----------
    site : str
        SOLRAD station ID (lowercase recommended).
    start : str
        Start date (YYYY-MM-DD or YYYYMMDD).
    end : str
        End date (YYYY-MM-DD or YYYYMMDD).
    output_csv : str, optional
        Output CSV path. If None, auto-named.

    Notes
    -----
    All internal logic is unchanged from the original version.
    Only the function name and comments were updated.
    """

    start_d = init_date(start)
    end_d   = init_date(end)

    station = site.lower().strip()

    if not output_csv:
        output_csv = f"solrad_{station}_{start_d}_{end_d}.csv"

    urls = _build_solrad_urls(station, start_d, end_d)
    frames = []

    for url in urls:
        try:
            text = http_get_with_retry(url)
            lines = [ln.strip() for ln in text.splitlines() if ln.strip()]

            if len(lines) < 3:
                print(f"[warn] Too few lines: {url}")
                continue

            # Metadata on the second line
            meta = _parse_meta_line(lines[1])
            tz_hours = meta["tz_hours"]

            df = _parse_data_block(lines[2:], tz_hours)
            if not df.empty:
                frames.append(df)
                print(f"[ok] {url} | TZ={tz_hours} | {len(df)} rows")

        except Exception as e:
            print(f"[err] {url}: {e}")

        time.sleep(0.4)

    if not frames:
        print("[DONE] No data available")
        return

    df_all = (
        pd.concat(frames, ignore_index=True)
        .drop_duplicates(subset=["UTC_Time"])
        .sort_values("UTC_Time")
    )

    df_all.to_csv(output_csv, index=False, encoding="utf-8")
    print(f"[DONE] Saved to {output_csv} | rows={len(df_all)}")
