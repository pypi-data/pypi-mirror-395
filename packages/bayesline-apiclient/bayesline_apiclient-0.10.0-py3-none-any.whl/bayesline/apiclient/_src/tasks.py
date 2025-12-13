import functools
import io
import json
import time
from pathlib import Path
from typing import Any, Callable, Coroutine, Generic, ParamSpec, Type, TypeVar, cast

import httpx
import polars as pl
from bayesline.api import (
    AsyncTask,
    AsyncTasksApi,
    Task,
    TaskError,
    TaskProgress,
    TasksApi,
    TaskState,
)
from pydantic import BaseModel
from tqdm import tqdm

from bayesline.apiclient import ApiClient, AsyncApiClient

T = TypeVar("T")
P = TypeVar("P", bound=BaseModel)


R = TypeVar("R")
S = ParamSpec("S")


def async_as_blocking(
    task_func: Callable[S, Coroutine[Any, Any, AsyncTask[R]]],
    *,
    timeout: float = -1.0,
    check_interval: float = 0.5,
) -> Callable[
    [Callable[S, Coroutine[Any, Any, R]]], Callable[S, Coroutine[Any, Any, R]]
]:
    """
    Decorates a function that is meant to delegate to its task-based counterpart
    and waits/blocks until the result is ready.
    """

    def decorator(
        func: Callable[S, Coroutine[Any, Any, R]],
    ) -> Callable[S, Coroutine[Any, Any, R]]:
        @functools.wraps(func)
        async def wrapper(self: Any, *args: S.args, **kwargs: S.kwargs) -> R:
            bound_task_func = task_func.__get__(self)
            task: AsyncTask[R] = await bound_task_func(*args, **kwargs)

            try:
                return await task.wait_result(
                    timeout=timeout, check_interval=check_interval
                )
            except KeyboardInterrupt as e:
                await task.cancel()
                raise KeyboardInterrupt(f"Cancelled task {task.task_id}") from e

        return cast(Callable[S, Coroutine[Any, Any, R]], wrapper)

    return decorator


def as_blocking(
    task_func: Callable[S, Task[R]],
    *,
    timeout: float = -1.0,
    check_interval: float = 0.5,
) -> Callable[[Callable[S, R]], Callable[S, R]]:
    """
    Decorates a function that is meant to delegate to its task-based counterpart
    and waits/blocks until the result is ready.
    """

    def decorator(
        func: Callable[S, R],
    ) -> Callable[S, R]:
        @functools.wraps(func)
        def wrapper(self: Any, *args: S.args, **kwargs: S.kwargs) -> R:
            bound_task_func = task_func.__get__(self)
            task: Task[R] = bound_task_func(*args, **kwargs)

            try:
                return task.wait_result(timeout=timeout, check_interval=check_interval)
            except KeyboardInterrupt as e:
                task.cancel()
                raise KeyboardInterrupt(f"Cancelled task {task.task_id}") from e

        return cast(Callable[S, R], wrapper)

    return decorator


def _raise_for_status(  # noqa: C901
    response: httpx.Response, exc_types: list[Type]
) -> None:
    if response.status_code in {200, 202}:
        return

    def _unescape(s: str) -> str:
        try:
            return json.loads(s)
        except json.JSONDecodeError:
            return s

    exc: Exception | None = None
    task_error: TaskError | None = None
    try:
        details = response.json()["detail"]
        stacktrace = details.get("stacktrace", "")
        task_error = TaskError(stacktrace)

        if "type" in details:
            if details["type"] == "KeyError":
                exc = KeyError(_unescape(details["message"]))
            elif details["type"] == "ValueError":
                exc = ValueError(_unescape(details["message"]))

            for exc_type in exc_types:
                if exc_type.__name__ == details["type"]:
                    exc = exc_type(_unescape(details["message"]))
    except (KeyError, ValueError, json.JSONDecodeError):
        # If we can't parse the response, fall back to default behavior
        pass

    if exc and task_error:
        raise exc from task_error
    elif task_error:
        raise task_error

    response.raise_for_status()


