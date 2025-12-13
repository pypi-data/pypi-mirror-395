"""
The @conte.op() decorator for tracing function executions
"""

import functools
import inspect
from datetime import datetime
from typing import Callable, Any, Optional
from contexere.context import Span, set_current_span, get_current_span
from contexere.config import get_config, is_enabled
from contexere.log import send_span


def op(name: Optional[str] = None):
    """
    Decorator to trace function execution as a span

    Args:
        name: Optional custom name for the span (defaults to function name)

    Example:
        >>> import contexere as conte
        >>> @conte.op()
        ... def process_data(text):
        ...     return text.upper()

        >>> @conte.op(name="custom-operation")
        ... def another_func():
        ...     pass
    """

    def decorator(func: Callable) -> Callable:
        # Determine span name
        span_name = name if name else func.__name__

        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            # Skip if tracing disabled or not configured
            if not is_enabled():
                return func(*args, **kwargs)

            # Create span
            config = get_config()
            span = Span(
                name=span_name,
                start_time=datetime.utcnow(),
                meta={"project_name": config.project_name}
            )

            # Capture inputs (only if they're JSON-serializable)
            try:
                # Get function signature
                sig = inspect.signature(func)
                bound_args = sig.bind(*args, **kwargs)
                bound_args.apply_defaults()

                # Store arguments
                span.inputs = dict(bound_args.arguments)
            except Exception:
                # If we can't capture inputs, that's okay
                span.inputs = {}

            # Set as current span in context
            previous_span = get_current_span()
            set_current_span(span)

            try:
                # Execute the decorated function
                result = func(*args, **kwargs)

                # Capture output
                try:
                    span.output = result
                except Exception:
                    span.output = "<non-serializable>"

                # Record end time
                span.end_time = datetime.utcnow()
                span.duration_ms = (
                    (span.end_time - span.start_time).total_seconds() * 1000
                )

                return result

            except Exception as e:
                # Capture exception
                span.error = f"{type(e).__name__}: {str(e)}"
                span.end_time = datetime.utcnow()
                span.duration_ms = (
                    (span.end_time - span.start_time).total_seconds() * 1000
                )

                # Re-raise the exception (never swallow user exceptions)
                raise

            finally:
                # Send span to backend (this never raises exceptions)
                try:
                    send_span(span)
                except Exception:
                    pass  # Absolutely never break user code

                # Restore previous span context
                set_current_span(previous_span)

        return wrapper

    return decorator
