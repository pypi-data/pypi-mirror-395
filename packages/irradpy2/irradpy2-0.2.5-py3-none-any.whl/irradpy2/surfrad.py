# surfrad.py
"""
SURFRAD radiation data downloader.

This module downloads SURFRAD data in NOAA GML format.
Behavior follows the same style as solrad.py:
    - Build URLs for realtime (last 48 hours) and archive directories
    - Parse metadata lines
    - Parse fixed-width data rows with QC filtering
    - Produce Local_Time, UTC_Time, UTC_Offset, and data variables
"""

import csv
import time
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Optional
from necessary_main import (
    init_date,
    http_get_with_retry,
    url_contact,
)


# ============================================================
# URL builder
# ============================================================

def _build_surfrad_urls(station: str, start_date, end_date) -> List[str]:
    """
    Build a list of SURFRAD URLs for the given date range.

    Rules:
        - Use realtime directory for the last ~48h of data
        - Use archive directory for older dates
    """
    base = "https://gml.noaa.gov/aftp/data/radiation/surfrad"
    station = station.lower()
    today_utc = datetime.now(timezone.utc).date()

    urls = set()
    delta = (end_date - start_date).days + 1

    for i in range(delta):
        d = start_date + timedelta(days=i)
        yy = d.strftime("%y")
        year = d.year
        doy = d.timetuple().tm_yday
        fname = f"{station}{yy}{doy:03d}.dat"

        # realtime directory (last 48 hours)
        if d >= today_utc - timedelta(days=2):
            u = url_contact(base, "realtime")
            u = url_contact(u, station)
            u = url_contact(u, str(year))
            u = url_contact(u, fname)
            urls.add(u)

        # archive directory
        if d <= today_utc - timedelta(days=1):
            u = url_contact(base, station)
            u = url_contact(u, str(year))
            u = url_contact(u, fname)
            urls.add(u)

    return sorted(urls)


# ============================================================
# Parse a single SURFRAD data line
# ============================================================

def _parse_surfrad_line(fields: List[str]) -> Optional[Dict]:
    """
    Parse a single SURFRAD data row.

    The field positions match the NOAA SURFRAD .dat format.
    QC logic:
        value = raw_value if (qc == 0 and value != -9999.9)
                else -999.9
    """
    try:
        # Parse timestamp (SURFRAD times are in UTC)
        year = int(fields[0])
        month = int(fields[2])
        day = int(fields[3])
        hour = int(fields[4])
        minute = int(fields[5])

        utc_dt = datetime(year, month, day, hour, minute, tzinfo=timezone.utc)

        record = {
            "Local_Time": utc_dt.strftime("%Y/%m/%d %H:%M:00"),
            "UTC_Time": utc_dt.strftime("%Y/%m/%d %H:%M:00"),
            "UTC_Offset": "+00:00"
        }

        # Variable positions (value at idx, QC at idx+1)
        var_map = [
            ("dw_solar",     8),
            ("uw_solar",     10),
            ("direct_n",     12),
            ("diffuse",      14),
            ("dw_ir",        16),
            ("dw_casetemp",  18),
            ("dw_dometemp",  20),
            ("uw_ir",        22),
            ("uw_casetemp",  24),
            ("uw_dometemp",  26),
            ("uvb",          28),
            ("par",          30),
            ("netsolar",     32),
            ("netir",        34),
            ("totalnet",     36),
            ("temp",         38),
            ("rh",           40),
            ("windspd",      42),
            ("winddir",      44),
            ("pressure",     46),
        ]

        for key, idx in var_map:
            val = float(fields[idx])
            qc = int(fields[idx + 1])
            record[key] = val if (qc == 0 and val != -9999.9) else -999.9

        return record

    except Exception:
        return None


# ============================================================
# Public API: unified interface
# ============================================================

def download_surfrad(
    station: str,
    start: str,
    end: str,
    output_path: Optional[str] = None
):
    """
    Public SURFRAD download function (replaces fetch_surfrad_data).

    Steps performed:
        - Build URLs for the specified date range
        - Download each file
        - Parse metadata (station name, optional version)
        - Parse all raw data rows with QC filtering
        - Deduplicate and sort
        - Write CSV output

    Parameters
    ----------
    station : str
        SURFRAD station ID (e.g., "bon", "dra", "fpk").
    start : str
        Start date (YYYY-MM-DD or YYYYMMDD).
    end : str
        End date (YYYY-MM-DD or YYYYMMDD).
    output_path : str, optional
        Output CSV path. If None, the filename is auto-generated.

    Notes
    -----
    Internal behaviors are fully preserved from the original version.
    Only comments and the public API name are changed.
    """

    start_date = init_date(start)
    end_date = init_date(end)

    if not output_path:
        output_path = f"surfrad_{start_date}_{end_date}.csv"

    station = station.lower()
    urls = _build_surfrad_urls(station, start_date, end_date)

    all_rows = []
    headers = {"User-Agent": "Mozilla/5.0"}

    for url in urls:
        try:
            text = http_get_with_retry(url, headers=headers, timeout=20, max_retries=3)
            lines = [ln.strip() for ln in text.splitlines() if ln.strip()]

            if len(lines) < 3:
                print(f"[warn] Empty or incomplete file: {url}")
                continue

            station_name = lines[0]
            meta_info = lines[1].split()

            print(f"[ok] {url} | {station_name} | +{len(lines) - 2} rows")

            # Parse data rows
            for ln in lines[2:]:
                fields = ln.split()
                rec = _parse_surfrad_line(fields)
                if rec:
                    all_rows.append(rec)

        except Exception as e:
            print(f"[err] {e} | {url}")

        finally:
            time.sleep(0.25)

    # Deduplicate by UTC_Time
    seen = set()
    dedup = []
    for r in all_rows:
        k = r["UTC_Time"]
        if k not in seen:
            seen.add(k)
            dedup.append(r)

    dedup.sort(key=lambda x: x["UTC_Time"])

    # CSV columns
    csv_cols = [
        "Local_Time", "UTC_Time", "UTC_Offset",
        "dw_solar", "uw_solar", "direct_n", "diffuse",
        "dw_ir", "dw_casetemp", "dw_dometemp",
        "uw_ir", "uw_casetemp", "uw_dometemp",
        "uvb", "par", "netsolar", "netir", "totalnet",
        "temp", "rh", "windspd", "winddir", "pressure",
    ]

    # Write CSV
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=csv_cols)
        w.writeheader()
        w.writerows(dedup)

    print(f"\n[DONE] Saved: {output_path} | rows={len(dedup)} | station={station}")
