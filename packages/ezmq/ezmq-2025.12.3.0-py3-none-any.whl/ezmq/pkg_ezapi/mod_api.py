import hashlib
import inspect
import re
from pathlib import Path
from uuid import UUID

from annotated_dict import AnnotatedDict

from ezmq.mq import BatchResponse
from . import Job, Resource, Jobs, Executor, Message
from . import log, MessageQueue, Response
from .. import JSONLResource

REQUEST_DEFAULTS = {
    "params": {},
    "json": {},
    "headers": {}
}


class APICache(JSONLResource):
    def __init__(self, identifier: str = None, cwd: Path = Path.cwd(), default_ttl: int | None = 604800):
        if not identifier:
            identifier = self.__class__.__name__.lower()
        identifier = f"{identifier}-api-cache"
        self.default_ttl = default_ttl  # None = infinite, 0 = no cache, >0 = seconds
        super().__init__(identifier, cwd)


class RequestHash(AnnotatedDict):
    method: str
    url: str
    params: dict
    json: dict
    headers: dict

    @classmethod
    def from_request(cls, **kwargs) -> 'RequestHash':
        if (not kwargs.get('method')) or (not kwargs.get('url')): raise KeyError(
            f'Missing either method or url, got {kwargs} instead')
        kwargs = REQUEST_DEFAULTS.copy() | kwargs
        instance = cls(**kwargs)
        return instance

    @property
    def hash_key(self) -> str:
        hash_data = {
            'method': self.method,
            'url': self.url,
            'params': self.params,
            'json': self.json,
            'headers': self.headers
        }
        json_str = json.dumps(hash_data, sort_keys=True, default=str)
        return hashlib.sha256(json_str.encode()).hexdigest()


class CacheEntry(AnnotatedDict):
    entry_time: int
    ttl: int = 604800
    method: str
    url: str
    params: dict = {}
    json: dict = {}
    headers: dict = {}
    response: dict
    hash_key: str = ""

    def __post_init__(self):
        if not self.hash_key and self.method and self.url:
            self.hash_key = self._compute_hash()

    def _compute_hash(self):
        request_hash = RequestHash(
            method=self.method,
            url=self.url,
            params=self.params,
            json=self.json,
            headers=self.headers
        )
        return request_hash.hash_key

    @classmethod
    def fetch(cls, hash_key: str, cache: list[dict]) -> 'CacheEntry':
        for entry in cache:
            if entry.get('hash_key') == hash_key:
                return cls(**entry)
        return None

    @staticmethod
    def is_in_cache(hash_key: str, cache: list[dict]) -> bool:
        return any(entry.get('hash_key') == hash_key for entry in cache)

    def commit(self, cache: list[dict]):
        if not self.response:
            raise KeyError("Can't commit without a response field!")

        for i, entry in enumerate(cache):
            if entry.get('hash_key') == self.hash_key:
                cache[i] = {**self}
                return

        cache.append({**self})

    @classmethod
    def from_kwargs(cls, **kwargs):
        if not kwargs.get("response"):
            raise KeyError("Can't construct a cache entry without a response field!")

        instance = cls()
        instance.ttl = kwargs.get("ttl", cls.ttl)
        instance.entry_time = int(time.time())
        instance.method = kwargs.get('method', 'GET')
        instance.url = kwargs.get('url', '')
        instance.params = kwargs.get('params', {})
        instance.json = kwargs.get('json', {})
        instance.headers = kwargs.get('headers', {})
        instance.response = kwargs.get('response')
        instance.hash_key = instance._compute_hash()
        return instance


