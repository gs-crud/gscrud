from .dto import AddRecordRequest, AddRecordResponse
from gscrud.repositories.sheet_repository import SheetRepository

class AddRecordUseCase:
    def __init__(self, repository: SheetRepository):
        self.repository = repository

    def execute(self, req: AddRecordRequest) -> AddRecordResponse:
        return AddRecordResponse(status=self.repository.insert_record(req.data))