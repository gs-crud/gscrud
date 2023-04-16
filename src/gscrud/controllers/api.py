from typing import Optional
from fastapi import APIRouter, Depends,Request, HTTPException, Header
from gscrud.repositories.sheet_repository import SheetRepository
from gscrud.usecases.api.get_record import (
    GetRecordRequest,
    GetRecordResponse,
    GetRecordUseCase
)

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
):
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
    