from typing import List, Dict


def validate_required_fields(data: Dict, required_fields: List[str]) -> List[str]:
    missing_fields = [
        field for field in required_fields if field not in data or data[field] is None
    ]
    return missing_fields