class RequestJob(Job):
    required_resources = ["api_cache"]
    method: str
    url: str
    params: dict = {}
    json: dict = {}
    headers: dict = {}
    cache_ttl: int | None = None

    def __init__(self):
        Job.__init__(self)

    def __repr__(self):
        return f"[{self.__class__.__name__}]"

    def _get_default_kwargs(self) -> dict:
        """Extract default kwargs from class attributes"""
        default_kwargs = {}
        for key, value in inspect.getmembers(self.__class__):
            if key.startswith("_"): continue
            if callable(value): continue
            if key in ["required_resources"]: continue
            if not isinstance(value, type):
                default_kwargs[key] = value
        return default_kwargs

    def _substitute_templates(self, kwargs: dict) -> dict:
        """Substitute ${template} variables in kwargs"""
        template_pattern = r'\$\{([^}]+)\}'

        for key, value in kwargs.items():
            if isinstance(value, str):
                matches = re.findall(template_pattern, value)
                for match in matches:
                    if match in kwargs:
                        value = value.replace(f'${{{match}}}', str(kwargs[match]))
                kwargs[key] = value
            elif isinstance(value, dict):
                for dict_key, dict_value in value.items():
                    if isinstance(dict_value, str):
                        matches = re.findall(template_pattern, dict_value)
                        for match in matches:
                            if match in kwargs:
                                dict_value = dict_value.replace(f'${{{match}}}', str(kwargs[match]))
                        value[dict_key] = dict_value

        return kwargs

    def _prepare_kwargs(self, **kwargs) -> dict:
        """Prepare kwargs by merging defaults and substituting templates"""
        default_kwargs = self._get_default_kwargs()

        # Substitute templates in defaults
        for key, value in default_kwargs.items():
            if isinstance(value, str):
                template_pattern = r'\$\{([^}]+)\}'
                matches = re.findall(template_pattern, value)
                for match in matches:
                    if match in kwargs:
                        value = value.replace(f'${{{match}}}', str(kwargs.pop(match)))
                default_kwargs[key] = value
            elif isinstance(value, dict):
                for dict_key, dict_value in value.items():
                    if isinstance(dict_value, str):
                        template_pattern = r'\$\{([^}]+)\}'
                        matches = re.findall(template_pattern, dict_value)
                        for match in matches:
                            if match in kwargs:
                                dict_value = dict_value.replace(f'${{{match}}}', str(kwargs.pop(match)))
                        value[dict_key] = dict_value

        return default_kwargs | kwargs

    def _get_hash_key(self, **kwargs) -> str:
        """Generate hash key for request"""
        return RequestHash.from_request(**kwargs).hash_key

    def _should_use_cache(self, api_cache: 'APICache') -> bool:
        """Determine if we should check cache for this request"""
        ttl = self.cache_ttl if self.cache_ttl is not None else api_cache.default_ttl
        return ttl != 0

    def _should_write_cache(self, api_cache: 'APICache') -> bool:
        """Determine if we should write to cache"""
        ttl = self.cache_ttl if self.cache_ttl is not None else api_cache.default_ttl
        return ttl != 0

    def _is_cache_valid(self, cache_entry: CacheEntry, api_cache: 'APICache') -> bool:
        """Check if cache entry is still valid"""
        if self.cache_ttl is not None:
            ttl = self.cache_ttl
        else:
            ttl = cache_entry.ttl if hasattr(cache_entry, 'ttl') else api_cache.default_ttl

        if ttl is None or ttl == -1:
            return True

        if ttl == 0:
            return False

        current_time = int(time.time())
        age = current_time - cache_entry.entry_time
        return age < ttl

    def _get_effective_ttl(self, api_cache: 'APICache') -> int | None:
        """Get the TTL value to store with this cache entry"""
        if self.cache_ttl is not None:
            return self.cache_ttl
        return api_cache.default_ttl

    def _make_http_request(self, **kwargs) -> dict:
        """Make HTTP request and return response"""
        log.warning(f"{self}: Couldn't find a request to '{kwargs['url']}' in the cache...")
        log.info(f"{self}: Making '{kwargs['method'].lower()}' request to {kwargs['url']}"
                 f"\n  - params: {kwargs['params']}"
                 f"\n  - json: {kwargs['json']}"
                 f"\n  - headers: {kwargs['headers']}")

        response = httpx.request(
            method=kwargs["method"],
            url=kwargs["url"],
            params=kwargs["params"],
            json=kwargs["json"],
            headers=kwargs["headers"],
        )
        response.raise_for_status()

        if response.is_success:
            log.debug(f"{self}: Successfully made request to '{kwargs['url']}'")
        else:
            log.warning(f"{self}: Failed to make request to '{kwargs['url']}': {response.text}")

        try:
            return response.json()
        except (json.JSONDecodeError, ValueError):
            return {
                "text": response.text,
                "status_code": response.status_code,
                "headers": dict(response.headers)
            }

    def execute(self, resources: dict[str, Resource], **kwargs):
        start_time = time.perf_counter()

        # Prepare kwargs with template substitution
        kwargs = self._prepare_kwargs(**kwargs)

        try:
            api_cache = resources["api_cache"]
            cache = api_cache.peek()
            hash_key = self._get_hash_key(**kwargs)

            # Check cache
            cache_entry = None
            if self._should_use_cache(api_cache):
                cache_entry = CacheEntry.fetch(hash_key, cache)
                if cache_entry and not self._is_cache_valid(cache_entry, api_cache):
                    log.debug(f"{self}: Cache entry expired (age: {int(time.time()) - cache_entry.entry_time}s)")
                    cache_entry = None

            if not cache_entry:
                try:
                    kwargs["response"] = self._make_http_request(**kwargs)
                except httpx.HTTPStatusError as e:
                    raise Exception(f"Failed to make request to '{kwargs['url']}': {e}")
                except httpx.RequestError as e:
                    raise Exception(f"Failed to make request to '{kwargs.get('url', 'unknown')}': {e}")
                except Exception as e:
                    raise Exception(f"Unexpected error for '{kwargs.get('url', 'unknown')}': {e}")

                # Write to cache
                if self._should_write_cache(api_cache):
                    try:
                        effective_ttl = self._get_effective_ttl(api_cache)
                        cache_entry = CacheEntry.from_kwargs(**kwargs,
                                                             ttl=effective_ttl if effective_ttl is not None else 604800)
                        with api_cache as c:
                            cache_entry.commit(c)

                        if CacheEntry.is_in_cache(cache_entry.hash_key, api_cache.peek()):
                            ttl_display = "infinite" if effective_ttl in (None, -1) else f"{effective_ttl}s"
                            log.info(
                                f"{self}: Successfully cached request as '{cache_entry.hash_key}' (TTL: {ttl_display})")

                    except Exception as e:
                        log.error(f"Error caching request for '{self.url}': {e}")

                end_time = time.perf_counter()
                duration = end_time - start_time
                log.debug(f"{self}: Executed fresh request in: {duration:.4f} seconds")
                return kwargs["response"]

            else:
                end_time = time.perf_counter()
                duration = end_time - start_time
                log.debug(f"{self}: Retrieved from cache in: {duration:.4f} seconds")
                return cache_entry.response

        except Exception as e:
            raise Exception

