import string
import pandas as pd
import numpy as np
from apiclient import discovery
from google.oauth2 import service_account, credentials
import pandas as pd
from gscrud.config import GOOGLE_SHEET_CRED_FILE_PATH
from typing import List, Any, Dict


class GoogleSheet:
    def __init__(self,
                 sheet_id: str,
                 sheet_name: str,
                 sheet_range: str = 'A:Z'):
        self.spreadsheet_id: str = sheet_id
        self.scopes: List[str] = ["https://www.googleapis.com/auth/drive",
                                  "https://www.googleapis.com/auth/drive.file",
                                  "https://www.googleapis.com/auth/spreadsheets"]
        self.sheet_range: str = sheet_range     # 'Sheet1!A:D'
        self.credentials: credentials = service_account.Credentials.from_service_account_file(
            GOOGLE_SHEET_CRED_FILE_PATH, scopes=self.scopes)
        self.service: str = discovery.build(
            'sheets', 'v4', credentials=self.credentials).spreadsheets()
        self.sheet_name: str = sheet_name
        self.df: pd.DataFrame = pd.DataFrame()
        self.cols: Dict[str, Dict[str, str]] = {}

        self.read_sheet_as_df()

    def get_all_sheets(self):
        sheet_meta = self.service.get(spreadsheetId=self.spreadsheet_id).execute()
        sheets = sheet_meta["sheets"]
        return sheets
    
    def get_sheet_grid_id(self):
        for sheet in self.get_all_sheets():
            if self.sheet_name == sheet["properties"]["title"]:
                return sheet["properties"]["sheetId"]

    def _return_json(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if isinstance(result, pd.DataFrame):
                return result.to_dict("records")
            return result
        return wrapper

    def insert_df(self, df: pd.DataFrame, append=True):
        df = df.replace(np.inf, "-")
        data = df.fillna("-").values.tolist()
        self.insert_list(data, append=append, sheet_name=self.sheet_name)

    def delete_row(self, row_number: int):
        print(self.spreadsheet_id)
        delete_dimension = {
            "requests": [
                {
                    "deleteDimension": {
                        "range": {
                            "sheetId": self.get_sheet_grid_id(),
                            "dimension": "ROWS",
                            "startIndex": row_number,
                            "endIndex": row_number+1,
                        }
                    }
                }
            ]
        }
        self.service.batchUpdate(
            spreadsheetId=self.spreadsheet_id, body=delete_dimension).execute()

    def read_sheet_as_df(self):
        data = self.service.values().get(spreadsheetId=self.spreadsheet_id,
                                         range=f"{self.sheet_name}!{self.sheet_range}").execute()
        self.df = pd.DataFrame(data['values'])
        self.df = self.df.T.set_index(0).T
        self.df["__row__"] = np.arange(1, len(self.df) + 1)
        for col in list(self.df):
            try:
                self.df[col] = self.df[col].apply(pd.to_numeric)
            except:
                pass
        for i, col in enumerate(list(self.df)):
            self.cols[col] = {
                "position": string.ascii_uppercase[i],
                "type": str(self.df[col].dtype)
            }
        return self.df

    def get_column_names(self) -> List[str]:
        if self.df.empty:
            self.read_sheet_as_df()
            return list(self.df)

    @_return_json
    def get_all(self) -> list:
        return self.df
    
    def update(self, column_to_update: str, value_to_update: str, condition_key: str, condition_value: str, condition_opeartor: str = "eq"):
        found_value = self.find_value(condition_key, condition_value, condition_opeartor)
        print(found_value)
        col_position = self.cols[column_to_update]["position"]
        update_data = []
        for f in found_value:
            col_ref = f"{col_position}{f['__row__']+1}"
            print(f"Updating => {col_ref}")
            update_data.append({
                "range": f"{self.sheet_name}!{col_ref}",
                "values": [[value_to_update]]
            })
        batch_update_values = {
            "valueInputOption": "RAW",
            "data": update_data
        }
        print(update_data)
        self.service.values().batchUpdate(spreadsheetId=self.spreadsheet_id, body=batch_update_values).execute()


    @_return_json
    def find_value(self, key: str, value: Any, operator: str = "eq"):
        # print(f"{key} - {value}")
        if self.df[key].dtype == object:
            return self.df.loc[self.df[key].str.contains(str(value))]
        if operator == "eq":
            return self.df[self.df[key] == value]
        if operator == "gr":
            return self.df[self.df[key] > value]
        if operator == "le":
            return self.df[self.df[key] < value]

    def insert_list(self, data: List[Any], append: bool=True) -> bool:
        print("Writing list to GSheet")
        print(data)
        insert_data = {
            'majorDimension': "ROWS",
            'values': data
        }
        if append:
            self.service.values().append(spreadsheetId=self.spreadsheet_id,
                                         body=insert_data,
                                         range=f"{self.sheet_name}!{self.sheet_range}",
                                         valueInputOption='USER_ENTERED').execute()
        return True


if __name__ == "__main__":
    import pandas as pd
    gs = GoogleSheet(
        sheet_id="1KF_GhbanJ186GEuAnrFPxEku5mbrwdcHubuMU5HX3D0",
        sheet_name="students")
    
    # gs.update("result", "pass", "mark", 50, "gr")
    # gs.update("result", "fail", "mark", 50, "le")
    # gs.update("result", "pass", "mark", 50, "eq")
    d = {
    "stu": 2,
    "name": "New",
    "mark": 25,
    "result": "fail"
  }

    gs.insert_list(
    [list(d.values())]
  )

    # print(gs.get_column_names())
    # print(gs.find_value("mark", 11, "gr"))
    # print(gs.find_value("name", "Muthu"))
    # print(gs.find_value("mark", 11, "le"))
    # print(gs.get_all())
    # print(gs.df)
    # gs.delete_row(1)
    # print(gs.get_all_sheets())

    # print(gs.df.dtypes)
