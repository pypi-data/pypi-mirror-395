# Judge0 Client

[![PyPI](https://img.shields.io/pypi/v/judge0-client?logo=pypi)](https://pypi.org/project/judge0-client/)
[![Python](https://img.shields.io/badge/python-%3E%3D3.10-blue?logo=python)](https://www.python.org/)
[![CI](https://github.com/Roslovets-Inc/judge0-client/actions/workflows/build_and_release.yml/badge.svg)](https://github.com/Roslovets-Inc/judge0-client/actions/workflows/build_and_release.yml)
[![Docs](https://img.shields.io/badge/docs-online-brightgreen)](https://roslovets-inc.github.io/judge0-client/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Asynchronous Python client for the Judge0 API. Built on top of `httpx` with Pydantic models for requests and responses.

This library helps you submit code to a Judge0 instance and retrieve execution results with clear, typed models and convenient error handling.

## Highlights

- Async, `httpx`-based client
- Pydantic models for request/response validation
- Single-file and multi-file submissions
- Fully automated Base64 handling for text fields and additional files
- Token-based auth header support

## Requirements

- Python 3.10+
- A running Judge0 instance (public or self-hosted)

## Installation

From PyPI:

```bash
pip install judge0-client
```

or

```bash
uv add judge0-client
```

## Quick Start (async)

```python
import asyncio
from judge0_client import Judge0Client, SingleFileSubmission


async def main() -> None:
    # On many instances, language_id=71 corresponds to Python 3
    req = SingleFileSubmission(
        language_id=71,
        source_code='print("Hello, Judge0!")',
    )

    async with Judge0Client(base_url="https://YOUR_JUDGE0_URL.com") as client:
        # 1) Create submission — returns token
        created = await client.create_submission(req)

        # 2) Poll result by token
        detail = await client.get_submission(created.token)
        print("STATUS:", detail.status.description)
        print("STDOUT:", detail.stdout)


if __name__ == "__main__":
    asyncio.run(main())
```

## Documentation

- [Project website](https://roslovets-inc.github.io/judge0-client/)
- [API Reference](https://roslovets-inc.github.io/judge0-client/reference/)

## Usage

### Client parameters

```text
Judge0Client(
    base_url: str,                        # Base URL of your Judge0 instance (no trailing slash)
    timeout: float | httpx.Timeout = 10.0,
    auth_header: str = "X-Auth-Token",   # Custom auth header name if needed
    auth_token: str | SecretStr | None = None,  # Token value passed in the auth header
)
```

Notes:
- The client sets `Accept: application/json` and `Content-Type: application/json` headers.
- If `auth_token` is provided, it will be sent as `{auth_header}: <token>`.

### Single-file submissions

```python
from judge0_client import SingleFileSubmission

req = SingleFileSubmission(
    language_id=71,
    source_code="print('sum =', int(input()) + 2)",
    stdin="40\n",
)
# Then use it with the client as shown in the Quick Start.
```

You can attach additional files that will be zipped and Base64-encoded automatically:

```python
from judge0_client import SingleFileSubmission

req = SingleFileSubmission(
    language_id=71,
    source_code="import helper; print(helper.answer())",
    additional_files={
        "helper.py": "def answer():\n    return 42\n",
    },
)
```

### Multi-file submissions

Use `MultiFileSubmission` (language `id=89` on Judge0 for multi-file/script-based runs). You must provide a `run` script in `additional_files`.

```python
from judge0_client import MultiFileSubmission

req = MultiFileSubmission(
    # language_id is fixed to 89 in this model
    additional_files={
        # Required run script
        "run": "python main.py\n",
        # Your sources
        "main.py": "print('Hello from multi-file!')\n",
    },
)
# Then use it with the client as shown in the Quick Start.
```

### Error handling

Network or HTTP errors raise `Judge0Error` with helpful context:

```python
import asyncio
from judge0_client import Judge0Client, SingleFileSubmission, Judge0Error


async def main() -> None:
    try:
        async with Judge0Client(base_url="https://judge0.ce.pdn.ac.lk") as client:
            req = SingleFileSubmission(language_id=71, source_code="print('hi')")
            created = await client.create_submission(req)
            detail = await client.get_submission(created.token)
            print(detail.stdout)
    except Judge0Error as e:
        # Inspect message, status code, and response body (if any)
        print("Submission failed:", e)


if __name__ == "__main__":
    asyncio.run(main())
```

## Tips

- Language IDs differ across Judge0 instances. Check your instance’s languages endpoint to confirm IDs.
- The client and models automatically handle Base64 encoding for text fields (`source_code`, `stdin`, `expected_output`) and additional files when required by Judge0.

## Contributing

Contributions are welcome! Feel free to open an issue or a pull request.

## License

MIT License — see [LICENSE](LICENSE).