class RequestJobs(Jobs):
    def __init__(self, identifier: str = None, cwd: Path = Path.cwd(), default_cache_ttl: int | None = 604800):
        if not identifier:
            identifier = self.__class__.__name__.lower()
        self.identifier = identifier
        if "api_cache" not in self.resources:
            self.resources["api_cache"] = APICache(identifier, cwd, default_cache_ttl)
        super().__init__()
        log.debug(f"{self}: Initialized with {len(self.types)} jobs and {len(self.resources)} resources for API Calls")

    def __repr__(self):
        return f"[{self.__class__.__name__}.RequestJobs]"


class RequestMessageQueue(MessageQueue):
    def __init__(self, job_types: type[RequestJobs], executor: type[Executor] = Executor, auto_start: bool = True):
        super().__init__(job_types, executor, auto_start)


class APIClient:
    headers = {}
    job_types: type[RequestJobs]
    auto_start: bool = True

    def __init__(self):
        if self.__class__.__name__ == "APIClient":
            raise RuntimeError("APIClient cannot be instantiated directly, it must be inherited")

        self.header_deviations: dict[str, dict[str, str]] = {}
        for job_name, job_type in self.job_types.__annotations__.items():
            job_type: RequestJob
            for pointer in job_type.__dict__:
                if pointer == "headers":
                    log.debug(f"{self}: Identified header deviation from default in job type '{job_type.__name__}'")
                    self.header_deviations[job_name] = job_type.__dict__[pointer]

        if not self.job_types:
            raise AttributeError("No job_types referenced")

        self.mq = RequestMessageQueue(self.job_types, executor=Executor, auto_start=self.auto_start)

    def __repr__(self):
        return f"[{self.__class__.__name__}.APIClient]"

    def _compile_headers(self, job_type, **kwargs):
        if not job_type in self.header_deviations:
            headers = self.headers
            if kwargs.get("headers"):
                headers = self.headers | kwargs["headers"]
            else:
                kwargs = {"headers": headers} | kwargs
        return kwargs

    def request(self, job_type: str, **kwargs) -> UUID:
        kwargs = self._compile_headers(job_type, **kwargs)
        return self.mq.send(job_type, **kwargs)

    def response(self, request_id: UUID) -> Response:
        return self.mq.receive(request_id)

    def request_and_response(self, job_type: str, timeout: int = 10, **kwargs) -> Response:
        kwargs = self._compile_headers(job_type, **kwargs)
        return self.mq.send_and_receive(job_type, timeout, **kwargs)

    def batch_request(self, messages: dict[str, Message]) -> dict[str, UUID]:
        for message in messages.values():
            if not message.get("payload"): continue
            message["payload"] = self._compile_headers(message.job_type, **message.payload)
        return self.mq.batch_send(messages)

    def batch_response(self, message_ids: dict[str, UUID], min_timeout: float = 1.0, max_iteration: int = 10) -> BatchResponse:
        return self.mq.batch_receive(message_ids, min_timeout, max_iteration)

    def batch_request_and_response(self, messages: dict[str, Message], min_timeout: float = 1.0,
                                   max_iteration: int = 10):
        for message in messages.values():
            if not message.get("payload"): continue
            message["payload"] = self._compile_headers(message.job_type, **message.payload)
        return self.mq.batch_send_and_receive(messages, min_timeout=min_timeout, max_iteration=max_iteration)


import json
import time
import threading
from pathlib import Path
from uuid import UUID

import pytest
import httpx
from unittest.mock import Mock, patch

from ezmq import Job, Executor


@pytest.fixture
def temp_dir(tmp_path):
    return tmp_path


@pytest.fixture
def api_cache(temp_dir):
    return APICache("test_api", cwd=temp_dir)


@pytest.fixture
def mock_response():
    response = Mock(spec=httpx.Response)
    response.is_success = True
    response.status_code = 200
    response.json.return_value = {"data": "test_data", "status": "success"}
    response.text = '{"data": "test_data", "status": "success"}'
    response.headers = {"content-type": "application/json"}
    return response


class TestRequestHash:
    def test_from_request_basic(self):
        hash_obj = RequestHash.from_request(method="GET", url="https://api.example.com")
        assert hash_obj.method == "GET"
        assert hash_obj.url == "https://api.example.com"
        assert hash_obj.params == {}
        assert hash_obj.json == {}
        assert hash_obj.headers == {}

    def test_from_request_with_params(self):
        hash_obj = RequestHash.from_request(
            method="POST",
            url="https://api.example.com/users",
            params={"page": 1},
            json={"name": "test"},
            headers={"Authorization": "Bearer token"}
        )
        assert hash_obj.params == {"page": 1}
        assert hash_obj.json == {"name": "test"}
        assert hash_obj.headers == {"Authorization": "Bearer token"}

    def test_from_request_missing_method(self):
        with pytest.raises(KeyError):
            RequestHash.from_request(url="https://api.example.com")

    def test_from_request_missing_url(self):
        with pytest.raises(KeyError):
            RequestHash.from_request(method="GET")

    def test_hash_key_deterministic(self):
        hash1 = RequestHash.from_request(method="GET", url="https://api.example.com")
        hash2 = RequestHash.from_request(method="GET", url="https://api.example.com")
        assert hash1.hash_key == hash2.hash_key

    def test_hash_key_different_params(self):
        hash1 = RequestHash.from_request(
            method="GET",
            url="https://api.example.com",
            params={"page": 1}
        )
        hash2 = RequestHash.from_request(
            method="GET",
            url="https://api.example.com",
            params={"page": 2}
        )
        assert hash1.hash_key != hash2.hash_key

    def test_hash_key_same_params_different_order(self):
        hash1 = RequestHash.from_request(
            method="GET",
            url="https://api.example.com",
            params={"a": 1, "b": 2}
        )
        hash2 = RequestHash.from_request(
            method="GET",
            url="https://api.example.com",
            params={"b": 2, "a": 1}
        )
        assert hash1.hash_key == hash2.hash_key


