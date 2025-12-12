# midc.py
"""
MIDC data downloader.
Uses utility functions in necessary_main to download data from NREL MIDC.
Supports multi-month parallel downloads, chronological reordering,
UTC time generation, DST ambiguity resolution, and column filtering.
"""

from datetime import datetime, timedelta
from io import StringIO
from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd
from necessary_main import (http_get_with_retry,read_flexible_csv,attach_local_and_offset,clip_by_local_date,expand_unnamed_columns,)

# Columns to keep for each site (mapping from raw MIDC column → unified lowercase name)
COLUMNS_TO_KEEP = {
    'BMS': {
        'Global CMP22 (vent/cor) [W/m^2]': 'ghi',
        'Direct CHP1-1 [W/m^2]': 'dni_chp1',
        'Direct NIP [W/m^2]': 'dni_nip',
        'Diffuse CM22-1 (vent/cor) [W/m^2]': 'dhi',
        'Avg Wind Speed @ 6ft [m/s]': 'wind_speed',
        'Tower Dry Bulb Temp [deg C]': 'temp_air',
        'Station Pressure [mBar]': 'air_pressure',
        'Tower RH [%]': 'relative_humidity'
    },
    'UOSMRL': {
        'Global CMP22 [W/m^2]': 'ghi',
        'Direct CHP1 [W/m^2]': 'dni_chp1',
        'Diffuse [W/m^2]': 'dhi',
        'Direct NIP [W/m^2]': 'dni_nip',
        'Air Temperature [deg C]': 'temp_air',
        'Relative Humidity [%]': 'relative_humidity',
        'Avg Wind Speed @ 10m [m/s]': 'wind_speed'
    },
    'HSU': {
        'Global Horiz [W/m^2]': 'ghi',
        'Direct Normal (calc) [W/m^2]': 'dni',
        'Diffuse Horiz (band_corr) [W/m^2]': 'dhi'
    },
    'UTPASRL': {
        'Global Horizontal [W/m^2]': 'ghi',
        'Direct Normal [W/m^2]': 'dni',
        'Diffuse Horizontal [W/m^2]': 'dhi',
        'CHP1 Temp [deg C]': 'temp_air'
    },
    'UAT': {
        'Global Horiz (platform) [W/m^2]': 'ghi',
        'Direct Normal [W/m^2]': 'dni',
        'Diffuse Horiz [W/m^2]': 'dhi',
        'Air Temperature [deg C]': 'temp_air',
        'Rel Humidity [%]': 'relative_humidity',
        'Avg Wind Speed @ 3m [m/s]': 'wind_speed'
    },
    'STAC': {
        'Global Horizontal [W/m^2]': 'ghi',
        'Direct Normal [W/m^2]': 'dni',
        'Diffuse Horizontal [W/m^2]': 'dhi',
        'Avg Wind Speed @ 10m [m/s]': 'wind_speed',
        'Air Temperature [deg C]': 'temp_air',
        'Rel Humidity [%]': 'relative_humidity'
    },
    'UNLV': {
        'Global Horiz [W/m^2]': 'ghi',
        'Direct Normal [W/m^2]': 'dni',
        'Diffuse Horiz (calc) [W/m^2]': 'dhi',
        'Dry Bulb Temp [deg C]': 'temp_air',
        'Avg Wind Speed @ 30ft [m/s]': 'wind_speed'
    },
    'ORNL': {
        'Global Horizontal [W/m^2]': 'ghi',
        'Direct Normal [W/m^2]': 'dni',
        'Diffuse Horizontal [W/m^2]': 'dhi',
        'Air Temperature [deg C]': 'temp_air',
        'Rel Humidity [%]': 'relative_humidity',
        'Avg Wind Speed @ 42ft [m/s]': 'wind_speed'
    },
    'NELHA': {
        'Global Horizontal [W/m^2]': 'ghi',
        'Air Temperature [W/m^2]': 'temp_air',
        'Avg Wind Speed @ 10m [m/s]': 'wind_speed',
        'Rel Humidity [%]': 'relative_humidity'
    },
    'ULL': {
        'Global Horizontal [W/m^2]': 'ghi',
        'Direct Normal [W/m^2]': 'dni',
        'Diffuse Horizontal [W/m^2]': 'dhi',
        'Air Temperature [deg C]': 'temp_air',
        'Rel Humidity [%]': 'relative_humidity',
        'Avg Wind Speed @ 3m [m/s]': 'wind_speed'
    },
    'NWTC': {
        'Global Horizontal [W/m^2]': 'ghi',
        'Direct Normal [W/m^2]': 'dni',
        'Diffuse Horizontal [W/m^2]': 'dhi',
        'Temperature @ 2m [deg C]': 'temp_air',
        'Avg Wind Speed @ 2m [m/s]': 'wind_speed',
        'Relative Humidity [%]': 'relative_humidity'
    },
}


