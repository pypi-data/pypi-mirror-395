from typing import Any
import httpx


class Judge0Error(Exception):
    """Generic Judge0 client exception."""


def raise_for_status(resp: httpx.Response) -> None:
    try:
        resp.raise_for_status()
    except httpx.HTTPStatusError as e:
        body: str | dict[str, Any]
        try:
            body = e.response.json()
        except Exception:
            body = e.response.text
        raise Judge0Error(f"HTTP {e.response.status_code}: {body}") from e