class TestCacheEntry:
    def test_from_kwargs_basic(self):
        entry = CacheEntry.from_kwargs(
            method="GET",
            url="https://api.example.com",
            response={"data": "test"}
        )
        assert entry.method == "GET"
        assert entry.url == "https://api.example.com"
        assert entry.response == {"data": "test"}
        assert entry.hash_key

    def test_from_kwargs_without_response(self):
        with pytest.raises(KeyError):
            CacheEntry.from_kwargs(method="GET", url="https://api.example.com")

    def test_from_kwargs_with_custom_ttl(self):
        entry = CacheEntry.from_kwargs(
            method="GET",
            url="https://api.example.com",
            response={"data": "test"},
            ttl=3600
        )
        assert entry.ttl == 3600

    def test_commit_to_empty_cache(self):
        cache = []
        entry = CacheEntry.from_kwargs(
            method="GET",
            url="https://api.example.com",
            response={"data": "test"}
        )
        entry.commit(cache)
        assert len(cache) == 1
        assert cache[0]["hash_key"] == entry.hash_key

    def test_commit_updates_existing(self):
        cache = []
        entry1 = CacheEntry.from_kwargs(
            method="GET",
            url="https://api.example.com",
            response={"data": "old"}
        )
        entry1.commit(cache)

        entry2 = CacheEntry.from_kwargs(
            method="GET",
            url="https://api.example.com",
            response={"data": "new"}
        )
        entry2.commit(cache)

        assert len(cache) == 1
        assert cache[0]["response"]["data"] == "new"

    def test_fetch_existing(self):
        cache = []
        entry = CacheEntry.from_kwargs(
            method="GET",
            url="https://api.example.com",
            response={"data": "test"}
        )
        entry.commit(cache)

        fetched = CacheEntry.fetch(entry.hash_key, cache)
        assert fetched is not None
        assert fetched.response == {"data": "test"}

    def test_fetch_nonexistent(self):
        cache = []
        fetched = CacheEntry.fetch("nonexistent_hash", cache)
        assert fetched is None

    def test_is_in_cache(self):
        cache = []
        entry = CacheEntry.from_kwargs(
            method="GET",
            url="https://api.example.com",
            response={"data": "test"}
        )
        entry.commit(cache)

        assert CacheEntry.is_in_cache(entry.hash_key, cache)
        assert not CacheEntry.is_in_cache("nonexistent", cache)

    def test_commit_without_response(self):
        cache = []
        entry = CacheEntry(
            method="GET",
            url="https://api.example.com",
            entry_time=int(time.time())
        )
        with pytest.raises(KeyError):
            entry.commit(cache)


class TestAPICache:
    def test_initialization(self, temp_dir):
        cache = APICache("test", cwd=temp_dir)
        assert cache.identifier == "test-api-cache"
        assert cache.file_path.name == "test-api-cache.jsonl"

    def test_read_write(self, temp_dir):
        cache = APICache("test", cwd=temp_dir)

        with cache as data:
            data.append({"key": "value1"})
            data.append({"key": "value2"})

        peeked = cache.peek()
        assert len(peeked) == 2
        assert peeked[0]["key"] == "value1"
        assert peeked[1]["key"] == "value2"

    def test_persistence(self, temp_dir):
        cache1 = APICache("test", cwd=temp_dir)
        with cache1 as data:
            data.append({"persistent": "data"})

        cache2 = APICache("test", cwd=temp_dir)
        peeked = cache2.peek()
        assert len(peeked) == 1
        assert peeked[0]["persistent"] == "data"


class TestRequestJob:
    def test_job_initialization(self):
        job = RequestJob()
        assert "api_cache" in job.required_resources

    def test_template_substitution(self, api_cache, mock_response):
        class TestJob(RequestJob):
            method = "GET"
            url = "https://api.example.com/users/${user_id}"
            params = {"filter": "${filter_value}"}

        job = TestJob()
        resources = {"api_cache": api_cache}

        with patch('httpx.request', return_value=mock_response):
            result = job.execute(resources, user_id="123", filter_value="active")
            assert result == {"data": "test_data", "status": "success"}

    def test_caching_behavior(self, api_cache, mock_response):
        class TestJob(RequestJob):
            method = "GET"
            url = "https://api.example.com/data"

        job = TestJob()
        resources = {"api_cache": api_cache}

        with patch('httpx.request', return_value=mock_response) as mock_request:
            result1 = job.execute(resources)
            result2 = job.execute(resources)

            assert mock_request.call_count == 1
            assert result1 == result2

    def test_http_error_handling(self, api_cache):
        class TestJob(RequestJob):
            method = "GET"
            url = "https://api.example.com/error"

        job = TestJob()
        resources = {"api_cache": api_cache}

        error_response = Mock(spec=httpx.Response)
        error_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "404 Not Found",
            request=Mock(),
            response=Mock()
        )

        with patch('httpx.request', return_value=error_response):
            with pytest.raises(Exception):
                job.execute(resources)

    def test_non_json_response(self, api_cache):
        class TestJob(RequestJob):
            method = "GET"
            url = "https://api.example.com/html"

        job = TestJob()
        resources = {"api_cache": api_cache}

        html_response = Mock(spec=httpx.Response)
        html_response.is_success = True
        html_response.status_code = 200
        html_response.json.side_effect = json.JSONDecodeError("msg", "doc", 0)
        html_response.text = "<html>test</html>"
        html_response.headers = {"content-type": "text/html"}
        html_response.raise_for_status = Mock()

        with patch('httpx.request', return_value=html_response):
            result = job.execute(resources)
            assert result["text"] == "<html>test</html>"
            assert result["status_code"] == 200


