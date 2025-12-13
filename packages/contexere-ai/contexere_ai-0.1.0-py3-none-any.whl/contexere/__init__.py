"""
Contexere - LLM Tracing and Context Engineering for Production AI Agents

A lightweight Python library for tracing LLM applications and agent workflows.
"""

from contexere.config import init
from contexere.op import op
from contexere.openai_instrumentation import instrument_openai

__version__ = "0.1.0"

__all__ = [
    "init",
    "op",
    "instrument_openai",
]
