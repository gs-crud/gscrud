from typing import Dict, Any, List
from gscrud.providers.google_sheet import GoogleSheet

class SheetRepository:
    def __init__(self, worksheet_id: str, sheet_name: str):
        self.worksheet_id = worksheet_id
        self.provider = GoogleSheet(
            worksheet_id,
            sheet_name=sheet_name,
        )

    def get_record(self):
        return self.provider.get_all()
    
    def insert_record(self, record: Dict[str, Any]) -> bool:
        return self.provider.insert_list(data=[list(record.values())])