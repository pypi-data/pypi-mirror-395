from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class ExpressionResult:
    expr: str
    value: Any = None
    type: Any = None
    failed: bool = False
    failed_reason: Optional[str] = None