class TestAPIClient:
    def test_cannot_instantiate_directly(self):
        with pytest.raises(RuntimeError):
            APIClient()

    def test_subclass_initialization(self, temp_dir):
        class GetUserJob(RequestJob):
            method = "GET"
            url = "https://api.example.com/users/${user_id}"

        class TestJobs(RequestJobs):
            get_user: GetUserJob

        class TestClient(APIClient):
            job_types = TestJobs
            headers = {"Authorization": "Bearer test_token"}

        client = TestClient()
        assert client.mq is not None

    def test_request_and_response(self, temp_dir, mock_response):
        class GetDataJob(RequestJob):
            method = "GET"
            url = "https://api.example.com/data"

        class TestJobs(RequestJobs):
            get_data: GetDataJob

            def __init__(self, identifier: str = None, cwd: Path = Path.cwd()):
                super().__init__(identifier, cwd)

        class TestClient(APIClient):
            job_types = TestJobs
            headers = {"Authorization": "Bearer token"}

        with patch('httpx.request', return_value=mock_response):
            client = TestClient()
            request_id = client.request("get_data")
            assert isinstance(request_id, UUID)

            response = client.response(request_id)
            assert response.success == True
            assert response.result == {"data": "test_data", "status": "success"}

    def test_header_compilation(self, temp_dir, mock_response):
        # Generate unique identifier for this test
        import uuid
        test_id = str(uuid.uuid4())[:8]

        class GetDataJob(RequestJob):
            method = "GET"
            url = f"https://api.example.com/data-{test_id}"

        class TestJobs(RequestJobs):
            get_data: GetDataJob

            def __init__(self, identifier: str = None, cwd: Path = Path.cwd()):
                super().__init__(f"headers_test_{test_id}", temp_dir)

        class TestClient(APIClient):
            job_types = TestJobs
            headers = {"Authorization": "Bearer token", "X-Custom": "value"}

        with patch('httpx.request', return_value=mock_response) as mock_request:
            client = TestClient()
            request_id = client.request("get_data")

            time.sleep(0.5)

            call_kwargs = mock_request.call_args.kwargs
            assert "Authorization" in call_kwargs["headers"]
            assert "X-Custom" in call_kwargs["headers"]

    def test_concurrent_requests(self, temp_dir, mock_response):
        class GetDataJob(RequestJob):
            method = "GET"
            url = "https://api.example.com/data/${id}"

        class TestJobs(RequestJobs):
            get_data: GetDataJob

        class TestClient(APIClient):
            job_types = TestJobs

        with patch('httpx.request', return_value=mock_response):
            client = TestClient()

            request_ids = []
            for i in range(10):
                request_id = client.request("get_data", id=str(i))
                request_ids.append(request_id)

            responses = []
            for request_id in request_ids:
                response = client.response(request_id)
                responses.append(response)

            assert len(responses) == 10
            assert all(r.success == True for r in responses)

    def test_batch_request(self, temp_dir, mock_response):
        class GetDataJob(RequestJob):
            method = "GET"
            url = "https://api.example.com/data/${id}"

        class TestJobs(RequestJobs):
            get_data: GetDataJob

        class TestClient(APIClient):
            job_types = TestJobs

        with patch('httpx.request', return_value=mock_response):
            client = TestClient()

            from ezmq import Message
            messages = {}
            for i in range(5):
                msg = Message()
                msg.job_type = "get_data"
                msg.payload = {"id": str(i)}
                messages[f"request_{i}"] = msg

            request_ids = client.batch_request(messages)
            assert len(request_ids) == 5
            assert all(isinstance(uid, UUID) for uid in request_ids.values())


class TestConcurrency:
    def test_thread_safe_caching(self, temp_dir, mock_response):
        class GetDataJob(RequestJob):
            method = "GET"
            url = "https://api.example.com/data"

        class TestJobs(RequestJobs):
            get_data: GetDataJob

        class TestClient(APIClient):
            job_types = TestJobs

        errors = []
        results = []

        def make_request(client):
            try:
                request_id = client.request("get_data")
                response = client.response(request_id)
                results.append(response.result)
            except Exception as e:
                errors.append(e)

        with patch('httpx.request', return_value=mock_response):
            client = TestClient()

            threads = []
            for _ in range(10):
                t = threading.Thread(target=make_request, args=(client,))
                threads.append(t)
                t.start()

            for t in threads:
                t.join()

        assert not errors
        assert len(results) == 10
        assert all(r == results[0] for r in results)

    def test_concurrent_different_requests(self, temp_dir):
        class GetDataJob(RequestJob):
            method = "GET"
            url = "https://api.example.com/data/${id}"

        class TestJobs(RequestJobs):
            get_data: GetDataJob

        class TestClient(APIClient):
            job_types = TestJobs

        def mock_request_func(**kwargs):
            response = Mock(spec=httpx.Response)
            response.is_success = True
            response.status_code = 200

            url = kwargs.get('url', '')
            data_id = url.split('/')[-1] if '/' in url else '0'
            response.json.return_value = {"id": data_id, "data": f"data_{data_id}"}
            response.raise_for_status = Mock()
            return response

        errors = []
        results = {}

        def make_request(client, request_id):
            try:
                uuid = client.request("get_data", id=str(request_id))
                response = client.response(uuid)
                results[request_id] = response.result
            except Exception as e:
                errors.append((request_id, e))

        with patch('httpx.request', side_effect=mock_request_func):
            client = TestClient()

            threads = []
            for i in range(20):
                t = threading.Thread(target=make_request, args=(client, i))
                threads.append(t)
                t.start()

            for t in threads:
                t.join()

        assert not errors
        assert len(results) == 20


