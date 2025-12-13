import functools
import json
import os
import time
import traceback
import uuid
from collections.abc import AsyncIterator, Awaitable, Callable, Iterator
from contextlib import asynccontextmanager, contextmanager
from inspect import iscoroutinefunction
from logging import getLogger
from pathlib import Path
from typing import Any

import httpx
from pydantic import BaseModel
from tqdm import tqdm

logger = getLogger(__name__)

_DEFAULT_TIMEOUT = httpx.Timeout(
    None,
    connect=int(os.getenv("BAYESLINE_APICLIENT_CONNECT_TIMEOUT", "900")),
    read=int(os.getenv("BAYESLINE_APICLIENT_READ_TIMEOUT", "900")),
    write=int(os.getenv("BAYESLINE_APICLIENT_WRITE_TIMEOUT", "900")),
)

MOVED_PERMANENTLY = 301
MOVED_TEMPORARILY = 307


# this address the fun quirk with the AWS ingress controller
# which rewrites http:// urls to https:// and sends a 301 permanent redirect
# The k8s pods internally work on http:// as they should, so if that process
# sends a temporary redirect 307 then then this client will follow it.
# but this redirect has http:// in front of it which then hits the ingress
# controller which rewrites it to https:// and sends a 301 permanent redirect.
# now this becomes a problem when the original request was anything other than a
# GET request because the HTTP protocol prescribes that temporary redirects
# retain their method, but permanent redirects are rewritten to GET.
# this changes the original method from POST to GET and the request fails.
# In this custom transport we always treat permanent redirects as temporary
# to alleviate this issue.
class PermanentToTemporaryRedirectTransport(httpx.HTTPTransport):

    def handle_request(self, request: httpx.Request) -> httpx.Response:
        response = super().handle_request(request)
        if response.status_code == MOVED_PERMANENTLY:
            response.status_code = MOVED_TEMPORARILY

        if "Location" in response.headers:
            location = response.headers["Location"]
            if location.startswith("http://") and request.url.scheme == "https":
                response.headers["Location"] = location.replace("http://", "https://")

        return response


class AsyncPermanentToTemporaryRedirectTransport(httpx.AsyncHTTPTransport):

    async def handle_async_request(self, request: httpx.Request) -> httpx.Response:
        response = await super().handle_async_request(request)
        if response.status_code == MOVED_PERMANENTLY:
            response.status_code = MOVED_TEMPORARILY

        if "Location" in response.headers:
            location = response.headers["Location"]
            if location.startswith("http://") and request.url.scheme == "https":
                response.headers["Location"] = location.replace("http://", "https://")

        return response


def format_bytes(num: float, suffix: str = "B") -> str:
    for unit in ["", "K", "M", "G", "T", "P"]:
        if abs(num) < 1024.0:
            return f"{num:.2f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.2f}E{suffix}"  # For exabyte+


class TqdmFileReader:

    def __init__(self, file_path: Path, chunk_size: int = 1024 * 128):
        self.file_path = file_path
        self.chunk_size = chunk_size
        self.total = file_path.stat().st_size
        self.read_bytes = 0

    def __enter__(self) -> "TqdmFileReader":
        self.pbar = tqdm(
            desc=f"Uploading {self.file_path.name}",
            total=100,
            unit_scale=True,
            bar_format="{l_bar}{bar}| [{elapsed}<{remaining}{postfix}])",
        )
        self.file = self.file_path.open("rb")
        return self

    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None:
        if self.file:
            self.file.close()
        if self.pbar:
            self.pbar.close()

    def read(self, size: int = -1) -> Any:
        chunk = self.file.read(size if size != -1 else self.chunk_size)
        self.read_bytes += len(chunk)
        if chunk:
            update = len(chunk) / self.total * 100
            if update + self.pbar.n > 100:
                update = 100 - self.pbar.n
            self.pbar.update(update)
            self.pbar.set_postfix_str(f"Uploaded {format_bytes(self.read_bytes)}")
        return chunk

    def close(self) -> None:
        self.file.close()

    def __getattr__(self, attr: Any) -> Any:
        # Delegate everything else to the file object
        return getattr(self.file, attr)


