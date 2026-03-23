import logging
from pathlib import Path
from typing import Union, List, Dict, Optional

from pdfmaster.src.extractors.table_extractor import TableExtractor

logger = logging.getLogger(__name__)


class SchemaGenerator:
    def __init__(self):
        self.table_extractor = TableExtractor()

    def extract(
        self, input_path: Union[str, Path], table_name: Optional[str] = None
    ) -> str:
        tables = self.table_extractor.extract(input_path)

        if not tables:
            raise ValueError("No tables found in PDF")

        sql_statements = []

        for idx, table in enumerate(tables):
            table_nm = table_name or f"extracted_table_{idx + 1}"
            headers = table["headers"]
            rows = table["rows"]

            columns = []
            for col_name in headers:
                safe_name = self._sanitize_column_name(col_name)
                columns.append(f"    {safe_name} TEXT")

            create_stmt = f"CREATE TABLE {table_nm} (\n"
            create_stmt += ",\n".join(columns)
            create_stmt += "\n);"

            sql_statements.append(create_stmt)

            for row in rows[:5]:
                if any(cell for cell in row):
                    insert_stmt = f"INSERT INTO {table_nm} ({', '.join(self._sanitize_column_name(h) for h in headers)}) VALUES ("
                    values = []
                    for cell in row:
                        val = str(cell).replace("'", "''") if cell else "NULL"
                        values.append(f"'{val}'")
                    insert_stmt += ", ".join(values)
                    insert_stmt += ");"
                    sql_statements.append(insert_stmt)

        logger.info(f"Generated SQL schema with {len(tables)} tables")
        return "\n\n".join(sql_statements)

    def _sanitize_column_name(self, name: str) -> str:
        name = name.strip()
        name = name.replace(" ", "_").replace("-", "_")
        name = "".join(c for c in name if c.isalnum() or c == "_")
        if name[0].isdigit():
            name = "col_" + name
        return name.lower() or "column"


class SQLExporter:
    def export(self, sql_content: str, output_path: Union[str, Path]) -> Path:
        if isinstance(output_path, str):
            output_path = Path(output_path)

        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(sql_content)

        logger.info(f"Exported SQL schema to {output_path}")
        return output_path
