from typing import Optional
from fastapi import APIRouter, Depends,Request, HTTPException, Header

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
        return {"sheet": sheet_name, "id": x_sheet_id}
    