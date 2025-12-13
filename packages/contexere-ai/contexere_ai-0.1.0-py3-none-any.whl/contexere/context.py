"""
Context management for span tracking using contextvars
"""

from contextvars import ContextVar
from dataclasses import dataclass, field
from typing import Optional, Any, Dict
from datetime import datetime
import uuid


@dataclass
class Span:
    """Represents a single function execution trace"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    duration_ms: Optional[float] = None
    inputs: Optional[Dict[str, Any]] = None
    output: Any = None
    error: Optional[str] = None
    meta: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert span to dictionary for JSON serialization"""
        return {
            "id": self.id,
            "name": self.name,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "duration_ms": self.duration_ms,
            "inputs": self.inputs,
            "output": self.output,
            "error": self.error,
            "meta": self.meta,
        }


@dataclass
class Event:
    """Represents an LLM call within a span"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    span_id: Optional[str] = None
    op: str = ""
    start_time: Optional[datetime] = None
    duration_ms: Optional[float] = None
    request: Optional[Dict[str, Any]] = None
    response: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    meta: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary for JSON serialization"""
        return {
            "id": self.id,
            "span_id": self.span_id,
            "op": self.op,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "duration_ms": self.duration_ms,
            "request": self.request,
            "response": self.response,
            "error": self.error,
            "meta": self.meta,
        }


# Context variable to track the current active span
_current_span: ContextVar[Optional[Span]] = ContextVar("current_span", default=None)


def get_current_span() -> Optional[Span]:
    """Get the currently active span from context"""
    return _current_span.get()


def set_current_span(span: Optional[Span]) -> None:
    """Set the current active span in context"""
    _current_span.set(span)
