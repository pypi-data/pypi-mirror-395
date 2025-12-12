# necessary_main.py
"""
通用工具函数：网络请求 / CSV解析 / 时间处理 / 日期转换 / 路径拼接
供 MIDC、SAURAN 等下载器复用
"""

from datetime import datetime, timedelta, timezone
import pytz
import time
import csv
from io import StringIO
from typing import Optional, Sequence, Tuple
import requests
import pandas as pd
import os
import re

# ======================
# 网络 & CSV
# ======================
def http_get_with_retry(url: str,
                        params: Optional[dict] = None,
                        headers: Optional[dict] = None,
                        timeout: int = 30,
                        max_retries: int = 3,
                        backoff: float = 1.5) -> str:
    """
    带重试的 GET，请求文本（自动编码兜底+BOM 去除）
    - 默认开启 gzip/keep-alive
    - 连接/读取分离超时
    - 轻微抖动的指数退避
    """
    hdr = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "text/csv",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
    }
    if headers:
        hdr.update(headers)

    last_exc = None
    for i in range(max_retries):
        try:
            resp = requests.get(
                url,
                params=params,
                headers=hdr,
                timeout=(min(10, timeout // 2 or 5), timeout),
            )
            resp.raise_for_status()
            if not resp.encoding:
                resp.encoding = resp.apparent_encoding or "utf-8"
            return resp.text.lstrip("\ufeff")
        except Exception as e:
            last_exc = e
            if i < max_retries - 1:
                sleep_s = (backoff ** i) * (1 + 0.1 * (i % 3))  # 抖动退避
                print(f"[warn] HTTP失败，第{i+1}次重试，等待{sleep_s:.1f}s… 详情：{e}")
                time.sleep(sleep_s)
    raise last_exc


def read_flexible_csv(text: str) -> pd.DataFrame:
    """
    通用 CSV 解析器
    - 优先用快路径 C 引擎 + 逗号
    - 失败则用 Sniffer/正则
    - 自动修正 BOM 列名
    """
    raw = StringIO(text)
    try:
        df_fast = pd.read_csv(raw, sep=",", engine="c", on_bad_lines="skip")
        df_fast.columns = [c.replace("\ufeff", "").replace("ï»¿", "") for c in df_fast.columns]
        return df_fast
    except Exception:
        pass

    raw.seek(0)
    try:
        sample = raw.read(4096)
        raw.seek(0)
        dialect = csv.Sniffer().sniff(sample)
        sep = dialect.delimiter
    except Exception:
        sep = None
        raw.seek(0)

    try:
        if sep:
            head_df = pd.read_csv(raw, nrows=0, sep=sep, engine="python")
        else:
            head_df = pd.read_csv(raw, nrows=0, sep=r'[,\t]+|\s{2,}', engine="python")
        ncols = len(head_df.columns)
    except Exception:
        raw.seek(0)
        head_df = pd.read_csv(raw, nrows=0, sep=",", engine="python")
        ncols = len(head_df.columns)
    raw.seek(0)

    df = pd.read_csv(
        raw,
        usecols=range(ncols),
        sep=(sep if sep else r'[,\t]+|\s{2,}'),
        engine="python",
        on_bad_lines="skip",
        skip_blank_lines=True,
    )
    df.columns = [c.replace("\ufeff", "").replace("ï»¿", "") for c in df.columns]
    return df

# ======================
# 时间 & 本地化
# ======================
def tz_localize_safely(naive_ts: pd.Series,
                       tz: str,
                       nonexistent: str = "shift_forward",
                       ambiguous: str = "infer") -> pd.Series:
    """将 naive 的时间本地化为 tz-aware，DST 友好"""
    return naive_ts.dt.tz_localize(tz, nonexistent=nonexistent, ambiguous=ambiguous)


def format_local_str(local_ts: pd.Series,
                     fmt: str = "%Y/%m/%d %H:%M:00") -> pd.Series:
    """时间戳序列格式化为字符串"""
    return local_ts.dt.strftime(fmt)


def attach_local_and_offset(df: pd.DataFrame,
                            local_ts: pd.Series,
                            local_col: str = "Local_Time",
                            offset_col: str = "UTC_Offset") -> pd.DataFrame:
    """
    插入 Local_Time 和 UTC_Offset（完全向量化）
    """
    local_str = local_ts.dt.strftime("%Y/%m/%d %H:%M:00")
    z = local_ts.dt.strftime("%z").str.replace(r"([+-]\d{2})(\d{2})", r"\1:\2", regex=True)

    out = df.copy()
    out = out.assign(**{local_col: local_str, offset_col: z})
    cols = [local_col, offset_col] + [c for c in out.columns if c not in (local_col, offset_col)]
    return out[cols]


def clip_by_local_date(local_ts: pd.Series,
                       begin: str,
                       end: str,
                       tz: str) -> Tuple[pd.Series, pd.Series]:
    """按本地日期半开区间 [begin, end+1d) 截断"""
    beg = pd.to_datetime(begin, format="%Y%m%d").tz_localize(tz)
    endt = (pd.to_datetime(end, format="%Y%m%d") + pd.Timedelta(days=1)).tz_localize(tz)
    mask = (local_ts >= beg) & (local_ts < endt)
    return mask, local_ts[mask]

# ======================
# 其他通用
# ======================
def expand_unnamed_columns(actual_cols: Sequence[str],
                           prefix: str = "Unnamed:") -> list:
    """匹配所有 Unnamed: 开头的列"""
    return [c for c in actual_cols if c.startswith(prefix)]


def init_date(date_str):
    formats = ["%Y%m%d", "%Y.%m.%d", "%Y-%m-%d", "%Y/%m/%d"]
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue
    raise ValueError(f"无效日期格式: {date_str}")


def init_str_date(date_str):
    formats = ["%Y%m%d", "%Y.%m.%d", "%Y-%m-%d", "%Y/%m/%d"]
    for fmt in formats:
        try:
            date = datetime.strptime(date_str, fmt).date()
            return datetime.strftime(date, '%Y-%m-%d')
        except ValueError:
            continue
    raise ValueError(f"无效日期格式: {date_str}")


def get_yesterday_utc_minus_7():
    utc_minus_7 = pytz.timezone('America/Denver')
    now_utc_minus_7 = datetime.now(utc_minus_7)
    yesterday_utc_minus_7 = now_utc_minus_7 - timedelta(1)
    return yesterday_utc_minus_7.date()


def url_contact(url, content):
    """安全拼接 URL 段"""
    url = url.rstrip("/")
    content = str(content).strip("/")
    return f"{url}/{content}"


def ensure_dir(path: str):
    """确保目录存在"""
    if path and not os.path.exists(path):
        os.makedirs(path, exist_ok=True)


def fmt_offset(hours: float) -> str:
    """格式化时区偏移为 +HH:MM"""
    sign = "+" if hours >= 0 else "-"
    h = abs(int(hours))
    m = abs(int((hours - int(hours)) * 60))
    return f"{sign}{h:02d}:{m:02d}"