def download_midc(site: str, begin: str, end: str, save_path: str = "midc_out.csv") -> None:
    """
    Public high-level MIDC download interface.
    This function replaces the old fetch_midc_to_csv().

    Steps performed:
        - Split the date range into monthly chunks
        - Parallel fetch (thread pool) for each month
        - Merge results in chronological order
        - DST ambiguity resolution (fall-back hour duplication handling)
        - Generate UTC_Time
        - Retain selected columns based on COLUMNS_TO_KEEP
        - Save to CSV

    Parameters
    ----------
    site : str
        MIDC site ID (e.g., "BMS").
    begin : str
        Start date (YYYYMMDD).
    end : str
        End date (YYYYMMDD).
    save_path : str
        Output CSV file path.

    Notes
    -----
    Internal behavior is unchanged. Only the public API name was unified.
    """
    max_workers = 6  # recommended for stability

    # Convert date to datetime
    begin_dt = datetime.strptime(begin, "%Y%m%d")
    end_dt = datetime.strptime(end, "%Y%m%d")
    end_plus1 = end_dt + timedelta(days=1)

    # Split range into monthly segments
    months = []
    cur = begin_dt.replace(day=1)
    while cur.date() <= end_dt.date():
        nxt = (cur.replace(year=cur.year + 1, month=1, day=1)
               if cur.month == 12 else
               cur.replace(month=cur.month + 1, day=1))
        months.append((cur, nxt - timedelta(days=1)))
        cur = nxt

    base_url = "https://midcdmz.nrel.gov/apps/data_api.pl"

    # Fast CSV parser
    def fast_read_csv(text: str) -> pd.DataFrame:
        """Try fast C-engine CSV parsing; fall back to flexible parsing."""
        try:
            return pd.read_csv(StringIO(text), sep=",", engine="c", on_bad_lines="skip")
        except Exception:
            return read_flexible_csv(text)

    # Fetch a single month
    def fetch_one(month_start, month_end) -> pd.DataFrame:
        text = http_get_with_retry(
            base_url,
            params={
                "site": site,
                "begin": month_start.strftime("%Y%m%d"),
                "end": month_end.strftime("%Y%m%d"),
            },
        )

        df = fast_read_csv(text)

        # Validate basic structure
        if df.empty or df.shape[1] < 4 or "Year" not in df.columns or "DOY" not in df.columns:
            return pd.DataFrame()

        # Time column (local solar time)
        time_col = df.columns[3]

        # Construct naive local timestamps
        year_i = df["Year"].astype("int32")
        doy_i = df["DOY"].astype("int32")
        hhmm_i = df[time_col].astype("Int64").fillna(0).astype("int32")
        hours = (hhmm_i // 100).astype("int16")
        mins = (hhmm_i % 100).astype("int16")

        year_start = pd.to_datetime(year_i.astype(str) + "-01-01", format="%Y-%m-%d")
        naive_local = (year_start
                       + pd.to_timedelta(doy_i - 1, unit="D")
                       + pd.to_timedelta(hours, unit="h")
                       + pd.to_timedelta(mins, unit="m"))

        # Initial clipping using naive timestamps
        mask = (naive_local >= begin_dt) & (naive_local < end_plus1)
        if not mask.any():
            return pd.DataFrame()

        out = df.loc[mask].copy()
        out.insert(0, "_naive_local", naive_local.loc[mask].values)
        return out

    # Parallel monthly fetch
    parts = []
    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        futs = {ex.submit(fetch_one, ms, me): (ms, me) for (ms, me) in months}
        for fut in as_completed(futs):
            df_part = fut.result()
            if not df_part.empty:
                parts.append((futs[fut][0], df_part))

    if not parts:
        raise RuntimeError(f"[error] No data available for {site} within the specified range ({begin}~{end})")

    # Sort by month and concatenate
    parts.sort(key=lambda x: x[0])
    final_df = pd.concat([p[1] for p in parts], ignore_index=True)

    # Resolve DST ambiguity for America/Denver timezone
    ns = pd.to_datetime(final_df["_naive_local"].values)
    ns = pd.Series(ns, index=final_df.index)

    key_min = ns.dt.strftime("%Y-%m-%d %H:%M")
    dup_mask = key_min.duplicated(keep=False)
    first_of_dup = ~key_min.duplicated(keep='first') & dup_mask

    ambiguous_vec = pd.Series(False, index=ns.index)
    ambiguous_vec[first_of_dup] = True

    local_ts = ns.dt.tz_localize(
        "America/Denver",
        nonexistent="shift_forward",
        ambiguous=ambiguous_vec.values
    )
    final_df = final_df.drop(columns=["_naive_local"])

    # Generate Local_Time and UTC_Offset
    final_df = attach_local_and_offset(final_df, local_ts)

    # Generate UTC_Time
    utc_time_str = local_ts.dt.tz_convert("UTC").dt.strftime("%Y/%m/%d %H:%M:00")
    final_df.insert(0, "UTC_Time", utc_time_str)

    # Reorder columns
    if site in COLUMNS_TO_KEEP:
        keep = expand_unnamed_columns(final_df.columns) + [
            c for c in COLUMNS_TO_KEEP[site] if c in final_df.columns
        ]
        base_cols = ["UTC_Time", "Local_Time", "UTC_Offset"]
        final_df = final_df[base_cols + keep] if keep else final_df[base_cols]
    else:
        final_df = final_df[["UTC_Time", "Local_Time", "UTC_Offset"]]

    # Final clipping using timezone-aware timestamps
    mask, _ = clip_by_local_date(local_ts, begin, end, "America/Denver")
    final_df = final_df[mask].reset_index(drop=True)
    final_df = final_df.loc[:, ~final_df.columns.str.contains('^Unnamed')]

    # Save CSV
    final_df.to_csv(save_path, index=False)
    print(f"[OK] Saved {save_path}, rows={len(final_df)}, threads={max_workers}")