class TaskClient(Task[T], Generic[T]):

    def __init__(
        self,
        client: ApiClient,
        task_id: str,
        tqdm_progress: bool = False,
        exc_types: list[Type] | None = None,
    ) -> None:
        self._api_client = client
        self._task_id = task_id
        self._tqdm_progress = tqdm_progress
        self._exc_types = exc_types or []

    def raise_for_status(self, response: httpx.Response) -> None:
        _raise_for_status(response, self._exc_types)

    @property
    def task_id(self) -> str:
        return self._task_id

    def get_progress(self) -> TaskProgress:
        response = self._api_client.get(f"{self._task_id}/progress")
        if response.status_code == 404:
            raise KeyError(f"Task {self.task_id} not found")
        return TaskProgress.model_validate(response.json())

    def is_ready(self) -> bool:
        response = self._api_client.get(f"{self._task_id}/ready")
        if response.status_code == 404:
            raise KeyError(f"Task {self.task_id} not found")
        return response.json()

    def wait_result(self, timeout: float = -1.0, check_interval: float = 1.0) -> T:
        start_time = time.time()

        pbar = None
        if self._tqdm_progress:
            pbar = tqdm(total=100)

        try:
            self._update_progress(self._tqdm_progress, pbar)
            while not self.is_ready():
                time.sleep(check_interval)
                self._update_progress(self._tqdm_progress, pbar)
                if 0 < timeout < time.time() - start_time:
                    raise TaskError(
                        f"Task {self.task_id} time out after {timeout} seconds."
                    )
            if pbar is not None:
                pbar.update(80 - pbar.n)
                pbar.set_postfix_str("Transferring data")
            return self.get_result()
        finally:
            if pbar is not None:
                pbar.update(100 - pbar.n)
                pbar.set_postfix_str("Done")
                pbar.close()

    def wait_ready(self, timeout: float = -1.0, check_interval: float = 1.0) -> None:
        start_time = time.time()

        pbar = None
        if self._tqdm_progress:
            pbar = tqdm(total=100)

        try:
            self._update_progress(self._tqdm_progress, pbar)
            while not self.is_ready():
                time.sleep(check_interval)
                self._update_progress(self._tqdm_progress, pbar)
                if 0 < timeout < time.time() - start_time:
                    raise TaskError(
                        f"Task {self.task_id} time out after {timeout} seconds."
                    )
            if pbar is not None:
                pbar.update(80 - pbar.n)
                pbar.set_postfix_str("Transferring data")
        finally:
            if pbar is not None:
                pbar.update(100 - pbar.n)
                pbar.set_postfix_str("Done")
                pbar.close()

    def _update_progress(self, progress: bool, pbar: tqdm | None) -> None:
        if progress:
            task_progress = self.get_progress()
            if pbar is not None:
                pbar.update(int(task_progress.last_progress * 0.75 - pbar.n))
                postfix = task_progress.last_message.ljust(25)
                postfix += f" - {task_progress.last_context}"
                pbar.set_postfix_str(postfix)

    def cancel(self) -> None:
        self._api_client.delete(self._task_id)


