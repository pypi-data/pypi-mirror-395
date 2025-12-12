# bsrn.py
"""
BSRN data downloader and parser (LR0100 version)
Prefers the *C0100 segment, falls back to *U0100 if needed.
Built on top of the necessary_main utility module.
"""

import ftplib
import os
import gzip
import csv
import shutil
from datetime import datetime, timedelta, timezone
from .necessary_main import ensure_dir, init_str_date
class BSRNDownloader:
    """
    BSRN FTP data downloader and parser (supports LR0100 only).
    This class handles:
        - FTP connection
        - File listing and downloading
        - GZ extraction
        - Parsing LR0100 lines
        - Converting data into a unified CSV format
    """

    HOST = "ftp.bsrn.awi.de"

    def __init__(self, site: str, username: str, password: str):
        self.site = site.lower()
        self.username = username
        self.password = password

    # ============================================
    # Downloading and extraction utilities
    # ============================================
    def _generate_month_ranges(self, start_date_str, end_date_str):
        """Generate monthly file segments (MMYY) between given date strings."""
        start_date = datetime.strptime(start_date_str, "%Y%m%d").date()
        end_date = datetime.strptime(end_date_str, "%Y%m%d").date()
        months = []
        cur = start_date.replace(day=1)

        while cur <= end_date:
            months.append(f"{cur.month:02d}{cur.year % 100:02d}")
            cur = (cur.replace(year=cur.year + 1, month=1)
                   if cur.month == 12 else cur.replace(month=cur.month + 1))
        return months

    def _safe_extract_gz(self, gz_path, output_dir):
        """Safely extract a .gz file. Returns True if succeeded."""
        try:
            with gzip.open(gz_path, 'rb') as gz:
                content = gz.read()

            base = os.path.basename(gz_path).replace(".gz", "")
            out_path = os.path.join(output_dir, base)

            with open(out_path, 'wb') as f:
                f.write(content)

            print(f"[Extracted] {out_path}")
            return True

        except Exception as e:
            print(f"[Extract error] {gz_path}: {e}")
            return False

    def download_and_extract(self, start_date, end_date, out_dir):
        """
        Download and extract all BSRN monthly .dat.gz files within the specified date range.
        """
        ensure_dir(out_dir)
        targets = [f"{self.site}{m}.dat.gz" for m in self._generate_month_ranges(start_date, end_date)]

        try:
            with ftplib.FTP(self.HOST) as ftp:
                ftp.login(self.username, self.password)
                ftp.cwd(f"/{self.site}/")

                files = []
                ftp.retrlines('NLST', files.append)
                exist = [f for f in files if f in targets]

                for f in exist:
                    local_gz = os.path.join(out_dir, f)
                    print(f"[Downloading] {f} ...")

                    with open(local_gz, 'wb') as lf:
                        ftp.retrbinary(f"RETR {f}", lf.write)

                    if self._safe_extract_gz(local_gz, out_dir):
                        os.remove(local_gz)

        except Exception as e:
            print(f"[FTP error] {e}")

    # ============================================
    # Data parsing utilities
    # ============================================
    @staticmethod
    def _merge_lines(lines):
        """
        Merge pairs of LR0100 lines into a single record.
        Ensures fixed-length output (21 fields).
        """
        merged = []
        for i in range(0, len(lines) - 1, 2):
            l1, l2 = lines[i], lines[i + 1]
            m = (l1 + l2 + [None] * 21)[:21]
            merged.append(m)
        return merged

    @staticmethod
    def _parse_dat_file(fpath, start_dt, end_dt):
        """
        Parse a BSRN .dat file and extract LR0100 records
        (prefer C0100 if available, else fall back to U0100).
        """
        lines = []
        has_c = False

        # Detect C0100 existence
        with open(fpath, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith("*C0100"):
                    has_c = True
                    break

        prefer = "C" if has_c else "U"

        with open(fpath, 'r', encoding='utf-8') as f:
            in_data = False
            for raw in f:
                line = raw.strip()

                if line.startswith("*U0100"):
                    in_data = (prefer == "U")
                    continue
                if line.startswith("*C0100"):
                    in_data = (prefer == "C")
                    continue

                # Stop when encountering new logic blocks
                if in_data and (line.startswith("*U") or line.startswith("*C")) and \
                        not (line.startswith("*U0100") or line.startswith("*C0100")):
                    in_data = False
                    continue

                if in_data and line:
                    lines.append(line.split())

        return BSRNDownloader._merge_lines(lines)

    # ============================================
    # CSV writing utilities
    # ============================================
    @staticmethod
    def _write_to_csv(merged, fpath, start_dt, end_dt, writer):
        """
        Write merged LR0100 records into CSV.
        Converts Day/Minute into UTC timestamps.
        """
        for rec in merged:
            try:
                day = int(rec[0])
                minute = int(rec[1])

                part = os.path.basename(fpath)[3:7]   # MMYY
                month = int(part[:2])
                year = 2000 + int(part[2:])

                ts = datetime(year, month, day, tzinfo=timezone.utc) + timedelta(minutes=minute)

                if not (start_dt <= ts <= end_dt):
                    continue

                utc_str = ts.strftime("%Y-%m-%d %H:%M:%S")
                row = [utc_str] + rec[2:21]  # drop Day & Minute

                writer.writerow(row)

            except Exception:
                continue

    def generate_csv(self, data_dir, start, end, out_path):
        """
        Generate the final CSV output from downloaded and parsed .dat files.
        """
        start_dt = datetime.strptime(start, "%Y%m%d").replace(tzinfo=timezone.utc)
        end_dt = datetime.strptime(end, "%Y%m%d").replace(hour=23, minute=59, tzinfo=timezone.utc)

        with open(out_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)

            writer.writerow([
                "UTC",
                "Avg_Global", "Std_Global", "Min_Global", "Max_Global",
                "Avg_Direct", "Std_Direct", "Min_Direct", "Max_Direct",
                "Diffuse_Avg", "Diffuse_Std", "Diffuse_Min", "Diffuse_Max",
                "LW_Avg", "LW_Std", "LW_Min", "LW_Max",
                "AirTemp", "RH", "Pressure"
            ])

            dat_files = sorted([d for d in os.listdir(data_dir) if d.endswith(".dat")])

            for name in dat_files:
                p = os.path.join(data_dir, name)
                merged = self._parse_dat_file(p, start_dt, end_dt)
                self._write_to_csv(merged, p, start_dt, end_dt, writer)

    # ============================================
    # Sorting & cleanup utilities
    # ============================================
    @staticmethod
    def _sort_csv(csv_path):
        """Sort the CSV file by UTC timestamp."""
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = sorted(reader, key=lambda x: datetime.strptime(x[0], "%Y-%m-%d %H:%M:%S"))

        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            w = csv.writer(f)
            w.writerow(header)
            w.writerows(rows)

    @staticmethod
    def _clean_temp(temp_dir):
        """Remove the temporary directory."""
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
            print(f"[Cleaned temp directory] {temp_dir}")

    def run(self, start, end, save_path):
        """
        Full workflow:
            - Download .gz files
            - Extract .dat files
            - Parse LR0100 data
            - Generate final CSV
            - Sort by UTC timestamp
            - Cleanup temp directory
        """
        temp_dir = "./_bsrn_temp"
        try:
            print(f"[BSRN] Downloading data for {self.site} ...")
            self.download_and_extract(start, end, temp_dir)
            self.generate_csv(temp_dir, start, end, save_path)
            self._sort_csv(save_path)
            print(f"[Completed] Output saved to: {save_path}")
        finally:
            self._clean_temp(temp_dir)


# =====================================================
# Public API (external users call ONLY this function)
# =====================================================
def download_bsrn(site, start, end, username, password, save_path):
    """
    Public high-level API for downloading BSRN LR0100 data.

    Parameters
    ----------
    site : str
        BSRN station ID (e.g., "cab")
    start : str
        Start date (YYYY-MM-DD or YYYYMMDD)
    end : str
        End date (YYYY-MM-DD or YYYYMMDD)
    username : str
        BSRN FTP username
    password : str
        BSRN FTP password
    save_path : str
        Output CSV path

    Notes
    -----
    This is the only function intended to be used by external users.
    All other methods inside BSRNDownloader are internal only.
    """
    start = init_str_date(start).replace("-", "")
    end = init_str_date(end).replace("-", "")
    d = BSRNDownloader(site, username, password)
    d.run(start, end, save_path)
