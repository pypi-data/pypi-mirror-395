"""
HTTP client for sending traces to the Contexere backend

CRITICAL: This module must NEVER raise exceptions that break user code.
All errors are swallowed and logged internally.
"""

import json
from typing import Dict, Any, Optional
from contexere.config import get_config
from contexere.context import Span, Event

# Try to import httpx, fall back gracefully if not available
try:
    import httpx
    HTTPX_AVAILABLE = True
except ImportError:
    HTTPX_AVAILABLE = False


def _safe_serialize(obj: Any) -> Any:
    """
    Safely serialize objects to JSON-compatible types
    Handles non-serializable objects by converting to string
    """
    try:
        # Try direct JSON serialization
        json.dumps(obj)
        return obj
    except (TypeError, ValueError):
        # Fallback: convert to string representation
        try:
            return str(obj)
        except Exception:
            return "<non-serializable>"


def _truncate_if_needed(data: Dict[str, Any], max_size: int = 10000) -> Dict[str, Any]:
    """
    Truncate large payloads to prevent overwhelming the backend
    """
    serialized = json.dumps(data, default=_safe_serialize)
    if len(serialized) > max_size:
        # Truncate large fields
        if "inputs" in data and isinstance(data["inputs"], dict):
            data["inputs"] = {"_truncated": True, "size": len(str(data["inputs"]))}
        if "output" in data:
            data["output"] = {"_truncated": True, "size": len(str(data["output"]))}
        if "request" in data and isinstance(data["request"], dict):
            data["request"] = {"_truncated": True, "size": len(str(data["request"]))}
        if "response" in data and isinstance(data["response"], dict):
            data["response"] = {"_truncated": True, "size": len(str(data["response"]))}
    return data


def send_span(span: Span) -> None:
    """
    Send a span to the backend

    This function NEVER raises exceptions - all errors are silently handled
    """
    if not HTTPX_AVAILABLE:
        return  # Silently skip if httpx not installed

    config = get_config()

    if not config.enabled or not config.api_key:
        return  # Tracing disabled or not configured

    try:
        # Prepare payload
        payload = span.to_dict()
        payload = _truncate_if_needed(payload)

        # Send HTTP POST request
        with httpx.Client(timeout=config.timeout) as client:
            client.post(
                f"{config.endpoint}/ingest/span",
                json=payload,
                headers={"x-contexere-api-key": config.api_key}
            )
        # Success - no logging to avoid noise
    except Exception:
        # Silently fail - never break user code
        pass


def send_event(event: Event) -> None:
    """
    Send an event to the backend

    This function NEVER raises exceptions - all errors are silently handled
    """
    if not HTTPX_AVAILABLE:
        return  # Silently skip if httpx not installed

    config = get_config()

    if not config.enabled or not config.api_key:
        return  # Tracing disabled or not configured

    try:
        # Prepare payload
        payload = event.to_dict()
        payload = _truncate_if_needed(payload)

        # Send HTTP POST request
        with httpx.Client(timeout=config.timeout) as client:
            client.post(
                f"{config.endpoint}/ingest/event",
                json=payload,
                headers={"x-contexere-api-key": config.api_key}
            )
        # Success - no logging to avoid noise
    except Exception:
        # Silently fail - never break user code
        pass
