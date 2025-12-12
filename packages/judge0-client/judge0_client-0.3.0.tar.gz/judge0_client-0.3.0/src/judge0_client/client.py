from typing import Self
import httpx
from pydantic import SecretStr
from .models.base_submission import BaseSubmission
from .models.submission_detail import SubmissionDetail
from .models.submission_response import SubmissionResponse
from .models.workers_response import WorkersResponse
from .models.about_response import AboutResponse
from .utils.exceptions import raise_for_status


class Judge0Client:
    """Asynchronous client for the Judge0 API."""

    base_url: str
    timeout: float | httpx.Timeout
    _auth_header: str
    _auth_token: SecretStr | None
    _verify_certs: bool
    _client: httpx.AsyncClient | None

    def __init__(
            self,
            base_url: str,
            timeout: float | httpx.Timeout = 10.0,
            auth_header: str = "X-Auth-Token",
            auth_token: str | SecretStr | None = None,
            verify_certs: bool = True,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._auth_header = auth_header
        if isinstance(auth_token, SecretStr):
            self._auth_token = auth_token
        else:
            self._auth_token = SecretStr(auth_token) if auth_token else None
        self._client = None

    async def __aenter__(self) -> Self:
        self.open()
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:  # noqa: ANN001
        await self.aclose()

    def open(self) -> None:
        """Initialize the underlying httpx client."""
        headers: dict[str, str] = ({
            "Accept": "application/json",
            "Content-Type": "application/json",
        }) | ({
                  self._auth_header: self._auth_token.get_secret_value()
              } if self._auth_token else {})
        if self._client is None:
            self._client = httpx.AsyncClient(
                base_url=self.base_url,
                timeout=self.timeout,
                headers=headers,
                verify=self._verify_certs,
            )

    async def aclose(self) -> None:
        if self._client:
            await self._client.aclose()
            self._client = None

    @property
    def client(self) -> httpx.AsyncClient:
        if self._client is None:
            raise RuntimeError("Client is not initialized. Use 'async with' or call open().")
        return self._client

    async def create_submission(
            self,
            request: BaseSubmission,
    ) -> SubmissionResponse:
        """Create a submission."""

        resp = await self.client.post(
            "/submissions",
            params={"base64_encoded": "true"},
            json=request.to_body(),
        )
        raise_for_status(resp)
        return SubmissionResponse.from_response(resp)

    async def get_submission(
            self,
            token: str,
    ) -> SubmissionDetail:
        """Get submission result by token."""

        resp = await self.client.get(
            url=f"/submissions/{token}",
            params={"base64_encoded": "true"}
        )
        raise_for_status(resp)
        return SubmissionDetail.from_response(resp).decode_base64()

    async def get_workers(self) -> list[WorkersResponse]:
        """Health-check endpoint: returns workers/queues state."""
        resp = await self.client.get("/workers")
        raise_for_status(resp)
        return WorkersResponse.from_response_list(resp)

    async def get_about(self) -> AboutResponse:
        """Returns general information."""
        resp = await self.client.get("/about")
        raise_for_status(resp)
        return AboutResponse.from_response(resp)

    async def get_isolate(self) -> str:
        """Returns result of isolate --version."""
        resp = await self.client.get("/isolate")
        raise_for_status(resp)
        return resp.text

    async def get_license(self) -> str:
        """Returns a license."""
        resp = await self.client.get("/license")
        raise_for_status(resp)
        return resp.text