class TqdmContentStreamer:

    def __init__(self, data: bytes, chunk_size: int = 1024 * 128):
        self.data = data
        self.chunk_size = chunk_size
        self.total = len(data)
        self.sent = 0

    def __enter__(self) -> "TqdmContentStreamer":
        self.pbar = tqdm(
            desc="Uploading data",
            total=100,
            unit_scale=True,
            bar_format="{l_bar}{bar}| [{elapsed}<{remaining}{postfix}])",
        )
        return self

    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None:
        if self.pbar:
            self.pbar.close()

    def __iter__(self) -> Iterator[bytes]:
        for i in range(0, len(self.data), self.chunk_size):
            chunk = self.data[i : i + self.chunk_size]
            self.sent += len(chunk)
            update = len(chunk) / self.total * 100
            if update + self.pbar.n > 100:
                update = 100 - self.pbar.n
            self.pbar.update(update)
            self.pbar.set_postfix_str(f"Uploaded {format_bytes(self.sent)}")
            yield chunk


class BaseApiClient:

    def __init__(
        self,
        endpoint: str,
        *,
        auth_str: str | None = None,
        auth_type: str | None = None,
        base_path: str | None = None,
        extra_params: dict[str, Any] | None = None,
        submit_exceptions: bool = True,
    ):
        if not (endpoint.strip() == "" or endpoint.strip()[-1] != "/"):
            raise AssertionError("endpoint should not end with a slash")
        if not (not base_path or base_path.strip()[-1] != "/"):
            raise AssertionError("base_path should not end with a slash")
        if not (not base_path or base_path.strip()[0] != "/"):
            raise AssertionError("base_path should not start with a slash")
        self.endpoint = endpoint.strip()
        self.auth_str = auth_str
        self.auth_type = auth_type
        self.base_path = "" if not base_path else base_path.strip()
        self.extra_params = extra_params or {}
        self.submit_exceptions = submit_exceptions

        if self.auth_type and not self.auth_str:
            raise ValueError("if auth type is given an auth_str is required")
        if self.auth_type and self.auth_type not in ["BEARER", "API_KEY", "PRESIGNED"]:
            raise ValueError("auth_type should be one of BEARER, API_KEY or PRESIGNED")

    def make_url(
        self,
        url: str,
        endpoint: bool = True,
        base_path: bool = True,
        params: dict[str, Any] | None = None,
    ) -> str:
        if url.startswith("/"):
            url = url[1:]

        result = []
        if endpoint:
            result.append(self.endpoint)
        if self.base_path and base_path:
            result.append(self.base_path)
        if url:
            result.append(url)

        url = "/".join(result)

        if params:
            url = str(
                httpx.URL(url, params=self._make_params_and_headers(url, params)[0])
            )
        return url

    def _make_params_and_headers(
        self,
        url: str,
        params: dict[str, Any] | None,
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        headers = {"X-Request-ID": uuid.uuid4().hex[:12]}
        params = params or {}
        params.update(self.extra_params)

        # httpx changed its behavior in version 0.28.0 where if params are provided
        # then any query string on the URL will be wiped.
        # hence we append the query string params here
        params.update(httpx.URL(url).params)

        if self.auth_type == "BEARER":
            return params, {"Authorization": f"Bearer {self.auth_str}", **headers}
        elif self.auth_type == "API_KEY":
            return {**params, "api_key": self.auth_str}, headers
        elif self.auth_type == "PRESIGNED":
            return {**params, "presigned_key": self.auth_str}, headers
        else:
            return params, headers

    def __str__(self) -> str:
        endpoint, base_path = self.endpoint, self.base_path
        return (
            f"{self.__class__.__name__}("
            f"endpoint={endpoint}, auth=***, "
            f"auth_type={self.auth_type}, "
            f"base_path={base_path})"
        )

    def __repr__(self) -> str:
        return str(self)


class ApiClient(BaseApiClient):

    def __init__(  # noqa: PLR0913
        self,
        endpoint: str,
        *,
        auth_str: str | None = None,
        auth_type: str | None = None,
        base_path: str | None = None,
        client: httpx.Client | None = None,
        verify: bool = True,
        proxy: str | None = None,
        extra_params: dict[str, Any] | None = None,
        submit_exceptions: bool = True,
    ):
        super().__init__(
            endpoint,
            auth_str=auth_str,
            auth_type=auth_type,
            base_path=base_path,
            extra_params=extra_params,
            submit_exceptions=submit_exceptions,
        )
        self.request_executor = client or httpx.Client(
            follow_redirects=True,
            timeout=_DEFAULT_TIMEOUT,
            verify=verify,
            # Note: we need to explicitly pass all relevant params to the Transport so
            # they can propagate to the underlying httpx HTTPTransport constructor,
            # as the constructor parameters on the httpx Client are not automatically
            # passed through.
            transport=PermanentToTemporaryRedirectTransport(verify=verify, proxy=proxy),
            proxy=proxy,
        )

        if self.auth_type and not self.auth_str:
            raise ValueError("if auth type is given an auth_str is required")
        if self.auth_type and self.auth_type not in ["BEARER", "API_KEY", "PRESIGNED"]:
            raise ValueError("auth_type should be one of BEARER, API_KEY or PRESIGNED")

        self.verify = verify
        self.proxy = proxy

    def __getstate__(self) -> dict[str, Any]:
        return {
            "endpoint": self.endpoint,
            "auth_str": self.auth_str,
            "auth_type": self.auth_type,
            "base_path": self.base_path,
            "verify": self.verify,
            "proxy": self.proxy,
            "extra_params": self.extra_params,
            "submit_exceptions": self.submit_exceptions,
        }

    def __setstate__(self, state: dict[str, Any]) -> None:
        self.__init__(  # type: ignore
            state["endpoint"],
            auth_str=state["auth_str"],
            auth_type=state["auth_type"],
            base_path=state["base_path"],
            verify=state["verify"],
            proxy=state["proxy"],
            extra_params=state["extra_params"],
            submit_exceptions=state["submit_exceptions"],
        )

    def with_base_path(self, base_path: str) -> "ApiClient":
        return ApiClient(
            self.endpoint,
            auth_str=self.auth_str,
            auth_type=self.auth_type,
            base_path=base_path,
            verify=self.verify,
            client=self.request_executor,
            proxy=self.proxy,
            extra_params=self.extra_params,
            submit_exceptions=self.submit_exceptions,
        )

    def append_base_path(self, base_path: str) -> "ApiClient":
        return ApiClient(
            self.endpoint,
            auth_str=self.auth_str,
            auth_type=self.auth_type,
            base_path=self.make_url(base_path, endpoint=False),
            verify=self.verify,
            client=self.request_executor,
            proxy=self.proxy,
            extra_params=self.extra_params,
            submit_exceptions=self.submit_exceptions,
        )

    @contextmanager
    def get_stream(
        self,
        url: str,
        *,
        absolute_url: bool = False,
        params: dict[str, Any] | None = None,
    ) -> Iterator[httpx.Response]:
        params, headers = self._make_params_and_headers(url, params)
        with self.request_executor.stream(
            "get",
            self.make_url(url) if not absolute_url else url,
            params=params,
            headers=headers,
        ) as response:
            yield response

    def get(
        self,
        url: str,
        *,
        absolute_url: bool = False,
        params: dict[str, Any] | None = None,
    ) -> httpx.Response:
        params, headers = self._make_params_and_headers(url, params)

        return self.raise_for_status(self.request_executor.get)(
            self.make_url(url) if not absolute_url else url,
            params=params,
            headers=headers,
        )

    def options(
        self,
        url: str,
        *,
        absolute_url: bool = False,
        params: dict[str, Any] | None = None,
    ) -> httpx.Response:
        params, headers = self._make_params_and_headers(url, params)

        return self.raise_for_status(self.request_executor.options)(
            self.make_url(url) if not absolute_url else url,
            params=params,
            headers=headers,
        )

    def head(
        self,
        url: str,
        *,
        absolute_url: bool = False,
        params: dict[str, Any] | None = None,
    ) -> httpx.Response:
        params, headers = self._make_params_and_headers(url, params)

        return self.raise_for_status(self.request_executor.head)(
            self.make_url(url) if not absolute_url else url,
            params=params,
            headers=headers,
        )

    def delete(
        self,
        url: str,
        *,
        absolute_url: bool = False,
        params: dict[str, Any] | None = None,
    ) -> httpx.Response:
        params, headers = self._make_params_and_headers(url, params)

        return self.raise_for_status(self.request_executor.delete)(
            self.make_url(url) if not absolute_url else url,
            params=params,
            headers=headers,
        )

    def post(
        self,
        url: str,
        body: dict[str, Any] | BaseModel | bytes | TqdmContentStreamer | None,
        files: dict[str, Any] | None = None,
        data: Any | None = None,
        params: dict[str, Any] | None = None,
        absolute_url: bool = False,
    ) -> httpx.Response:
        params, headers = self._make_params_and_headers(url, params)
        if sum(x is not None for x in [body, data, files]) > 1:
            raise ValueError("Only one of json, files or data should be provided")
        elif body is None and data is None and files is None:
            raise ValueError("Either json, files or data should be provided")

        kwargs: dict[str, Any]
        if isinstance(body, BaseModel):
            kwargs = {"data": body.model_dump_json()}
        elif data is not None:
            kwargs = {"data": data}
        elif isinstance(body, dict):
            kwargs = {"json": body}
        elif isinstance(body, bytes):
            kwargs = {"content": body}
        elif isinstance(body, TqdmContentStreamer):
            kwargs = {"content": body}
        else:
            kwargs = {"json": body}

        if files:
            kwargs["files"] = files

        return self.raise_for_status(self.request_executor.post)(
            self.make_url(url) if not absolute_url else url,
            params=params,
            headers=headers,
            **kwargs,
        )

    def put(
        self,
        url: str,
        body: dict[str, Any] | BaseModel | bytes,
        data: Any | None = None,
        params: dict[str, Any] | None = None,
        absolute_url: bool = False,
    ) -> httpx.Response:
        params, headers = self._make_params_and_headers(url, params)
        if body is not None and data is not None:
            raise ValueError("Only one of json or data should be provided")
        elif body is None and data is None:
            raise ValueError("Either json or data should be provided")

        kwargs: dict[str, Any]
        if isinstance(body, BaseModel):
            kwargs = {"data": body.model_dump_json()}
        elif data is not None:
            kwargs = {"data": data}
        elif isinstance(body, dict):
            kwargs = {"json": body}
        elif isinstance(body, bytes):
            kwargs = {"content": body}
        else:
            kwargs = {"json": body}

        return self.raise_for_status(self.request_executor.put)(
            self.make_url(url) if not absolute_url else url,
            params=params,
            headers=headers,
            **kwargs,
        )

    def submit_exception(  # noqa: C901
        self,
        response_or_exception: httpx.Response | Exception | None,
        original_request_id: str,
    ) -> None:
        if (
            isinstance(response_or_exception, httpx.Response)
            and response_or_exception.status_code >= 500
        ):
            exc_str = os.linesep.join(traceback.format_stack())
        elif isinstance(response_or_exception, Exception):
            e = response_or_exception
            exc_str = os.linesep.join(
                traceback.format_exception(type(e), e, e.__traceback__)
            )
        else:
            return

        if self.submit_exceptions:
            try:
                url = self.make_url(
                    f"/v1/maintenance/incidents/{original_request_id}",
                    base_path=False,
                )
                params, headers = self._make_params_and_headers(
                    url, params={"source": "client"}
                )
                self.request_executor.post(
                    url,
                    json={"error": exc_str},
                    params=params,
                    headers=headers,
                )
            except Exception:
                logger.error("Failed to log error to server.", exc_info=True)

        if (
            isinstance(response_or_exception, httpx.Response)
            and response_or_exception.status_code >= 500
        ):
            context_str = ""
            try:
                context = response_or_exception.json()
                context_str = bytes(json.dumps(context, indent=2), "utf-8").decode(
                    "unicode_escape"
                )
            except Exception:
                context = {}
            try:
                response_or_exception.raise_for_status()
            except httpx.HTTPStatusError as e:
                raise httpx.HTTPStatusError(
                    context_str,
                    request=response_or_exception.request,
                    response=response_or_exception,
                ) from e
        elif isinstance(response_or_exception, Exception):
            raise response_or_exception

    def raise_for_status(  # noqa: C901
        self,
        fn: Callable[..., httpx.Response],
    ) -> Callable[..., httpx.Response]:
        @functools.wraps(fn)
        def wrapped(
            *args: Any, **kwargs: Any
        ) -> httpx.Response:  # noqa: ANN002, ANN003
            response: httpx.Response | None = None
            try:
                retry: int = 3
                while retry > 0:
                    try:
                        now = time.time()
                        response = fn(
                            *args,
                            timeout=_DEFAULT_TIMEOUT,
                            **kwargs,
                        )  # typing: ignore
                        break
                    except (httpx.ReadError, httpx.RemoteProtocolError) as e:
                        logger.warning(
                            f"Received read error from server. {str(e)}. Retrying {retry}. "
                            f"Args {args} {kwargs.get('params', {})}",
                        )
                        retry -= 1
                        if retry == 0:
                            raise
                        continue
                    except Exception as e:
                        elapsed = time.time() - now
                        raise Exception(
                            f"exception during request. took {elapsed} seconds. "
                            f"Args {args} {kwargs.get('params', {})}",
                        ) from e
                if response is None:
                    raise AssertionError("response is None")
                return response
            except Exception as e:
                self.submit_exception(
                    e, kwargs.get("headers", {}).get("X-Request-ID", "N/A")
                )
                raise
            finally:
                if response:
                    self.submit_exception(
                        response, kwargs.get("headers", {}).get("X-Request-ID", "N/A")
                    )

        return wrapped


class AsyncApiClient(BaseApiClient):

    def __init__(  # noqa: PLR0913
        self,
        endpoint: str,
        *,
        auth_str: str | None = None,
        auth_type: str | None = None,
        base_path: str | None = None,
        client: httpx.AsyncClient | httpx.Client | None = None,
        verify: bool = True,
        proxy: str | None = None,
        extra_params: dict[str, Any] | None = None,
        submit_exceptions: bool = False,
    ):
        super().__init__(
            endpoint,
            auth_str=auth_str,
            auth_type=auth_type,
            base_path=base_path,
            extra_params=extra_params,
            submit_exceptions=submit_exceptions,
        )
        self.request_executor = client or httpx.AsyncClient(
            follow_redirects=True,
            timeout=_DEFAULT_TIMEOUT,
            verify=verify,
            # Note: we need to explicitly pass all relevant params to the Transport so
            # they can propagate to the underlying httpx HTTPTransport constructor,
            # as the constructor parameters on the httpx Client are not automatically
            # passed through.
            transport=AsyncPermanentToTemporaryRedirectTransport(
                verify=verify, proxy=proxy
            ),
            proxy=proxy,
        )

        if self.auth_type and not self.auth_str:
            raise ValueError("if auth type is given an auth_str is required")
        if self.auth_type and self.auth_type not in ["BEARER", "API_KEY", "PRESIGNED"]:
            raise ValueError("auth_type should be one of BEARER, API_KEY or PRESIGNED")

        self.verify = verify
        self.proxy = proxy

    def __getstate__(self) -> dict[str, Any]:
        return {
            "endpoint": self.endpoint,
            "auth_str": self.auth_str,
            "auth_type": self.auth_type,
            "base_path": self.base_path,
            "verify": self.verify,
            "proxy": self.proxy,
            "extra_params": self.extra_params,
            "submit_exceptions": self.submit_exceptions,
        }

    def __setstate__(self, state: dict[str, Any]) -> None:
        self.__init__(  # type: ignore
            state["endpoint"],
            auth_str=state["auth_str"],
            auth_type=state["auth_type"],
            base_path=state["base_path"],
            verify=state["verify"],
            proxy=state["proxy"],
            extra_params=state["extra_params"],
            submit_exceptions=state["submit_exceptions"],
        )

    def sync(self) -> ApiClient:
        return ApiClient(
            self.endpoint,
            auth_str=self.auth_str,
            auth_type=self.auth_type,
            base_path=self.base_path,
            verify=self.verify,
            proxy=self.proxy,
            extra_params=self.extra_params,
            submit_exceptions=self.submit_exceptions,
        )

    def with_base_path(self, base_path: str) -> "AsyncApiClient":
        return AsyncApiClient(
            self.endpoint,
            auth_str=self.auth_str,
            auth_type=self.auth_type,
            base_path=base_path,
            verify=self.verify,
            client=self.request_executor,
            proxy=self.proxy,
            extra_params=self.extra_params,
            submit_exceptions=self.submit_exceptions,
        )

    def append_base_path(self, base_path: str) -> "AsyncApiClient":
        return AsyncApiClient(
            self.endpoint,
            auth_str=self.auth_str,
            auth_type=self.auth_type,
            base_path=self.make_url(base_path, endpoint=False),
            verify=self.verify,
            client=self.request_executor,
            proxy=self.proxy,
            extra_params=self.extra_params,
            submit_exceptions=self.submit_exceptions,
        )

    @asynccontextmanager
    async def get_stream(
        self,
        url: str,
        *,
        absolute_url: bool = False,
        params: dict[str, Any] | None = None,
    ) -> AsyncIterator[httpx.Response]:
        params, headers = self._make_params_and_headers(url, params)
        if isinstance(self.request_executor, httpx.AsyncClient):
            async with self.request_executor.stream(
                "get",
                self.make_url(url) if not absolute_url else url,
                params=params,
                headers=headers,
            ) as response:
                yield response
        else:
            with self.request_executor.stream(
                "get",
                self.make_url(url) if not absolute_url else url,
                params=params,
                headers=headers,
            ) as response:
                yield response

    async def get(
        self,
        url: str,
        *,
        absolute_url: bool = False,
        params: dict[str, Any] | None = None,
    ) -> httpx.Response:
        params, headers = self._make_params_and_headers(url, params)

        return await self.raise_for_status(self.request_executor.get)(
            self.make_url(url) if not absolute_url else url,
            params=params,
            headers=headers,
        )

    async def options(
        self,
        url: str,
        *,
        absolute_url: bool = False,
        params: dict[str, Any] | None = None,
    ) -> httpx.Response:
        params, headers = self._make_params_and_headers(url, params)

        return await self.raise_for_status(self.request_executor.options)(
            self.make_url(url) if not absolute_url else url,
            params=params,
            headers=headers,
        )

    async def delete(
        self,
        url: str,
        *,
        absolute_url: bool = False,
        params: dict[str, Any] | None = None,
    ) -> httpx.Response:
        params, headers = self._make_params_and_headers(url, params)

        return await self.raise_for_status(self.request_executor.delete)(
            self.make_url(url) if not absolute_url else url,
            params=params,
            headers=headers,
        )

    async def post(
        self,
        url: str,
        body: dict[str, Any] | BaseModel | str | bytes | TqdmContentStreamer | None,
        files: dict[str, Any] | None = None,
        data: Any | None = None,
        params: dict[str, Any] | None = None,
        absolute_url: bool = False,
    ) -> httpx.Response:
        params, headers = self._make_params_and_headers(url, params)
        if sum(x is not None for x in [body, data, files]) > 1:
            raise ValueError("Only one of json, files or data should be provided")
        elif body is None and data is None and files is None:
            raise ValueError("Either json, files or data should be provided")

        kwargs: dict[str, Any]
        if isinstance(body, BaseModel):
            kwargs = {"data": body.model_dump_json()}
        elif data is not None:
            kwargs = {"data": data}
        elif isinstance(body, dict | str):
            kwargs = {"json": body}
        elif isinstance(body, bytes):
            kwargs = {"content": body}
        elif isinstance(body, TqdmContentStreamer):
            kwargs = {"content": body}
        else:
            kwargs = {"json": body}

        if files:
            kwargs["files"] = files

        return await self.raise_for_status(self.request_executor.post)(
            self.make_url(url) if not absolute_url else url,
            params=params,
            headers=headers,
            **kwargs,
        )

    async def put(
        self,
        url: str,
        body: dict[str, Any] | BaseModel | bytes | None,
        data: Any | None = None,
        params: dict[str, Any] | None = None,
        absolute_url: bool = False,
    ) -> httpx.Response:
        params, headers = self._make_params_and_headers(url, params)
        if body is not None and data is not None:
            raise ValueError("Only one of json or data should be provided")
        elif body is None and data is None:
            raise ValueError("Either json or data should be provided")

        kwargs: dict[str, Any]
        if isinstance(body, BaseModel):
            kwargs = {"data": body.model_dump_json()}
        elif data is not None:
            kwargs = {"data": data}
        elif isinstance(body, dict):
            kwargs = {"json": body}
        elif isinstance(body, bytes):
            kwargs = {"content": body}
        else:
            kwargs = {"json": body}

        return await self.raise_for_status(self.request_executor.put)(
            self.make_url(url) if not absolute_url else url,
            params=params,
            headers=headers,
            **kwargs,
        )

    async def submit_exception(  # noqa: C901
        self,
        response_or_exception: (
            httpx.Response | Awaitable[httpx.Response] | Exception | None
        ),
        original_request_id: str,
    ) -> None:

        if (
            isinstance(response_or_exception, httpx.Response)
            and response_or_exception.status_code >= 500
        ):
            exc_str = os.linesep.join(traceback.format_stack())
        elif isinstance(response_or_exception, Exception):
            e = response_or_exception
            exc_str = os.linesep.join(
                traceback.format_exception(type(e), e, e.__traceback__)
            )
        else:
            return

        if self.submit_exceptions:
            try:
                url = self.make_url(
                    f"/v1/maintenance/incidents/{original_request_id}",
                    base_path=False,
                )
                params, headers = self._make_params_and_headers(
                    url, params={"source": "client"}
                )
                log_error_response = self.request_executor.post(
                    url,
                    json={"error": exc_str},
                    params=params,
                    headers=headers,
                )
                if iscoroutinefunction(self.request_executor.post):
                    await log_error_response  # type: ignore
            except Exception:
                logger.error("Failed to log error to server.", exc_info=True)

        if (
            isinstance(response_or_exception, httpx.Response)
            and response_or_exception.status_code >= 500
        ):
            context_str = ""
            try:
                context = response_or_exception.json()
                context_str = bytes(json.dumps(context, indent=2), "utf-8").decode(
                    "unicode_escape"
                )
            except Exception:
                context = {}
            try:
                response_or_exception.raise_for_status()
            except httpx.HTTPStatusError as e:
                raise httpx.HTTPStatusError(
                    context_str,
                    request=response_or_exception.request,
                    response=response_or_exception,
                ) from e
        elif isinstance(response_or_exception, Exception):
            raise response_or_exception

    def raise_for_status(  # noqa: C901
        self,
        fn: Callable[..., Awaitable[httpx.Response]] | Callable[..., httpx.Response],
    ) -> Callable[..., Awaitable[httpx.Response]]:
        @functools.wraps(fn)
        async def wrapped(
            *args: Any, **kwargs: Any
        ) -> httpx.Response:  # noqa: ANN002, ANN003
            response: httpx.Response | None = None
            try:
                retry: int = 3
                while retry > 0:
                    try:
                        now = time.time()
                        response_ = fn(*args, timeout=_DEFAULT_TIMEOUT, **kwargs)
                        response = await response_ if iscoroutinefunction(fn) else response_  # type: ignore
                        break
                    except (httpx.ReadError, httpx.RemoteProtocolError) as e:
                        logger.warning(
                            f"Received read error from server. {str(e)}. Retrying {retry}. "
                            f"Args {args} {kwargs.get('params', {})}",
                        )
                        retry -= 1
                        if retry == 0:
                            raise
                        continue
                    except Exception as e:
                        elapsed = time.time() - now
                        raise Exception(
                            f"exception ({type(e)} during request. "
                            f"took {elapsed} seconds. Args {args} {kwargs.get('params', {})}",
                        ) from e

                if response is None:
                    raise AssertionError("response is None")
                return response  # type: ignore
            except Exception as e:
                await self.submit_exception(
                    e, kwargs.get("headers", {}).get("X-Request-ID", "N/A")
                )
                raise
            finally:
                if response:
                    await self.submit_exception(
                        response, kwargs.get("headers", {}).get("X-Request-ID", "N/A")
                    )

        return wrapped
