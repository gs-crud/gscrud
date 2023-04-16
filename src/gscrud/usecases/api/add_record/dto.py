from dataclasses import dataclass
from typing import Dict, Any, List

@dataclass
class AddRecordRequest:
    data: Dict[str, Any]

@dataclass
class AddRecordResponse:
    status: bool