class AsyncTaskClient(AsyncTask[T], Generic[T]):

    def __init__(
        self,
        client: AsyncApiClient,
        task_id: str,
        tqdm_progress: bool = False,
        exc_types: list[Type] | None = None,
    ) -> None:
        self._api_client = client
        self._task_id = task_id
        self._tqdm_progress = tqdm_progress
        self._exc_types = exc_types or []

    def raise_for_status(self, response: httpx.Response) -> None:
        _raise_for_status(response, self._exc_types)

    @property
    def task_id(self) -> str:
        return self._task_id

    async def get_progress(self) -> TaskProgress:
        response = await self._api_client.get(f"{self._task_id}/progress")
        if response.status_code == 404:
            raise KeyError(f"Task {self.task_id} not found")
        return TaskProgress.model_validate(response.json())

    async def is_ready(self) -> bool:
        response = await self._api_client.get(f"{self._task_id}/ready")
        if response.status_code == 404:
            raise KeyError(f"Task {self.task_id} not found")
        return response.json()

    async def wait_result(
        self, timeout: float = -1.0, check_interval: float = 1.0
    ) -> T:
        start_time = time.time()

        pbar = None
        if self._tqdm_progress:
            pbar = tqdm(total=100)

        try:
            await self._update_progress(self._tqdm_progress, pbar)
            while not await self.is_ready():
                time.sleep(check_interval)
                await self._update_progress(self._tqdm_progress, pbar)
                if 0 < timeout < time.time() - start_time:
                    raise TaskError(
                        f"Task {self.task_id} time out after {timeout} seconds."
                    )
            if pbar is not None:
                pbar.update(80 - pbar.n)
                pbar.set_postfix_str("Transferring data")
            return await self.get_result()
        finally:
            if pbar is not None:
                pbar.update(100 - pbar.n)
                pbar.set_postfix_str("Done")
                pbar.close()

    async def wait_ready(
        self, timeout: float = -1.0, check_interval: float = 1.0
    ) -> None:
        start_time = time.time()

        pbar = None
        if self._tqdm_progress:
            pbar = tqdm(total=100)

        try:
            await self._update_progress(self._tqdm_progress, pbar)
            while not await self.is_ready():
                time.sleep(check_interval)
                await self._update_progress(self._tqdm_progress, pbar)
                if 0 < timeout < time.time() - start_time:
                    raise TaskError(
                        f"Task {self.task_id} time out after {timeout} seconds."
                    )
            if pbar is not None:
                pbar.update(80 - pbar.n)
                pbar.set_postfix_str("Transferring data")
        finally:
            if pbar is not None:
                pbar.update(100 - pbar.n)
                pbar.set_postfix_str("Done")
                pbar.close()

    async def _update_progress(self, progress: bool, pbar: tqdm | None) -> None:
        if progress:
            task_progress = await self.get_progress()
            if pbar is not None:
                pbar.update(int(task_progress.last_progress * 0.75 - pbar.n))
                postfix = task_progress.last_message.ljust(25)
                postfix += f" - {task_progress.last_context}"
                pbar.set_postfix_str(postfix)

    async def cancel(self) -> None:
        await self._api_client.delete(self._task_id)


class DataFrameTaskClient(TaskClient[pl.DataFrame]):

    def get_result(self) -> pl.DataFrame:
        response = self._api_client.get(
            f"{self._task_id}/result", params={"type": "dataframe"}
        )

        if response.status_code == 404:
            raise KeyError(f"Task {self.task_id} not found")
        elif response.status_code == 206:
            dfs = []
            for path in response.json():
                response = self._api_client.get(
                    f"{self._task_id}/result",
                    params={"type": "dataframe", "path": path},
                )
                dfs.append(pl.read_parquet(io.BytesIO(response.content)))
            return pl.concat(dfs)
        else:
            self.raise_for_status(response)
            return pl.read_parquet(io.BytesIO(response.content))


class DataFrameDictTaskClient(TaskClient[dict[str, pl.DataFrame]]):

    def get_result(self) -> dict[str, pl.DataFrame]:
        response = self._api_client.get(
            f"{self._task_id}/result", params={"type": "dataframe"}
        )

        if response.status_code == 404:
            raise KeyError(f"Task {self.task_id} not found")
        elif response.status_code == 206:
            dfs = {}
            for path in response.json():
                response = self._api_client.get(
                    f"{self._task_id}/result",
                    params={"type": "dataframe", "path": path},
                )
                name = response.headers["Content-Disposition"].split("filename=")[1]
                name = name.split(".")[0]
                dfs[name] = pl.read_parquet(io.BytesIO(response.content))
            return dfs
        elif response.status_code == 204:
            return {}
        else:
            self.raise_for_status(response)
            name = response.headers["Content-Disposition"].split("filename=")[1]
            name = name.split(".")[0]
            return {name: pl.read_parquet(io.BytesIO(response.content))}


