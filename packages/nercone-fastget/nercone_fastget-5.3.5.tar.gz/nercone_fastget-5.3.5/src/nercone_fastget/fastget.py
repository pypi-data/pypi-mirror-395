import os
import asyncio
from curl_cffi import aio, CurlError
from curl_cffi.const import HTTPVersion
from importlib.metadata import version
from typing import Union, Optional, Dict, Any, TypeVar, Awaitable, List

try:
    VERSION = version("nercone-fastget")
except Exception:
    VERSION = "0.0.0"

DEFAULT_CHUNK_SIZE = 1024 * 64
DEFAULT_TIMEOUT = 30.0
DEFAULT_RETRIES = 3
DEFAULT_THREADS = 8

T = TypeVar("T")

class FastGetError(Exception):
    pass

class ProgressCallback:
    async def on_start(self, total_size: int, threads: int, http_version: str, final_url: str, verify_was_enabled: bool) -> None: pass
    async def on_update(self, worker_id: int, loaded: int) -> None: pass
    async def on_complete(self) -> None: pass
    async def on_merge_start(self, total_size: int) -> None: pass
    async def on_merge_update(self, loaded: int) -> None: pass
    async def on_merge_complete(self) -> None: pass
    async def on_error(self, msg: str) -> None: pass

class FastGetResponse:
    def __init__(self, original: aio.AsyncClient.Response, content: bytes):
        self._r = original
        self.content = content
        self.url = str(original.url)
        self.status_code = original.status_code
        self.headers = original.headers
        self.http_version = original.http_version

    @property
    def text(self) -> str:
        return self.content.decode(self._r.encoding or 'utf-8', errors='replace')

    def json(self, **kwargs) -> Any:
        return self._r.json(**kwargs)

