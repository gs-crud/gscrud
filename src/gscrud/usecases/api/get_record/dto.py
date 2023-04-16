from typing import Dict, List, Any
from dataclasses import dataclass


@dataclass
class GetRecordRequest:
    search_key: str = ""
    search_value: str = ""

@dataclass
class GetRecordResponse:
    response: List[Dict[str, Any]]
