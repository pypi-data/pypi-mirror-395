from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class Finding:
    file_path: str
    line_no: int
    pattern_name: str
    severity: str
    description: str
    line_preview: str

    # AI fields (optional)
    ai_confirmed: Optional[bool] = None
    ai_severity: Optional[str] = None
    ai_type: Optional[str] = None
    ai_reason: Optional[str] = None

    def effective_severity(self) -> str:
        return (self.ai_severity or self.severity).upper()

    def to_dict(self) -> Dict:
        return {
            "file": self.file_path,
            "line": self.line_no,
            "pattern": self.pattern_name,
            "severity": self.severity,
            "description": self.description,
            "line_preview": self.line_preview.strip(),
            "ai_confirmed": self.ai_confirmed,
            "ai_severity": self.ai_severity,
            "ai_type": self.ai_type,
            "ai_reason": self.ai_reason,
        }