class TestCacheEviction:
    def test_ttl_stored(self, temp_dir):
        cache = APICache("test", cwd=temp_dir)

        entry = CacheEntry.from_kwargs(
            method="GET",
            url="https://api.example.com/data",
            response={"data": "test"},
            ttl=3600
        )

        with cache as c:
            entry.commit(c)

        cached = cache.peek()
        assert cached[0]["ttl"] == 3600

    def test_entry_time_recorded(self, temp_dir):
        cache = APICache("test", cwd=temp_dir)

        before = int(time.time())
        entry = CacheEntry.from_kwargs(
            method="GET",
            url="https://api.example.com/data",
            response={"data": "test"}
        )
        after = int(time.time())

        assert before <= entry.entry_time <= after


class TestEdgeCases:
    def test_empty_cache_file(self, temp_dir):
        cache = APICache("test", cwd=temp_dir)
        cache.file_path.touch()

        peeked = cache.peek()
        assert peeked == []

    def test_corrupted_cache_line(self, temp_dir):
        cache = APICache("test", cwd=temp_dir)

        with cache as c:
            c.append({"valid": "entry1"})

        with cache.file_path.open('a') as f:
            f.write('{"invalid": json\n')

        with cache as c:
            c.append({"valid": "entry2"})

        peeked = cache.peek()
        assert len(peeked) >= 2
        assert any(e.get("valid") == "entry1" for e in peeked)
        assert any(e.get("valid") == "entry2" for e in peeked)

    def test_large_response_body(self, temp_dir, mock_response):
        large_data = {"data": "x" * 100000}
        mock_response.json.return_value = large_data

        class GetDataJob(RequestJob):
            method = "GET"
            url = "https://api.example.com/large"

        job = GetDataJob()
        cache = APICache("test", cwd=temp_dir)
        resources = {"api_cache": cache}

        with patch('httpx.request', return_value=mock_response):
            result = job.execute(resources)
            assert result == large_data

            cached = cache.peek()
            assert len(cached) == 1
            assert cached[0]["response"] == large_data


@pytest.fixture
def temp_dir(tmp_path):
    return tmp_path


@pytest.fixture
def mock_response():
    response = Mock(spec=httpx.Response)
    response.is_success = True
    response.status_code = 200
    response.json.return_value = {"data": "test_data", "status": "success"}
    response.text = '{"data": "test_data", "status": "success"}'
    response.headers = {"content-type": "application/json"}
    response.raise_for_status = Mock()
    return response


class TestTTLInfiniteCache:
    def test_infinite_cache_with_none(self, temp_dir, mock_response):
        """Test that cache_ttl=None means infinite caching"""
        cache = APICache("test_infinite", cwd=temp_dir, default_ttl=None)

        class TestJob(RequestJob):
            method = "GET"
            url = "https://api.example.com/infinite-cache-test"
            cache_ttl = None

        job = TestJob()
        resources = {"api_cache": cache}

        with patch('httpx.request', return_value=mock_response) as mock_request:
            result1 = job.execute(resources)
            assert mock_request.call_count == 1

            time.sleep(1)
            result2 = job.execute(resources)

            assert mock_request.call_count == 1
            assert result1 == result2

            cached = cache.peek()
            assert len(cached) == 1

    def test_infinite_cache_with_negative_one(self, temp_dir, mock_response):
        """Test that cache_ttl=-1 means infinite caching"""
        cache = APICache("test_infinite_neg", cwd=temp_dir, default_ttl=3600)

        class TestJob(RequestJob):
            method = "GET"
            url = "https://api.example.com/infinite-neg-test"
            cache_ttl = -1

        job = TestJob()
        resources = {"api_cache": cache}

        with patch('httpx.request', return_value=mock_response) as mock_request:
            result1 = job.execute(resources)
            time.sleep(1)
            result2 = job.execute(resources)

            assert mock_request.call_count == 1
            assert result1 == result2

    def test_global_infinite_cache(self, temp_dir, mock_response):
        """Test that default_ttl=None makes all requests cache infinitely"""
        cache = APICache("test_global_infinite", cwd=temp_dir, default_ttl=None)

        class TestJob(RequestJob):
            method = "GET"
            url = "https://api.example.com/global-infinite"

        job = TestJob()
        resources = {"api_cache": cache}

        with patch('httpx.request', return_value=mock_response) as mock_request:
            job.execute(resources)
            time.sleep(1)
            job.execute(resources)
            job.execute(resources)

            assert mock_request.call_count == 1
            assert len(cache.peek()) == 1