class FastGetSession:
    def __init__(self, max_threads: int = DEFAULT_THREADS, http1: bool = True, http2: bool = True, http3: bool = True, verify: bool = True, follow_redirects: bool = True):
        self.max_threads = max_threads

        self.http_versions_to_try = []
        if http3:
            self.http_versions_to_try.append(HTTPVersion.V3)
        if http2:
            self.http_versions_to_try.append(HTTPVersion.V2)
        if http1:
            self.http_versions_to_try.append(HTTPVersion.V1_1)

        if not self.http_versions_to_try:
            raise ValueError("At least one of HTTP/1, HTTP/2, or HTTP/3 must be enabled.")

        self.client_args = {
            "verify": verify,
            "follow_redirects": follow_redirects,
            "timeout": DEFAULT_TIMEOUT,
        }

    async def _get_info(self, client: aio.AsyncClient, method: str, url: str, **kwargs) -> tuple[int, bool, bool, Optional[aio.AsyncClient.Response]]:
        headers = kwargs.get("headers", {}).copy()
        headers["User-Agent"] = f'FastGet/{VERSION} (Info)'
        if method.upper() != "GET":
            return 0, False, False, None

        try:
            head_resp = await client.head(url, headers=headers)
            head_resp.raise_for_status()
            size = int(head_resp.headers.get("content-length", 0))
            accept_ranges = head_resp.headers.get("accept-ranges", "").lower() == "bytes"
            reject_fg = head_resp.headers.get("rejectfastget", "").lower() in ["true", "1", "yes"]
            return size, accept_ranges, reject_fg, head_resp

        except CurlError:
            try:
                get_headers = headers.copy()
                get_headers["Range"] = "bytes=0-0"
                get_resp = await client.get(url, headers=get_headers)
                get_resp.raise_for_status()
                size_str = "0"
                if get_resp.status_code == 206 and "content-range" in get_resp.headers:
                    content_range = get_resp.headers["content-range"]
                    if '/' in content_range:
                        size_str = content_range.split('/')[-1]
                else:
                    size_str = get_resp.headers.get("content-length", "0")
                
                size = int(size_str) if size_str.isdigit() else 0
                accept_ranges = get_resp.headers.get("accept-ranges", "").lower() == "bytes" or get_resp.status_code == 206
                reject_fg = get_resp.headers.get("rejectfastget", "").lower() in ["true", "1", "yes"]
                return size, accept_ranges, reject_fg, get_resp
            except CurlError:
                raise

    async def _download_worker_to_storage(self, client: aio.AsyncClient, method: str, url: str, start: int, end: int, worker_id: int, total_threads: int, part_path: str, callback: ProgressCallback, **kwargs) -> None:
        headers = kwargs.get("headers", {}).copy()
        headers["Range"] = f"bytes={start}-{end}"
        headers["User-Agent"] = f'FastGet/{VERSION} (Worker {worker_id+1}/{total_threads})'
        kwargs["headers"] = headers
        for attempt in range(DEFAULT_RETRIES):
            try:
                response = await client.request(method, url, **kwargs)
                response.raise_for_status()
                with open(part_path, "wb") as f:
                    async for chunk in response.aiter_content(chunk_size=DEFAULT_CHUNK_SIZE):
                        f.write(chunk)
                        await callback.on_update(worker_id, len(chunk))
                return
            except CurlError as e:
                if attempt == DEFAULT_RETRIES - 1:
                    await callback.on_error(f"Worker {worker_id+1} failed: {e}")
                    raise
                await asyncio.sleep(1)

    async def _download_worker_to_memory(self, client: aio.AsyncClient, method: str, url: str, start: int, end: int, worker_id: int, total_threads: int, callback: ProgressCallback, **kwargs) -> bytes:
        headers = kwargs.get("headers", {}).copy()
        headers["Range"] = f"bytes={start}-{end}"
        headers["User-Agent"] = f'FastGet/{VERSION} (Worker {worker_id+1}/{total_threads})'
        kwargs["headers"] = headers
        part_buffer = bytearray()
        for attempt in range(DEFAULT_RETRIES):
            try:
                response = await client.request(method, url, **kwargs)
                response.raise_for_status()
                async for chunk in response.aiter_content(chunk_size=DEFAULT_CHUNK_SIZE):
                    part_buffer.extend(chunk)
                    await callback.on_update(worker_id, len(chunk))
                return bytes(part_buffer)
            except CurlError as e:
                if attempt == DEFAULT_RETRIES - 1:
                    await callback.on_error(f"Worker {worker_id+1} failed: {e}")
                    raise
                part_buffer.clear()
                await asyncio.sleep(1)
        return b""

    async def process(self, method: str, url: str, output: Optional[str] = None, data: Any = None, json: Any = None, params: Any = None, headers: Dict = None, callback: Optional[ProgressCallback] = None, strategy: str = 'storage') -> Union[str, FastGetResponse]:
        callback = callback or ProgressCallback()
        headers = headers or {}
        req_kwargs = {"data": data, "json": json, "params": params, "headers": headers}

        client = None
        last_error = None
        info_result = None

        for version in self.http_versions_to_try:
            client_args = self.client_args.copy()
            client_args["http_version"] = version
            temp_client = aio.AsyncClient(**client_args)
            try:
                info_result = await self._get_info(temp_client, method, url, **req_kwargs)
                client = temp_client
                break
            except CurlError as e:
                last_error = e
                await temp_client.close()
                is_last_attempt = (version == self.http_versions_to_try[-1])
                if not is_last_attempt:
                    await callback.on_error(f"Request with {version.name} failed. Trying fallback...")

        if not client:
            await callback.on_error(f"All HTTP versions failed. Last error: {last_error}")
            raise FastGetError(f"Failed to connect to {url} with all tried HTTP versions.") from last_error

        try:
            file_size, is_resumable, is_rejected, info_response = info_result

            if method.upper() == "GET" and not info_response:
                raise FastGetError(f"Failed to retrieve file information from {url}")

            use_parallel = (method.upper() == "GET" and is_resumable and not is_rejected and file_size > 0 and output is not None and self.max_threads > 1)
            threads = self.max_threads if use_parallel else 1
            http_version = info_response.http_version if info_response else "UNKNOWN"
            final_url = str(info_response.url) if info_response else url
            verify_was_enabled = self.client_args.get("verify", True)

            await callback.on_start(file_size, threads, http_version, final_url, verify_was_enabled)
            if output:
                out_dir = os.path.dirname(output)
                if out_dir: os.makedirs(out_dir, exist_ok=True)
                if use_parallel:
                    part_size = file_size // threads
                    tasks = []
                    if strategy == 'memory':
                        for i in range(threads):
                            start = i * part_size
                            end = file_size - 1 if i == threads - 1 else start + part_size - 1
                            tasks.append(self._download_worker_to_memory(client, method, url, start, end, i, threads, callback, **req_kwargs))
                        parts_in_memory: List[bytes] = await asyncio.gather(*tasks)
                        await callback.on_merge_start(file_size)
                        with open(output, "wb") as outfile:
                            for part_data in parts_in_memory:
                                outfile.write(part_data)
                                await callback.on_merge_update(len(part_data))
                        await callback.on_merge_complete()
                    else:
                        part_files = []
                        for i in range(threads):
                            start = i * part_size
                            end = file_size - 1 if i == threads - 1 else start + part_size - 1
                            part_path = f"{output}.part{i}"
                            part_files.append(part_path)
                            tasks.append(self._download_worker_to_storage(client, method, url, start, end, i, threads, part_path, callback, **req_kwargs))
                        await asyncio.gather(*tasks)
                        await callback.on_merge_start(file_size)
                        with open(output, "wb") as outfile:
                            for part_file in part_files:
                                try:
                                    with open(part_file, "rb") as infile:
                                        while chunk := infile.read(DEFAULT_CHUNK_SIZE):
                                            outfile.write(chunk)
                                            await callback.on_merge_update(len(chunk))
                                    os.remove(part_file)
                                except FileNotFoundError:
                                    await callback.on_error(f"Part file {part_file} not found during merge.")
                        await callback.on_merge_complete()
                else:
                    headers["User-Agent"] = f'FastGet/{VERSION} (Single-Thread)'
                    response = await client.request(method, url, **req_kwargs)
                    response.raise_for_status()
                    with open(output, "wb") as f:
                        async for chunk in response.aiter_content(chunk_size=DEFAULT_CHUNK_SIZE):
                            f.write(chunk)
                            await callback.on_update(0, len(chunk))
                await callback.on_complete()
                return output
            else:
                headers["User-Agent"] = f'FastGet/{VERSION} (Single-Thread/Memory)'
                response = await client.request(method, url, **req_kwargs)
                response.raise_for_status()
                await callback.on_update(0, len(response.content))
                await callback.on_complete()
                return FastGetResponse(response, response.content)
        finally:
            if client:
                await client.close()

def run_sync(coro: Awaitable[T]) -> T:
    try: loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(coro)

def download(url: str, output: str, **kwargs) -> str:
    session = FastGetSession(max_threads=kwargs.pop("threads", DEFAULT_THREADS), http1=not kwargs.pop("no_http1", False), http2=not kwargs.pop("no_http2", False), http3=not kwargs.pop("no_http3", False))
    return run_sync(session.process("GET", url, output=output, **kwargs))

def request(method: str, url: str, **kwargs) -> FastGetResponse:
    session = FastGetSession(max_threads=kwargs.pop("threads", DEFAULT_THREADS), http1=not kwargs.pop("no_http1", False), http2=not kwargs.pop("no_http2", False), http3=not kwargs.pop("no_http3", False))
    return run_sync(session.process(method, url, output=None, **kwargs))

def get(url: str, **kwargs) -> FastGetResponse:
    return request("GET", url, **kwargs)

def post(url: str, **kwargs) -> FastGetResponse:
    return request("POST", url, **kwargs)
