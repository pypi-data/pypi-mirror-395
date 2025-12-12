# BitPulse

![Python Version](https://img.shields.io/badge/python-3.10--3.13-blue)
![License](https://img.shields.io/badge/license-GraphBit%20Framework-orange)
[![PyPI](https://img.shields.io/pypi/v/bitpulse.svg)](https://pypi.org/project/bitpulse/)




Production-grade LLM observability for GraphBit workflows.

- Zero-config automatic tracing for LLM calls and workflows
- Captures prompts, responses, tokens, latency, errors
- Sends trace data to your observability API endpoint

## Project Info

- Python: 3.10–3.13
- License: GraphBit Framework License
- PyPI: [bitpulse](https://pypi.org/project/bitpulse/)
- PRs: Welcome via GitHub pull requests

## Install

```bash
pip install bitpulse
```

Python: 3.10–3.13

## What It Does

BitPulse automatically captures detailed trace data from GraphBit LLM clients and workflows and submits it to your observability endpoint for monitoring, analytics, and debugging.

## Key Features

- Automatic tracing for LLM calls and workflows
- Rich metadata: prompts, responses, tokens, latency, finish reasons, errors
- Tool-call detection for agent workflows
- Works with OpenAI and GraphBit internals
- Type-safe models (Pydantic) and robust async I/O

## Quick Start

```python
import asyncio, os
from graphbit import LlmClient, LlmConfig
from bitpulse import AutoTracer

async def main():
    tracer = await AutoTracer.create()
    cfg = LlmConfig.openai(api_key=os.getenv("OPENAI_API_KEY"), model="gpt-4o-mini")
    client = tracer.wrap_client(LlmClient(cfg), cfg)
    resp = await client.complete_full_async("What is GraphBit?", max_tokens=100)
    results = await tracer.send()
    print("sent:", results["sent"], "failed:", results["failed"])

asyncio.run(main())
```

## Configuration

Set environment variables to configure external endpoints:

```bash
export BITPULSE_TRACING_API_KEY="your-api-key"
export BITPULSE_TRACEABLE_PROJECT="your-project-name"
# optional
export BITPULSE_TRACING_API_URL="https://your-api-endpoint.com/traces"
```

## Links


- GitHub: [InfinitiBit/bitpulse](https://github.com/InfinitiBit/bitpulse)
- Issues: [issue tracker](https://github.com/InfinitiBit/bitpulse/issues)

## License

GraphBit Framework License. See `LICENSE.md` in the repository.

## Trace Data Format Example

Example JSON payload sent to your observability endpoint:

```json
{
    "tracing_api_key": "your-api-key",
    "traceable_project_name": "your-project",
    "run_name": "LlmClient",
    "run_type": "llm",
    "status": "success",
    "input": "Hello, world!",
    "output": "Hi there!",
    "error": null,
    "start_time": "2025-01-01T00:00:00Z",
    "latency": 123.45,
    "tokens": 50,
    "metadata": {
        "model_name": "gpt-4o-mini",
        "provider": "openai",
        "input_tokens": 10,
        "output_tokens": 40,
        "finish_reason": "stop"
    }
}
```

## API Reference

High-level AutoTracer methods:

- `AutoTracer.create()`: Initialize tracer
- `wrap_client(llm_client, llm_config)`: Trace LLM client calls
- `wrap_executor(executor, llm_config)`: Trace workflow execution
- `send()`: Convert and submit captured spans to your endpoint
- `export()`: Export captured traces locally