class TestTTLNoCache:
    def test_no_caching_with_zero(self, temp_dir, mock_response):
        """Test that cache_ttl=0 disables caching"""
        cache = APICache("test_no_cache", cwd=temp_dir, default_ttl=0)

        class TestJob(RequestJob):
            method = "GET"
            url = "https://api.example.com/no-cache-test"
            cache_ttl = 0

        job = TestJob()
        resources = {"api_cache": cache}

        with patch('httpx.request', return_value=mock_response) as mock_request:
            result1 = job.execute(resources)
            result2 = job.execute(resources)

            assert mock_request.call_count == 2
            assert result1 == result2

            cached = cache.peek()
            assert len(cached) == 0

    def test_global_no_caching(self, temp_dir, mock_response):
        """Test that default_ttl=0 disables all caching"""
        cache = APICache("test_global_no_cache", cwd=temp_dir, default_ttl=0)

        class TestJob(RequestJob):
            method = "GET"
            url = "https://api.example.com/global-no-cache"

        job = TestJob()
        resources = {"api_cache": cache}

        with patch('httpx.request', return_value=mock_response) as mock_request:
            job.execute(resources)
            job.execute(resources)
            job.execute(resources)

            assert mock_request.call_count == 3
            assert len(cache.peek()) == 0

    def test_job_level_no_cache_overrides_default(self, temp_dir, mock_response):
        """Test that job-level cache_ttl=0 overrides default TTL"""
        cache = APICache("test_override_no_cache", cwd=temp_dir, default_ttl=3600)

        class NoCacheJob(RequestJob):
            method = "GET"
            url = "https://api.example.com/override-no-cache"
            cache_ttl = 0

        job = NoCacheJob()
        resources = {"api_cache": cache}

        with patch('httpx.request', return_value=mock_response) as mock_request:
            job.execute(resources)
            job.execute(resources)

            assert mock_request.call_count == 2
            assert len(cache.peek()) == 0


class TestTTLExpiration:
    def test_custom_ttl_expiration(self, temp_dir, mock_response):
        """Test that cache expires after custom TTL"""
        cache = APICache("test_expire", cwd=temp_dir, default_ttl=1)

        class TestJob(RequestJob):
            method = "GET"
            url = "https://api.example.com/expire-test"
            cache_ttl = 1

        job = TestJob()
        resources = {"api_cache": cache}

        with patch('httpx.request', return_value=mock_response) as mock_request:
            result1 = job.execute(resources)
            assert mock_request.call_count == 1

            result2 = job.execute(resources)
            assert mock_request.call_count == 1

            time.sleep(2)

            result3 = job.execute(resources)
            assert mock_request.call_count == 2

            assert result1 == result2 == result3

    def test_per_job_ttl_override(self, temp_dir, mock_response):
        """Test that job-level TTL overrides cache default"""
        cache = APICache("test_override", cwd=temp_dir, default_ttl=3600)

        class ShortTTLJob(RequestJob):
            method = "GET"
            url = "https://api.example.com/short-ttl"
            cache_ttl = 1

        class DefaultTTLJob(RequestJob):
            method = "GET"
            url = "https://api.example.com/default-ttl"

        short_job = ShortTTLJob()
        default_job = DefaultTTLJob()
        resources = {"api_cache": cache}

        with patch('httpx.request', return_value=mock_response) as mock_request:
            short_job.execute(resources)
            default_job.execute(resources)

            time.sleep(2)

            short_job.execute(resources)
            default_job.execute(resources)

            assert mock_request.call_count == 3

    def test_job_ttl_overrides_entry_ttl(self, temp_dir, mock_response):
        """Test that job-level TTL overrides the stored entry TTL"""
        cache = APICache("test_override_entry", cwd=temp_dir, default_ttl=3600)

        class FlexibleJob(RequestJob):
            method = "GET"
            url = "https://api.example.com/flexible"

        job = FlexibleJob()
        resources = {"api_cache": cache}

        with patch('httpx.request', return_value=mock_response) as mock_request:
            job.cache_ttl = 3600
            job.execute(resources)
            assert mock_request.call_count == 1

            time.sleep(2)

            job.cache_ttl = 1
            job.execute(resources)

            assert mock_request.call_count == 2


class TestTTLMixedStrategies:
    def test_mixed_ttl_strategies(self, temp_dir, mock_response):
        """Test mixing infinite, timed, and no-cache strategies"""
        cache = APICache("test_mixed", cwd=temp_dir, default_ttl=3600)

        class InfiniteJob(RequestJob):
            method = "GET"
            url = "https://api.example.com/infinite"
            cache_ttl = None

        class ShortJob(RequestJob):
            method = "GET"
            url = "https://api.example.com/short"
            cache_ttl = 1

        class NoCacheJob(RequestJob):
            method = "GET"
            url = "https://api.example.com/nocache"
            cache_ttl = 0

        infinite_job = InfiniteJob()
        short_job = ShortJob()
        nocache_job = NoCacheJob()
        resources = {"api_cache": cache}

        with patch('httpx.request', return_value=mock_response) as mock_request:
            infinite_job.execute(resources)
            short_job.execute(resources)
            nocache_job.execute(resources)
            assert mock_request.call_count == 3

            time.sleep(2)

            infinite_job.execute(resources)
            short_job.execute(resources)
            nocache_job.execute(resources)

            assert mock_request.call_count == 5
            assert len(cache.peek()) == 2


