from typing import Optional, Dict, Any, List
from fastapi import APIRouter, Depends,Request, HTTPException, Header
from gscrud.repositories.sheet_repository import SheetRepository
from gscrud.usecases.api.get_record import (
    GetRecordRequest,
    GetRecordResponse,
    GetRecordUseCase
)

from gscrud.usecases.api.add_record import (
    AddRecordRequest,
    AddRecordResponse,
    AddRecordUseCase
)
from pydantic import BaseModel

class Data(BaseModel):
    data: Dict[str, Any]


# router = APIRouter()
router = APIRouter(
    prefix="/api",
    tags=["api"],
    responses={404: {"description": "Not found"}},
)

def sheet_header(req: Request):
    if "x-sheet-id" not in req.headers:
        raise HTTPException(
                status_code=401,
                detail="Unauthorized"
            )
    return True


@router.get("/{sheet_name}/")
async def read_api(
    sheet_name: str, 
    authorized: bool = Depends(sheet_header),
    x_sheet_id: str = Header(None)
) -> list[Dict[str, Any]]:
    """
    Create an item with all the information:

    - **sheet_name**: Name of the sheet
    """
    if authorized:
        dto = GetRecordRequest()
        repo = SheetRepository(
            worksheet_id=x_sheet_id,
            sheet_name=sheet_name
        )
        use_case = GetRecordUseCase(repo)
        return use_case.execute(dto)
    
@router.post("/{sheet_name}/")
async def insert_api(
    sheet_name: str, 
    data: Data,
    authorized: bool = Depends(sheet_header),
    x_sheet_id: str = Header(None)
) -> Dict[str, Any]:
    """
    Create an item with all the information:

    - **sheet_name**: Name of the sheet
    """
    if authorized:
        dto = AddRecordRequest(
            data=data.data
        )
        print(type(data))
        repo = SheetRepository(
            worksheet_id=x_sheet_id,
            sheet_name=sheet_name
        )
        use_case = AddRecordUseCase(repo)
        return {"status": use_case.execute(dto).status}
    