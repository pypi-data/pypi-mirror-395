import os
import pandas as pd
import requests
from io import StringIO
from datetime import timezone, timedelta
import urllib3

from .necessary_main import (
    init_str_date,
    url_contact,
    ensure_dir,
    fmt_offset,
)

# Disable TLS warnings (some SAURAN nodes have invalid certificates)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def _parse_tmstamp_series(raw: pd.Series) -> pd.Series:
    """
    Robust timestamp parser for SAURAN 'TmStamp' formats.
    Supports multiple common patterns:
        - YYYY/MM/DD HH:MM(:SS)
        - DD/MM/YYYY HH:MM(:SS)
        - YYYY-MM-DD HH:MM(:SS)
    If seconds are missing, minute resolution is assumed.
    """
    s = raw.astype(str).str.strip()

    formats = [
        "%Y/%m/%d %H:%M:%S",
        "%d/%m/%Y %H:%M:%S",
        "%Y-%m-%d %H:%M:%S",
        "%Y/%m/%d %H:%M",
        "%d/%m/%Y %H:%M",
        "%Y-%m-%d %H:%M",
    ]

    ts = pd.to_datetime(s, format=formats[0], errors="coerce")

    for fmt in formats[1:]:
        ts = ts.fillna(pd.to_datetime(s, format=fmt, errors="coerce"))

    # Final fallback (auto-detection, day-first enabled)
    ts = ts.fillna(pd.to_datetime(s, errors="coerce", dayfirst=True))
    return ts


def download_sauran(site: str,
                    begin: str,
                    end: str,
                    save_path: str = "sauran_out.csv",
                    tz_offset_hours: float = 2.0) -> None:
    """
    High-level SAURAN download interface (public API).

    Steps performed:
        - Build SAURAN API request URL
        - Handle HTTPS fallback to HTTP when necessary
        - Parse 4-line header (name, unit)
        - Parse timestamps with multiple formats
        - Convert local timestamps to UTC and offset string
        - Insert UTC_Time, Local_Time, UTC_Offset
        - Save to CSV

    Parameters
    ----------
    site : str
        SAURAN station ID (e.g., "NMU", "UNV").
    begin : str
        Start date (YYYYMMDD or YYYY-MM-DD).
    end : str
        End date (YYYYMMDD or YYYY-MM-DD).
    save_path : str
        Output CSV file path.
    tz_offset_hours : float
        Timezone offset from UTC (South Africa = +2).

    Notes
    -----
    The function replaces the previous fetch_sauran_to_csv().
    All internal logic remains unchanged.
    """

    base_url_https = "https://sauran.ac.za/api/DataDownload"
    base_url_http  = "http://sauran.ac.za/api/DataDownload"
    user_type = "Minute"

    start_str = init_str_date(begin)
    end_str   = init_str_date(end)

    def build_url(base):
        url = url_contact(base, site)
        url = url_contact(url, user_type)
        url = url_contact(url, start_str)
        url = url_contact(url, end_str)
        return url

    # Try HTTPS first; fallback to HTTP
    url = build_url(base_url_https)
    try:
        resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"},
                            timeout=60, verify=False)
        resp.raise_for_status()
    except Exception as e:
        print(f"[warn] HTTPS failed, retrying HTTP: {e}")
        url = build_url(base_url_http)
        resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=60)
        resp.raise_for_status()

    lines = resp.text.splitlines()
    if len(lines) < 5:
        raise RuntimeError(f"[error] Response too short: only {len(lines)} lines")

    # Line 2: field names; line 3: units
    field_row = [x.strip() for x in lines[1].split(",")]
    unit_row  = [x.strip() for x in lines[2].split(",")]

    # Data begins at line 5
    data_text = "\n".join(lines[4:])
    df = pd.read_csv(StringIO(data_text), header=None)

    # Align header lengths
    data_cols = df.shape[1]

    if len(unit_row) < len(field_row):
        unit_row += [""] * (len(field_row) - len(unit_row))
    if len(field_row) < len(unit_row):
        field_row += [""] * (len(unit_row) - len(field_row))

    header = [
        f"{f}[{u}]" if (f and u) else (f or "")
        for f, u in zip(field_row, unit_row)
    ]

    # Match header length with data columns
    if len(header) < data_cols:
        header += [f"Extra_{i}" for i in range(len(header), data_cols)]
    elif len(header) > data_cols:
        header = header[:data_cols]

    df.columns = header

    # First column must be TmStamp
    first_col = df.columns[0]
    if not first_col.lower().startswith("tmstamp"):
        if "tmstamp" not in first_col.lower():
            raise RuntimeError(f"Invalid format: expected TmStamp, got: {first_col}")

    # ================= Timestamp processing =================
    # SAURAN timestamps are END-OF-PERIOD → shift back 1 minute
    naive_ts = _parse_tmstamp_series(df.iloc[:, 0]) - pd.Timedelta(minutes=1)

    # Localize with fixed offset timezone
    tz = timezone(timedelta(hours=tz_offset_hours))
    local_ts = naive_ts.dt.tz_localize(tz, nonexistent="shift_forward", ambiguous="NaT")

    # Local time string (YYYY-MM-DD HH:MM:SS+HH:MM)
    local_str = local_ts.dt.strftime("%Y-%m-%d %H:%M:%S%z").str.replace(
        r"([+-]\d{2})(\d{2})$", r"\1:\2", regex=True
    )

    # UTC time (YYYY-MM-DD HH:MM:SS)
    utc_str = local_ts.dt.tz_convert("UTC").dt.strftime("%Y-%m-%d %H:%M:%S")
    offset_str = fmt_offset(tz_offset_hours)

    # Insert unified output columns
    df.drop(columns=[df.columns[0]], inplace=True)
    df.insert(0, "UTC_Time", utc_str)
    df.insert(1, "Local_Time", local_str)
    df.insert(2, "UTC_Offset", offset_str)

    # Save output
    ensure_dir(os.path.dirname(save_path) or ".")
    df.to_csv(save_path, index=False, encoding="utf-8-sig")

    print(f"[OK] Saved {save_path}, rows={len(df)}")

    # Print one sample row for quick inspection
    if len(df) > 0:
        print(f"Example: {df.iloc[0, 0]} UTC  <->  {df.iloc[0, 1]} Local  (offset {df.iloc[0, 2]})")
