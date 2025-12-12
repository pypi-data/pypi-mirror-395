from sqlalchemy import Table
from typing import Dict, Any

class DataMapper:
    def __init__(self, table: Table):
        self.table_name = table.name
        self.table = table

    def dict_to_row(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return {k: v for k, v in data.items() if k in self.table.c}
