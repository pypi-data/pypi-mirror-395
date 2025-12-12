from dataclasses import dataclass, asdict
import json
from typing import Dict, Optional, Any, Union
from enum import Enum

class ResponseStatus(Enum):
    SUCCESS = "success"
    ERROR = "error"

@dataclass
class AgentRequest:
    agent: str
    params: Dict[str, Any]

    @classmethod
    def from_json(cls, json_str: str) -> 'AgentRequest':
        data = json.loads(json_str)
        return cls(**data)

    def to_json(self) -> str:
        return json.dumps(asdict(self))

@dataclass
class AgentResponse:
    status: str  # Store as string to avoid serialization issues
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

    @classmethod
    def from_json(cls, json_str: str) -> 'AgentResponse':
        data = json.loads(json_str)
        return cls(**data)

    def to_json(self) -> str:
        return json.dumps(asdict(self))

    @classmethod
    def success(cls, result: Any) -> 'AgentResponse':
        # Convert the result to a proper dictionary format if it's not already
        if isinstance(result, dict):
            result_dict = result
        elif isinstance(result, str):
            result_dict = {"response": result}
        else:
            # For any other type, convert to string and wrap in response field
            result_dict = {"response": str(result)}
            
        return cls(
            status="success",
            result=result_dict,
            error=None  # Explicitly set to None for success responses
        )

    @classmethod
    def error(cls, error_message: str) -> 'AgentResponse':
        return cls(
            status="error",
            result=None,  # Explicitly set to None for error responses
            error=error_message
        )