import logging
from pathlib import Path
from typing import Union, List, Dict, Optional
import pandas as pd

logger = logging.getLogger(__name__)


class TableExtractor:
    def __init__(self):
        self.min_rows = 2
        self.min_cols = 2

    def extract(self, input_path: Union[str, Path]) -> List[Dict]:
        if isinstance(input_path, str):
            input_path = Path(input_path)

        if not input_path.exists():
            raise FileNotFoundError(f"PDF file not found: {input_path}")

        try:
            import pdfplumber
        except ImportError:
            raise ImportError("pdfplumber is required for table extraction")

        tables_data = []

        with pdfplumber.open(input_path) as pdf:
            for page_num, page in enumerate(pdf.pages):
                tables = page.extract_tables()

                for table_idx, table in enumerate(tables):
                    if table and len(table) >= self.min_rows and len(table[0]) >= self.min_cols:
                        df = pd.DataFrame(table[1:], columns=table[0])

                        tables_data.append({
                            "page": page_num + 1,
                            "table_index": table_idx,
                            "headers": table[0],
                            "rows": table[1:],
                            "dataframe": df,
                        })

        logger.info(f"Extracted {len(tables_data)} tables from PDF")
        return tables_data

    def extract_to_dataframes(
        self, input_path: Union[str, Path]
    ) -> List[pd.DataFrame]:
        tables = self.extract(input_path)
        return [t["dataframe"] for t in tables]
