# Contexere

**LLM Tracing and Context Engineering for Production AI Agents**

Contexere is a lightweight Python library for tracing LLM applications and agent workflows in production.

## Installation

```bash
pip install contexere
```

## Quick Start

```python
import contexere as conte
from openai import OpenAI

# Initialize Contexere
conte.init(
    api_key="ck_...",  # Your Contexere API key
    project_name="my-agent"
)

# Instrument your OpenAI client
client = conte.instrument_openai(OpenAI(api_key="sk_..."))

# Trace function executions
@conte.op()
def process_query(question):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": question}]
    )
    return response.choices[0].message.content

# All calls are now traced automatically
result = process_query("What is the capital of France?")
```

## Features

- **Function-level tracing**: Use `@conte.op()` to trace any function
- **LLM call tracing**: Automatic instrumentation for OpenAI calls
- **Captures everything**: Inputs, outputs, exceptions, latency, token usage
- **Project grouping**: Organize traces by project name
- **Non-blocking**: Never breaks your code, even if tracing fails

## API Reference

### `conte.init(api_key, project_name="default", endpoint=None, enabled=True)`

Initialize the Contexere SDK.

- `api_key`: Your Contexere API key
- `project_name`: Logical project name for grouping traces
- `endpoint`: Custom backend endpoint (optional)
- `enabled`: Enable/disable tracing

### `@conte.op(name=None)`

Decorator to trace function execution.

- `name`: Optional custom name for the span (defaults to function name)

### `conte.instrument_openai(client)`

Wrap an OpenAI client to trace all LLM calls.

- `client`: An OpenAI client instance

Returns an instrumented client that traces all calls.

## License

MIT