class ListTaskClient(TaskClient[list[Any]]):

    def get_result(self) -> list[Any]:
        response = self._api_client.get(
            f"{self._task_id}/result", params={"type": "json-list"}
        )
        if response.status_code == 404:
            raise KeyError(f"Task {self.task_id} not found")
        self.raise_for_status(response)
        return response.json()


class LazyFrameTaskClient(TaskClient[pl.LazyFrame]):

    def __init__(
        self,
        client: ApiClient,
        task_id: str,
        tqdm_progress: bool = False,
        exc_types: list[Type] | None = None,
        out_path: Path | None = None,
    ) -> None:
        super().__init__(client, task_id, tqdm_progress, exc_types)

        self._out_path = out_path
        if self._out_path is not None and "{i}" not in self._out_path.name:
            raise ValueError("out_path must contain {i} to be used for lazy frames")

    def get_result(self) -> pl.LazyFrame:
        if self._out_path is not None:
            return self._get_result_on_disk()
        else:
            return self._get_result_in_memory()

    def _get_result_on_disk(self) -> pl.LazyFrame:
        if self._out_path is None:
            raise ValueError("out_path is required for lazy frames")

        with self._api_client.get_stream(
            f"{self._task_id}/result", params={"type": "dataframe"}
        ) as response:
            if response.status_code == 404:
                raise KeyError(f"Task {self.task_id} not found")
            elif response.status_code == 206:
                dfs: list[pl.LazyFrame] = []
                for i, path in enumerate(response.json()):
                    with self._api_client.get_stream(
                        f"{self._task_id}/result",
                        params={"type": "dataframe", "path": path},
                    ) as path_response:
                        out_path = self._out_path.with_name(
                            self._out_path.name.replace("{i}", str(i))
                        )
                        if out_path.exists():
                            raise FileExistsError(
                                f"File {out_path} already exists. Please delete all files of "
                                f"the pattern {self._out_path} before running this task."
                            )
                        with open(out_path, "wb") as f:
                            for chunk in path_response.iter_bytes():
                                f.write(chunk)
                    dfs.append(pl.scan_parquet(out_path))
                return pl.concat(dfs)
            else:
                self.raise_for_status(response)
                out_path = self._out_path.with_name(
                    self._out_path.name.replace("{i}", "0")
                )
                if out_path.exists():
                    raise FileExistsError(
                        f"File {out_path} already exists. Please delete all files of "
                        f"the pattern {self._out_path} before running this task."
                    )
                with open(out_path, "wb") as f:
                    for chunk in response.iter_bytes():
                        f.write(chunk)
                return pl.scan_parquet(out_path)

    def _get_result_in_memory(self) -> pl.LazyFrame:
        response = self._api_client.get(
            f"{self._task_id}/result", params={"type": "dataframe"}
        )

        if response.status_code == 404:
            raise KeyError(f"Task {self.task_id} not found")
        elif response.status_code == 206:
            dfs = []
            for path in response.json():
                response = self._api_client.get(
                    f"{self._task_id}/result",
                    params={"type": "dataframe", "path": path},
                )
                dfs.append(pl.read_parquet(io.BytesIO(response.content)).lazy())
            return pl.concat(dfs)
        else:
            self.raise_for_status(response)
            return pl.read_parquet(io.BytesIO(response.content)).lazy()


class PydanticTaskClient(TaskClient[P], Generic[P]):

    def __init__(
        self,
        model_class: type[P],
        client: ApiClient,
        task_id: str,
        tqdm_progress: bool = False,
        exc_types: list[Type] | None = None,
    ) -> None:
        super().__init__(client, task_id, tqdm_progress, exc_types)
        self._model_class = model_class

    def get_result(self) -> P:
        response = self._api_client.get(
            f"{self._task_id}/result", params={"type": "json"}
        )
        if response.status_code == 404:
            raise KeyError(f"Task {self.task_id} not found")
        self.raise_for_status(response)
        return self._model_class.model_validate(response.json())


