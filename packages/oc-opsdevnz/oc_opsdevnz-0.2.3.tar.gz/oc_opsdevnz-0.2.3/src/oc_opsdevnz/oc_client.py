# src/oc_opsdevnz/oc_client.py
import hashlib
import os
import time
from typing import Any, Dict, Iterable, Literal, Optional

import httpx

from .secrets import get_oc_token

PROD_URL = "https://api.opencollective.com/graphql/v2"
STAGING_URL = "https://api-staging.opencollective.com/graphql/v2"


def _infer_api_url_from_secret_ref(env_var: str = "OC_SECRET_REF") -> str:
    """Peek at the op:// reference to pick staging vs prod automatically."""
    ref = os.getenv(env_var, "")  # e.g. op://startmeup.nz/api-staging.opencollective.com/credential
    if "api-staging.opencollective.com" in ref:
        return STAGING_URL
    if "api.opencollective.com" in ref:
        return PROD_URL
    return STAGING_URL  # default to staging


# Safer default: staging unless explicitly overridden.
DEFAULT_OC_API_URL = os.getenv("OC_API_URL", STAGING_URL)

AuthMode = Literal["personal", "oauth"]
DEBUG = os.getenv("OC_DEBUG", "").lower() in ("1", "true", "yes")


class OpenCollectiveError(Exception):
    """Base error for OpenCollective client issues."""


class GraphQLError(OpenCollectiveError):
    def __init__(self, message: str, *, errors: Optional[list[dict[str, Any]]] = None, status_code: Optional[int] = None):
        super().__init__(message)
        self.errors = errors or []
        self.status_code = status_code


class HTTPRequestError(OpenCollectiveError):
    def __init__(self, message: str, *, status_code: Optional[int] = None):
        super().__init__(message)
        self.status_code = status_code


class TransportError(OpenCollectiveError):
    """Network/transport failure."""


def _redact(text: str, secrets: Iterable[str]) -> str:
    """Best-effort redaction to avoid echoing tokens in errors."""
    if not text:
        return text
    redacted = str(text)
    for s in secrets or []:
        if s:
            redacted = redacted.replace(str(s), "***REDACTED***")
    return redacted


def _token_fingerprint(token: Optional[str]) -> str:
    if not token:
        return ""
    digest = hashlib.sha256(token.encode("utf-8")).hexdigest()
    return digest[:12]


class OpenCollectiveClient:
    def __init__(
        self,
        api_url: Optional[str] = None,
        token: Optional[str] = None,
        app_name: str = "oc_opsdevnz",
        auth_mode: AuthMode = "personal",
        allow_prod: bool = False,
        timeout: float = 20.0,
        transport: Optional[httpx.BaseTransport] = None,
        http_client: Optional[httpx.Client] = None,
        log_requests: bool = DEBUG,
        **kwargs,
    ):
        api_url = api_url or kwargs.pop("base_url", None)
        resolved_api_url = (api_url or DEFAULT_OC_API_URL).rstrip("/")

        if resolved_api_url == PROD_URL.rstrip("/") and not allow_prod:
            raise ValueError("Refusing to use production API without allow_prod=True or OpenCollectiveClient.for_prod().")

        self.api_url = resolved_api_url
        self.token = token or get_oc_token()
        self.app_name = app_name
        self.auth_mode = auth_mode
        self.log_requests = log_requests

        self._client = http_client or httpx.Client(
            timeout=timeout,
            transport=transport,
        )
        self._owns_client = http_client is None

    @classmethod
    def for_prod(cls, token: Optional[str] = None, app_name: str = "oc_opsdevnz-prod", auth_mode: AuthMode = "personal", **kwargs):
        return cls(api_url=PROD_URL, token=token, app_name=app_name, auth_mode=auth_mode, allow_prod=True, **kwargs)

    @classmethod
    def for_staging(cls, token: Optional[str] = None, app_name: str = "oc_opsdevnz-staging", auth_mode: AuthMode = "personal", **kwargs):
        return cls(api_url=STAGING_URL, token=token, app_name=app_name, auth_mode=auth_mode, **kwargs)

    @classmethod
    def from_secret_ref(cls, secret_ref_env: str = "OC_SECRET_REF", app_name: str = "oc_opsdevnz", auth_mode: AuthMode = "personal", **kwargs):
        token = get_oc_token(secret_ref_env=secret_ref_env)
        api_url = _infer_api_url_from_secret_ref(secret_ref_env)
        allow_prod = api_url == PROD_URL
        return cls(api_url=api_url, token=token, app_name=app_name, auth_mode=auth_mode, allow_prod=allow_prod, **kwargs)

    def close(self) -> None:
        if self._owns_client:
            self._client.close()

    def __enter__(self) -> "OpenCollectiveClient":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    def _headers(self) -> Dict[str, str]:
        headers = {
            "User-Agent": self.app_name,
        }
        if self.auth_mode == "personal":
            headers["Personal-Token"] = self.token
        else:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def graphql(self, query: str, variables: Optional[Dict[str, Any]] = None, retry: int = 2, idempotency_key: Optional[str] = None) -> Dict[str, Any]:
        payload = {"query": query, "variables": variables or {}}
        headers = self._headers()
        if idempotency_key:
            headers["Idempotency-Key"] = idempotency_key

        last_err: Optional[Exception] = None
        for attempt in range(retry + 1):
            try:
                resp = self._client.post(self.api_url, json=payload, headers=headers)
                if self.log_requests:
                    print(f"[oc_opsdevnz] POST {self.api_url} status={resp.status_code}")
                resp.raise_for_status()
                data = resp.json()
            except httpx.HTTPStatusError as exc:
                last_err = self._handle_http_error(exc.response)
                if exc.response.status_code >= 500 and attempt < retry:
                    time.sleep(0.5 * (attempt + 1))
                    continue
                break
            except httpx.HTTPError as exc:
                last_err = TransportError(str(exc))
                if attempt < retry:
                    time.sleep(0.5 * (attempt + 1))
                    continue
                break
            else:
                if "errors" in data:
                    errors = data.get("errors") or []
                    message = errors[0].get("message") if errors and isinstance(errors[0], dict) else "GraphQL error"
                    raise GraphQLError(_redact(str(message), [self.token]), errors=errors, status_code=resp.status_code)
                return data.get("data", {})
        raise last_err  # type: ignore

    def _handle_http_error(self, response: httpx.Response) -> HTTPRequestError:
        raw_body = response.text or ""
        redacted_body = _redact(raw_body, [self.token])
        snippet = redacted_body[:400]

        msg = f"HTTP {response.status_code} {self.api_url} — {response.reason_phrase}."
        if DEBUG:
            msg += f" Body: {snippet or '<omitted>'}"
            fp = _token_fingerprint(self.token)
            if fp:
                msg += f" Token fingerprint: {fp}"
        else:
            if response.status_code not in (401, 403):
                msg += f" Body: {snippet or '<omitted>'}"
            else:
                msg += " Body: <omitted>"
        return HTTPRequestError(msg, status_code=response.status_code)

    execute = graphql
