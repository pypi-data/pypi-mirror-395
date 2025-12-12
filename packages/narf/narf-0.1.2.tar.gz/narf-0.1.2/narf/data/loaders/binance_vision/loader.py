import hashlib
import io
import os
from typing import List, Optional
from datetime import datetime
import zipfile
from matplotlib.dates import relativedelta
import requests
import pandas as pd

from narf.data.loaders.base_loader import Loader, extract_semantic_path


URL_PATTERNS = [
    (
        (),
        "{base}/{market}/um/monthly/klines/{symbol}/{interval}/{symbol}-{interval}-{year}-{month:02d}.zip",
    ),
    (
        ("futures",),
        "{base}/{market}/um/monthly/klines/{symbol}/{interval}/{symbol}-{interval}-{year}-{month:02d}.zip",
    ),
    (
        ("futures", "<margination>", "<datatype>"),
        "{base}/{market}/{margination}/monthly/{datatype}/{symbol}/{interval}/{symbol}-{interval}-{year}-{month:02d}.zip",
    ),

    (
        ("spot",),
        "{base}/{market}/monthly/{datatype}/{symbol}/{interval}/{symbol}-{interval}-{year}-{month:02d}.zip",
    ),
    (
        ("spot", "aggTrades"),
        "{base}/{market}/monthly/{datatype}/{symbol}/{symbol}-{datatype}-{year}-{month:02d}.zip",
    ),
    (
        ("spot", "<datatype>"),
        "{base}/{market}/monthly/{datatype}/{symbol}/{interval}/{symbol}-{interval}-{year}-{month:02d}.zip",
    ),
]


INDEX_COLUMN = {
    "klines": "open_time",
    "trades": "timestamp",
    "aggTrades": "timestamp",
}


def cache_to_file(func):
    def wrapper(url: str, *args, **kwargs):
        url_hash = hashlib.sha256(url.encode()).hexdigest()
        cache_file = f"cache/{url_hash}.csv"
        if not os.path.exists(cache_file):
            df = func(url, *args, **kwargs)
            df.to_csv(cache_file)
        return pd.read_csv(cache_file)
    return wrapper


@cache_to_file
def load_zipped_csv(url: str, header: Optional[List[str]] = None) -> pd.DataFrame:
    r = requests.get(url)
    r.raise_for_status()

    zf = zipfile.ZipFile(io.BytesIO(r.content))
    name = zf.namelist()[0]

    with zf.open(name) as f:
        df = pd.read_csv(f)#, header=None if header else 0, names=header, index_col=False)

    return df


class BinanceVisionLoader(Loader):
    BASE_URL = "https://data.binance.vision/data"
    URL_PATTERNS = URL_PATTERNS

    def _load_month(self, symbol: str, interval: str, year: int, month: int) -> pd.DataFrame:
        url = self._build_url(**{
            "symbol": symbol,
            "interval": interval,
            "year": year,
            "month": month,
        })
        print('Loading', url)
        df = load_zipped_csv(url)

        path = self.get_parsed_path()
        idx_col = INDEX_COLUMN[path["datatype"]]

        df[idx_col] = pd.to_datetime(df[idx_col] * 1000000)
        df.set_index(idx_col, inplace=True)

        return df
    
    def load(self, symbol: str, start: datetime, end: Optional[datetime] = None, interval: str = "1m") -> pd.DataFrame:
        if end is None:
            end = datetime.now()

        cursor = start
        df = pd.DataFrame()
        while cursor <= end:
            df = pd.concat([
                df, 
                self._load_month(symbol, interval, cursor.year, cursor.month),
            ])
            cursor += relativedelta(months=1)
        
        return df