class AsyncDataFrameTaskClient(AsyncTaskClient[pl.DataFrame]):

    async def get_result(self) -> pl.DataFrame:
        response = await self._api_client.get(
            f"{self._task_id}/result", params={"type": "dataframe"}
        )
        if response.status_code == 404:
            raise KeyError(f"Task {self.task_id} not found")
        elif response.status_code == 206:
            dfs = []
            for path in response.json():
                response = await self._api_client.get(
                    f"{self._task_id}/result",
                    params={"type": "dataframe", "path": path},
                )
                dfs.append(pl.read_parquet(io.BytesIO(response.content)))
            return pl.concat(dfs)
        else:
            self.raise_for_status(response)
            return pl.read_parquet(io.BytesIO(response.content))


class AsyncDataFrameDictTaskClient(AsyncTaskClient[dict[str, pl.DataFrame]]):

    async def get_result(self) -> dict[str, pl.DataFrame]:
        response = await self._api_client.get(
            f"{self._task_id}/result", params={"type": "dataframe"}
        )

        if response.status_code == 404:
            raise KeyError(f"Task {self.task_id} not found")
        elif response.status_code == 206:
            dfs = {}
            for path in response.json():
                response = await self._api_client.get(
                    f"{self._task_id}/result",
                    params={"type": "dataframe", "path": path},
                )
                name = response.headers["Content-Disposition"].split("filename=")[1]
                name = name.split(".")[0]
                dfs[name] = pl.read_parquet(io.BytesIO(response.content))
            return dfs
        elif response.status_code == 204:
            return {}
        else:
            self.raise_for_status(response)
            name = response.headers["Content-Disposition"].split("filename=")[1]
            name = name.split(".")[0]
            return {name: pl.read_parquet(io.BytesIO(response.content))}


class AsyncListTaskClient(AsyncTaskClient[list[Any]]):

    async def get_result(self) -> list[Any]:
        response = await self._api_client.get(
            f"{self._task_id}/result", params={"type": "json-list"}
        )
        if response.status_code == 404:
            raise KeyError(f"Task {self.task_id} not found")
        self.raise_for_status(response)
        return response.json()


class AsyncLazyFrameTaskClient(AsyncTaskClient[pl.LazyFrame]):

    def __init__(
        self,
        client: AsyncApiClient,
        task_id: str,
        tqdm_progress: bool = False,
        exc_types: list[Type] | None = None,
        out_path: Path | None = None,
    ) -> None:
        super().__init__(client, task_id, tqdm_progress, exc_types)

        self._out_path = out_path
        if self._out_path is not None and "{i}" not in self._out_path.name:
            raise ValueError("out_path must contain {i} to be used for lazy frames")

    async def get_result(self) -> pl.LazyFrame:
        if self._out_path is not None:
            return await self._get_result_on_disk()
        else:
            return await self._get_result_in_memory()

    async def _get_result_on_disk(self) -> pl.LazyFrame:
        if self._out_path is None:
            raise ValueError("out_path is required for lazy frames")

        async with self._api_client.get_stream(
            f"{self._task_id}/result", params={"type": "dataframe"}
        ) as response:
            if response.status_code == 404:
                raise KeyError(f"Task {self.task_id} not found")
            elif response.status_code == 206:
                dfs = []
                for i, path in enumerate(response.json()):
                    async with self._api_client.get_stream(
                        f"{self._task_id}/result",
                        params={"type": "dataframe", "path": path},
                    ) as path_response:
                        out_path = self._out_path.with_name(
                            self._out_path.name.replace("{i}", str(i))
                        )
                        if out_path.exists():
                            raise FileExistsError(
                                f"File {out_path} already exists. Please delete all files of "
                                f"the pattern {self._out_path} before running this task."
                            )
                        with open(out_path, "wb") as f:
                            async for chunk in path_response.aiter_bytes():
                                f.write(chunk)
                    dfs.append(pl.scan_parquet(out_path))
                return pl.concat(dfs)
            else:
                self.raise_for_status(response)
                out_path = self._out_path.with_name(
                    self._out_path.name.replace("{i}", "0")
                )
                if out_path.exists():
                    raise FileExistsError(
                        f"File {out_path} already exists. Please delete all files of "
                        f"the pattern {self._out_path} before running this task."
                    )
                with open(out_path, "wb") as f:
                    async for chunk in response.aiter_bytes():
                        f.write(chunk)
                return pl.scan_parquet(out_path)

    async def _get_result_in_memory(self) -> pl.LazyFrame:
        response = await self._api_client.get(
            f"{self._task_id}/result", params={"type": "dataframe"}
        )

        if response.status_code == 404:
            raise KeyError(f"Task {self.task_id} not found")
        elif response.status_code == 206:
            dfs = []
            for path in response.json():
                response = await self._api_client.get(
                    f"{self._task_id}/result",
                    params={"type": "dataframe", "path": path},
                )
                dfs.append(pl.read_parquet(io.BytesIO(response.content)).lazy())
            return pl.concat(dfs)
        else:
            self.raise_for_status(response)
            return pl.read_parquet(io.BytesIO(response.content)).lazy()