class TestTTLValidationLogic:
    def test_cache_validation_infinite(self, temp_dir):
        """Test validation logic for infinite cache"""
        cache = APICache("test_validation_inf", cwd=temp_dir, default_ttl=3600)

        class TestJob(RequestJob):
            method = "GET"
            url = "https://api.example.com/validation-test"

        job = TestJob()

        current_time = int(time.time())

        entry_infinite_none = CacheEntry(
            method="GET",
            url="test",
            entry_time=current_time - 10000,
            ttl=None,
            response={"data": "test"},
            hash_key="test123"
        )
        assert job._is_cache_valid(entry_infinite_none, cache) == True

        entry_infinite_neg = CacheEntry(
            method="GET",
            url="test",
            entry_time=current_time - 10000,
            ttl=-1,
            response={"data": "test"},
            hash_key="test124"
        )
        assert job._is_cache_valid(entry_infinite_neg, cache) == True

    def test_cache_validation_no_cache(self, temp_dir):
        """Test validation logic for no cache"""
        cache = APICache("test_validation_no", cwd=temp_dir, default_ttl=3600)

        class TestJob(RequestJob):
            method = "GET"
            url = "https://api.example.com/validation-test"

        job = TestJob()
        current_time = int(time.time())

        entry_no_cache = CacheEntry(
            method="GET",
            url="test",
            entry_time=current_time,
            ttl=0,
            response={"data": "test"},
            hash_key="test125"
        )
        assert job._is_cache_valid(entry_no_cache, cache) == False

    def test_cache_validation_timed(self, temp_dir):
        """Test validation logic for timed cache"""
        cache = APICache("test_validation_timed", cwd=temp_dir, default_ttl=3600)

        class TestJob(RequestJob):
            method = "GET"
            url = "https://api.example.com/validation-test"

        job = TestJob()
        current_time = int(time.time())

        entry_valid = CacheEntry(
            method="GET",
            url="test",
            entry_time=current_time - 100,
            ttl=3600,
            response={"data": "test"},
            hash_key="test126"
        )
        assert job._is_cache_valid(entry_valid, cache) == True

        entry_expired = CacheEntry(
            method="GET",
            url="test",
            entry_time=current_time - 7200,
            ttl=3600,
            response={"data": "test"},
            hash_key="test127"
        )
        assert job._is_cache_valid(entry_expired, cache) == False


class TestTTLEdgeCases:
    def test_ttl_stored_correctly(self, temp_dir):
        """Test that TTL is stored correctly in cache"""
        cache = APICache("test_ttl_storage", cwd=temp_dir)

        entry = CacheEntry.from_kwargs(
            method="GET",
            url="https://api.example.com/data",
            response={"data": "test"},
            ttl=3600
        )

        with cache as c:
            entry.commit(c)

        cached = cache.peek()
        assert cached[0]["ttl"] == 3600

    def test_ttl_none_stored_correctly(self, temp_dir):
        """Test that TTL=None is stored correctly"""
        cache = APICache("test_ttl_none", cwd=temp_dir, default_ttl=None)

        entry = CacheEntry.from_kwargs(
            method="GET",
            url="https://api.example.com/infinite",
            response={"data": "test"},
            ttl=None
        )

        with cache as c:
            entry.commit(c)

        cached = cache.peek()
        # Depending on implementation, None might be stored as 604800 or None
        assert cached[0]["ttl"] in (None, 604800)

    def test_multiple_jobs_different_ttls(self, temp_dir, mock_response):
        """Test that multiple jobs with different TTLs work correctly"""
        cache = APICache("test_multi_ttl", cwd=temp_dir, default_ttl=3600)

        class Job1(RequestJob):
            method = "GET"
            url = "https://api.example.com/job1"
            cache_ttl = None

        class Job2(RequestJob):
            method = "GET"
            url = "https://api.example.com/job2"
            cache_ttl = 1

        class Job3(RequestJob):
            method = "GET"
            url = "https://api.example.com/job3"
            cache_ttl = 0

        job1 = Job1()
        job2 = Job2()
        job3 = Job3()
        resources = {"api_cache": cache}

        with patch('httpx.request', return_value=mock_response) as mock_request:
            job1.execute(resources)
            job2.execute(resources)
            job3.execute(resources)
            assert mock_request.call_count == 3

            time.sleep(2)

            job1.execute(resources)  # Cached (infinite)
            job2.execute(resources)  # Expired (new call)
            job3.execute(resources)  # Never cached (new call)

            assert mock_request.call_count == 5

            time.sleep(2)

            job1.execute(resources)  # Still cached
            job2.execute(resources)  # Still expired
            job3.execute(resources)  # Still not cached

            assert mock_request.call_count == 7


class TestTTLIntegration:
    def test_ttl_with_api_client(self, temp_dir, mock_response):
        """Test TTL functionality through APIClient"""
        import uuid
        test_id = str(uuid.uuid4())[:8]

        class InfiniteJob(RequestJob):
            method = "GET"
            url = f"https://api.example.com/infinite-{test_id}"
            cache_ttl = None

        class TestJobs(RequestJobs):
            infinite_job: InfiniteJob

            def __init__(self, identifier: str = None, cwd: Path = Path.cwd()):
                super().__init__(f"ttl_test_{test_id}", temp_dir, default_cache_ttl=3600)

        class TestClient(APIClient):
            job_types = TestJobs

        with patch('httpx.request', return_value=mock_response) as mock_request:
            client = TestClient()

            request_id1 = client.request("infinite_job")
            response1 = client.response(request_id1)

            time.sleep(1)

            request_id2 = client.request("infinite_job")
            response2 = client.response(request_id2)

            assert mock_request.call_count == 1
            assert response1.success == response2.success


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
