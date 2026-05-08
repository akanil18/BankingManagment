import io
import pandas as pd
from typing import Optional


class FileParser:

    @staticmethod
    def parse(content: bytes, ext: str) -> Optional[pd.DataFrame]:
        try:
            if ext in ["xlsx", "xls"]:
                return pd.read_excel(io.BytesIO(content), engine="openpyxl")
            elif ext == "csv":
                return pd.read_csv(io.BytesIO(content))
        except Exception:
            return None