class AsyncPydanticTaskClient(AsyncTaskClient[P], Generic[P]):

    def __init__(
        self,
        model_class: type[P],
        client: AsyncApiClient,
        task_id: str,
        tqdm_progress: bool = False,
        exc_types: list[Type] | None = None,
    ) -> None:
        super().__init__(client, task_id, tqdm_progress, exc_types)
        self._model_class = model_class

    async def get_result(self) -> P:
        response = await self._api_client.get(
            f"{self._task_id}/result", params={"type": "json"}
        )
        if response.status_code == 404:
            raise KeyError(f"Task {self.task_id} not found")
        self.raise_for_status(response)
        return self._model_class.model_validate(response.json())


class ResolvedObjectTaskClient(Task[T], Generic[T]):

    def __init__(self, result: T) -> None:
        self._result = result

    @property
    def task_id(self) -> str:
        raise NotImplementedError()

    def get_progress(self) -> TaskProgress:
        return TaskProgress(
            state=TaskState.COMPLETED, last_progress=100, last_message="Done"
        )

    def is_ready(self) -> bool:
        return True

    def get_result(self) -> T:
        return self._result

    def wait_result(self, timeout: float = -1.0, check_interval: float = 1.0) -> T:
        del timeout, check_interval
        return self.get_result()

    def wait_ready(self, timeout: float = -1.0, check_interval: float = 1.0) -> None:
        del timeout, check_interval

    def cancel(self) -> None:
        pass


class AsyncResolvedObjectTaskClient(AsyncTask[T], Generic[T]):

    def __init__(self, result: T) -> None:
        self._result = result

    @property
    def task_id(self) -> str:
        raise NotImplementedError()

    async def get_progress(self) -> TaskProgress:
        return TaskProgress(
            state=TaskState.COMPLETED, last_progress=100, last_message="Done"
        )

    async def is_ready(self) -> bool:
        return True

    async def get_result(self) -> T:
        return self._result

    async def wait_result(
        self, timeout: float = -1.0, check_interval: float = 1.0
    ) -> T:
        del timeout, check_interval
        return await self.get_result()

    async def wait_ready(
        self, timeout: float = -1.0, check_interval: float = 1.0
    ) -> None:
        del timeout, check_interval

    async def cancel(self) -> None:
        pass


class TasksClient(TasksApi):

    def __init__(self, client: ApiClient) -> None:
        self.api_client = client.append_base_path("tasks")

    def get_task_progress(self, task_id: str) -> TaskProgress:
        response = self.api_client.get(f"{task_id}/progress")
        if response.status_code == 404:
            raise KeyError(f"Task {task_id} not found")
        return TaskProgress.model_validate(response.json())


class AsyncTasksClient(AsyncTasksApi):

    def __init__(self, client: AsyncApiClient) -> None:
        self.api_client = client.append_base_path("tasks")

    async def get_task_progress(self, task_id: str) -> TaskProgress:
        response = await self.api_client.get(f"{task_id}/progress")
        return TaskProgress.model_validate(response.json())
