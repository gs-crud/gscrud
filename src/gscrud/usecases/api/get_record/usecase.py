from .dto import GetRecordRequest, GetRecordResponse
from gscrud.repositories.sheet_repository import SheetRepository

class GetRecordUseCase:
    def __init__(self, repository: SheetRepository):
        self.repository = repository

    def execute(self, req: GetRecordRequest) -> GetRecordResponse:
        return self.repository.get_record()