"""
OpenAI client instrumentation for tracing LLM calls
"""

from datetime import datetime
from typing import Any, Optional
from contexere.context import Event, get_current_span
from contexere.config import get_config, is_enabled
from contexere.log import send_event


class InstrumentedOpenAI:
    """
    Wrapper around OpenAI client that traces all LLM calls

    This wrapper intercepts chat.completions.create() calls and logs them as events
    """

    def __init__(self, client):
        """
        Initialize instrumented OpenAI client

        Args:
            client: An OpenAI client instance
        """
        self._client = client

        # Wrap the chat completions interface
        self.chat = InstrumentedChatCompletions(client.chat, self)

        # Pass through all other attributes to the underlying client
        for attr in dir(client):
            if not attr.startswith('_') and attr != 'chat' and not hasattr(self, attr):
                setattr(self, attr, getattr(client, attr))


class InstrumentedChatCompletions:
    """Wrapper for OpenAI chat completions"""

    def __init__(self, chat, instrumented_client):
        self._chat = chat
        self._instrumented_client = instrumented_client

        # Wrap the completions interface
        self.completions = InstrumentedCompletionsCreate(chat.completions)

        # Pass through other attributes
        for attr in dir(chat):
            if not attr.startswith('_') and attr != 'completions' and not hasattr(self, attr):
                setattr(self, attr, getattr(chat, attr))


class InstrumentedCompletionsCreate:
    """Wrapper for OpenAI chat completions create"""

    def __init__(self, completions):
        self._completions = completions

        # Pass through all attributes except 'create'
        for attr in dir(completions):
            if not attr.startswith('_') and attr != 'create' and not hasattr(self, attr):
                setattr(self, attr, getattr(completions, attr))

    def create(self, **kwargs) -> Any:
        """
        Instrumented version of chat.completions.create()

        Traces the LLM call as an event and associates it with the current span
        """
        # If tracing is disabled, just call the original function
        if not is_enabled():
            return self._completions.create(**kwargs)

        # Create event
        config = get_config()
        current_span = get_current_span()

        event = Event(
            span_id=current_span.id if current_span else None,
            op="openai.chat.completions.create",
            start_time=datetime.utcnow(),
            meta={"project_name": config.project_name}
        )

        # Capture request
        try:
            event.request = {
                "model": kwargs.get("model"),
                "messages": kwargs.get("messages"),
                "temperature": kwargs.get("temperature"),
                "max_tokens": kwargs.get("max_tokens"),
                # Add other relevant parameters
            }
        except Exception:
            event.request = {"_error": "Failed to capture request"}

        try:
            # Execute the actual OpenAI call
            start = datetime.utcnow()
            response = self._completions.create(**kwargs)
            end = datetime.utcnow()

            # Calculate duration
            event.duration_ms = (end - start).total_seconds() * 1000

            # Capture response
            try:
                event.response = {
                    "id": getattr(response, "id", None),
                    "model": getattr(response, "model", None),
                    "choices": [
                        {
                            "message": {
                                "role": choice.message.role,
                                "content": choice.message.content,
                            },
                            "finish_reason": choice.finish_reason,
                        }
                        for choice in getattr(response, "choices", [])
                    ],
                    "usage": {
                        "prompt_tokens": getattr(response.usage, "prompt_tokens", None),
                        "completion_tokens": getattr(response.usage, "completion_tokens", None),
                        "total_tokens": getattr(response.usage, "total_tokens", None),
                    } if hasattr(response, "usage") else None,
                }
            except Exception:
                event.response = {"_error": "Failed to capture response"}

            return response

        except Exception as e:
            # Capture error
            event.error = f"{type(e).__name__}: {str(e)}"
            event.duration_ms = (datetime.utcnow() - event.start_time).total_seconds() * 1000

            # Re-raise exception (never swallow user exceptions)
            raise

        finally:
            # Send event to backend (never raises exceptions)
            try:
                send_event(event)
            except Exception:
                pass  # Never break user code


def instrument_openai(client):
    """
    Instrument an OpenAI client to trace all LLM calls

    Args:
        client: An OpenAI client instance

    Returns:
        An instrumented OpenAI client that traces all calls

    Example:
        >>> from openai import OpenAI
        >>> import contexere as conte
        >>>
        >>> conte.init(api_key="ck_12345", project_name="my-project")
        >>> client = conte.instrument_openai(OpenAI(api_key="sk_..."))
        >>>
        >>> # All calls are now traced
        >>> response = client.chat.completions.create(
        ...     model="gpt-4",
        ...     messages=[{"role": "user", "content": "Hello"}]
        ... )
    """
    return InstrumentedOpenAI(client)
