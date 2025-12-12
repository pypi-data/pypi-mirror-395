import asyncio
import inspect
import time
import traceback
import uuid
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor
from queue import PriorityQueue
from threading import Thread, Lock
from typing import Any, Dict
from uuid import UUID

from annotated_dict import AnnotatedDict
from loguru import logger as log


class Resource(ABC):
    """
    Abstract base class for managing shared resources with automatic locking.

    Resources represent any shared state that requires synchronized access across
    multiple threads or processes. The class implements the context manager protocol
    to ensure proper acquisition and release of locks.

    Attributes:
        identifier: Unique string identifying this resource instance
        timeout: Maximum seconds to wait when acquiring the lock
        lock: Threading lock for synchronization
        _resource: Internal storage for the resource data loaded during context entry

    Usage:
        class DatabaseResource(Resource):
            def _enter(self):
                return connect_to_database(self.identifier)

            def _exit(self):
                self._resource.close()

            def _peek(self):
                return read_only_connection(self.identifier)

        db = DatabaseResource("main_db", timeout=10.0)

        with db as connection:
            connection.execute("UPDATE users SET ...")

        data = db.peek()
    """

    def __init__(self, identifier: str, timeout: float = 30.0):
        self.identifier = identifier
        self.timeout = timeout
        self.lock = Lock()
        self._resource = None

    @abstractmethod
    def _enter(self):
        pass

    @abstractmethod
    def _exit(self):
        pass

    @abstractmethod
    def _peek(self):
        """
        Read the resource without acquiring the lock.

        This method provides non-blocking read-only access to the resource.
        Implement this to return a snapshot or read-only view of the resource
        without acquiring the lock. This is useful for checking state without
        blocking other operations.

        Returns:
            Read-only view or snapshot of the resource

        Raises:
            Any exception during read operation

        Warning:
            The returned data may be stale or inconsistent if another thread
            is currently modifying the resource. Use with caution.
        """
        pass

    def peek(self):
        """
        Get read-only access to the resource without locking.

        Returns:
            Read-only view or snapshot from _peek()

        Warning:
            This does not acquire the lock, so the data may be inconsistent
            if the resource is being modified by another thread.
        """
        return self._peek()

    def __enter__(self):
        acquired = self.lock.acquire(timeout=self.timeout)
        if not acquired:
            raise TimeoutError(f"Could not acquire {self.__class__.__name__}:{self.identifier}")

        try:
            self._resource = self._enter()
            return self._resource
        except Exception as e:
            self.lock.release()
            raise

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self._exit()
        finally:
            self.lock.release()


class Job(ABC):
    """
    Abstract base class for defining work units that can be executed by the message queue.

    Jobs encapsulate a specific operation that can be queued and executed concurrently.
    Each job declares which resources it needs, and the executor ensures those resources
    are available when the job runs.

    Attributes:
        required_resources: List of resource identifiers this job needs to access

    Usage:
        class ProcessDataJob(Job):
            required_resources = ['database', 'file_storage']

            def execute(self, resources, **kwargs):
                if not (data_id := kwargs.get('data_id')): raise KeyError('data_id is required')
                with resources['database'] as db:
                    data = db.fetch(data_id)
                with resources['file_storage'] as fs:
                    fs.save(data)
                return {'status': 'complete'}
    """

    required_resources: list[str] = []

    @abstractmethod
    def execute(self, resources: dict[str, Resource], **kwargs):
        """
        Execute the job's operation.

        This method contains the core logic of the job. It receives access to any
        required resources and can accept arbitrary keyword arguments from the
        message payload.

        Args:
            resources: Dictionary mapping resource names to Resource instances
            **kwargs: Arbitrary keyword arguments from the message payload

        Returns:
            Any result data to be returned in the Response

        Raises:
            Any exception raised here will be caught and returned as an error Response
        """
        pass


class Jobs:
    """
    Container class for registering job types and managing their resources.

    Jobs acts as a registry that validates job classes at initialization and provides
    methods to look up job types and their required resources. Job types are declared
    as type annotations on subclasses.

    Attributes:
        resources: Dictionary mapping resource names to Resource instances shared
                  across all job types

    Usage:
        class MyJobs(Jobs):
            resources = {
                'db': DatabaseResource('main.db'),
                'cache': CacheResource('redis://localhost')
            }

            send_email: SendEmailJob
            process_payment: ProcessPaymentJob
            generate_report: GenerateReportJob

        jobs = MyJobs()
        print(jobs.types)  # ['send_email', 'process_payment', 'generate_report']
    """

    resources: dict[str, Resource] = {}

    def __init__(self):
        """
        Initialize and validate all registered job types.

        Performs validation to ensure all annotated job types:
        - Have an 'execute' method
        - The execute method is callable
        - The execute method accepts **kwargs

        Raises:
            TypeError: If any job type fails validation
        """
        for job_name in self.__annotations__:
            job_type = self.__annotations__[job_name]

            if not hasattr(job_type, 'execute'):
                raise TypeError(f"{job_type.__name__} missing 'execute' method")

            execute_method = getattr(job_type, 'execute')

            if not callable(execute_method):
                raise TypeError(f"{job_type.__name__}.execute is not callable")

            sig = inspect.signature(execute_method)

            has_kwargs = any(
                param.kind == inspect.Parameter.VAR_KEYWORD
                for param in sig.parameters.values()
            )

            if not has_kwargs:
                raise TypeError(f"{job_type.__name__}.execute must accept **kwargs")

    @property
    def types(self):
        """
        Get list of all registered job type names.

        Returns:
            List of job type names (excludes 'resources')
        """
        return [k for k in self.__annotations__.keys() if k != 'resources']

    def get_resources_for_job(self, job_type: str) -> dict[str, Resource]:
        """
        Get the resources required by a specific job type.

        Args:
            job_type: Name of the job type

        Returns:
            Dictionary mapping resource names to Resource instances for only
            the resources required by this job type

        Raises:
            ValueError: If job_type is not found in registered types
        """
        if job_type not in self.__annotations__:
            raise ValueError(f"Job type '{job_type}' not found")

        job_class = self.__annotations__[job_type]

        if not hasattr(job_class, 'required_resources'):
            return {}

        required = job_class.required_resources
        return {key: self.resources[key] for key in required if key in self.resources}


class Message(AnnotatedDict):
    """
    Encapsulates a job request with metadata.

    Attributes:
        id: Unique identifier for tracking this message through the system
        job_type: String name of the job type to execute
        payload: Dictionary of keyword arguments to pass to the job's execute method
        priority: Priority of the message
    """
    id: UUID
    job_type: str
    payload: dict
    priority: int = 5


class Response(AnnotatedDict):
    """
    Encapsulates the result of executing a job.

    Attributes:
        id: UUID matching the original Message id
        success: True if job completed without exception, False otherwise
        error: Error message string if success is False, empty string otherwise
        result: Return value from job's execute method if successful, None otherwise
    """
    id: UUID
    success: bool
    error: str
    result: Any

# TODO: Documentation
class BatchResponse(AnnotatedDict):
    responses: dict[str, Response]
    timed_out: dict[str, Response]


class Executor:
    """
    Manages background execution of jobs from a queue using a thread pool.

    The Executor watches a queue for incoming messages, spawns threads to execute
    the corresponding jobs, and stores results in a shared response map. It handles
    resource acquisition and exception handling automatically.

    Attributes:
        queue: Queue instance containing Message objects to process
        job_types: Jobs instance providing job class definitions and resources
        response_map: Shared dictionary mapping message IDs to Response objects
        running: Boolean flag controlling the watch loop
        thread_pool: ThreadPoolExecutor for parallel job execution
        worker_thread: Background thread running the watch loop

    Usage:
        executor = Executor(queue, job_types, max_workers=10)
        response_map = {}
        executor.start(response_map)

        # Later...
        executor.stop()
    """

    def __init__(self, queue: PriorityQueue, job_types: Jobs, max_workers: int = 5):
        """
        Initialize the executor.

        Args:
            queue: Queue to watch for incoming messages
            job_types: Jobs instance containing job definitions and resources
            max_workers: Maximum number of concurrent job executions
        """
        self.queue: PriorityQueue = queue
        self.job_types = job_types
        self.response_map: Dict[UUID, Response] = {}
        self.running = False
        self.thread_pool = ThreadPoolExecutor(max_workers=max_workers)

    def start(self, response_map: Dict[UUID, Response]):
        """
        Start the background worker thread.

        Args:
            response_map: Shared dictionary where responses will be stored.
                         This must be the same dict used by MessageQueue.receive()
        """
        self.response_map = response_map
        self.running = True
        self.worker_thread = Thread(target=self._watch_loop, daemon=True)
        self.worker_thread.start()

    def stop(self):
        """
        Stop the executor and wait for all in-progress jobs to complete.

        Sets the running flag to False, causing the watch loop to exit, then
        shuts down the thread pool gracefully.
        """
        self.running = False
        self.thread_pool.shutdown(wait=True)

    def _watch_loop(self):
        """
        Continuously poll the queue and submit jobs to the thread pool.

        This method runs in a background thread and checks the queue for new
        messages. When a message is found, it's submitted to the thread pool
        for execution. Sleeps briefly when the queue is empty to avoid busy-waiting.
        """
        while self.running:
            if not self.queue.empty():
                priority, counter, message = self.queue.get()
                self.thread_pool.submit(self._execute_and_store, message)
            else:
                time.sleep(0.001)

    def _execute_and_store(self, message: Message):
        """
        Execute a message and store its response in the response map.

        This is the entry point for thread pool workers. It calls _execute()
        and stores the result where MessageQueue.receive() can find it.

        Args:
            message: Message to execute
        """
        response = self._execute(message)
        self.response_map[message.id] = response

    def _execute(self, message: Message) -> Response:
        """
        Execute a single job message and return the response.

        Instantiates the job class, acquires required resources, calls execute(),
        and wraps the result or any exception in a Response object.

        Args:
            message: Message containing job type and payload

        Returns:
            Response object with success status and result or error
        """
        try:
            job_type_class = self.job_types.__annotations__[message.job_type]
            job_instance = job_type_class()

            resources = self.job_types.get_resources_for_job(message.job_type)
            result = job_instance.execute(resources=resources, **message.payload)

            if inspect.iscoroutine(result):
                try:
                    loop = asyncio.get_event_loop()
                    if loop.is_closed():
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                except RuntimeError:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)

                result = loop.run_until_complete(result)

            return Response(
                id=message.id,
                success=True,
                error="",
                result=result
            )
        except Exception as e:
            log.error(f"Error executing job '{message.id}':")
            log.error(f"  - job-type: {message.job_type}")
            log.error(f"  - payload: {message.payload}")
            log.error(f"  - error: {e}")
            log.error(f"  - traceback:\n{traceback.format_exc()}")
            return Response(
                id=message.id,
                success=False,
                error=str(e),
                result=None
            )


class MessageQueue:
    """
    Abstract base class for a message queue system with request-response pattern.

    MessageQueue provides a simple interface for sending job requests and receiving
    responses. It manages a queue, response map, and executor internally. Subclasses
    must implement the abstract methods but typically just call the parent implementation.

    The queue supports both synchronous and asynchronous receive patterns, making it
    suitable for use in both threaded and async/await contexts.

    Attributes:
        queue: Internal Queue for storing pending messages
        response_map: Shared dictionary where executor stores completed responses
        job_types: Jobs instance containing job definitions
        executor: Executor instance that processes messages

    Usage:
        class MyQueue(MessageQueue):
            pass

        class MyJobs(Jobs):
            send_email: SendEmailJob

        mq = MyQueue(MyJobs)
        mq.executor.start(mq.response_map)

        msg_id = mq.send('send_email', to='user@example.com', subject='Hello')
        response = mq.receive(msg_id, timeout=10.0)

        if response.success:
            print(response.result)
        else:
            print(f"Error: {response.error}")
    """

    def __init__(self, job_types: type[Jobs], executor: type[Executor] = Executor, auto_start: bool = True):
        """
        Initialize the message queue.

        Args:
            job_types: Jobs subclass (not instance) containing job type definitions
            executor: Executor class to use (default: Executor)
        """
        self.queue = PriorityQueue()
        self.response_map: Dict[UUID, Response] = {}
        self.job_types = job_types()
        self.executor = executor(self.queue, self.job_types)
        self._counter = 0
        self._counter_lock = Lock()
        if auto_start: self.executor.start(self.response_map)

    def send(self, job_type: str, priority: int = 5,  **kwargs) -> UUID:
        """
        Queue a job for execution.

        Creates a Message with a unique ID and the provided parameters, adds it
        to the queue, and returns the ID for later retrieval of the response.

        :param job_type: String name of the job type to execute (must be registered in Jobs)
        :param priority: Priority level of the message
        :param kwargs: Arbitrary keyword arguments to pass to the job's execute method

        Returns:
            UUID that can be used with receive() to get the response

        Raises:
            ValueError: If job_type is not registered in the Jobs instance
        """
        if not self.executor.running: log.warning(f"{self}: Sent message to queue without executor running!")
        if job_type not in self.job_types.types:
            raise ValueError(f"Invalid job type '{job_type}' not found in: {self.job_types.types}")
        message = Message(
            id=uuid.uuid4(),
            job_type=job_type,
            priority=priority,
            payload=kwargs
        )
        with self._counter_lock:
            counter = self._counter
            self._counter += 1
        self.queue.put((priority, counter, message))
        return message.id

    def receive(self, message_id: UUID, timeout: float = 30.0) -> Response:
        """
        Wait for and retrieve the response for a previously sent message.

        Polls the response_map until the response appears or timeout is reached.
        This is a blocking synchronous call suitable for threaded contexts.

        Args:
            message_id: UUID returned from send()
            timeout: Maximum seconds to wait for the response

        Returns:
            Response object containing success status and result or error.
            If timeout is reached, returns a Response with success=False and error='Timeout'
        """
        if not self.executor.running: log.warning(
            f"{self}: Attempted to receive response from queue without executor running!")
        start_time = time.time()
        while time.time() - start_time < timeout:
            if message_id in self.response_map:
                return self.response_map.pop(message_id)
            time.sleep(0.01)
        return Response(id=message_id, success=False, error="Timeout", result=None)

    async def async_receive(self, message_id: UUID, timeout: float = 30.0) -> Response:
        """
        Asynchronously wait for and retrieve the response for a previously sent message.

        Similar to receive() but uses async/await and yields control during polling,
        making it suitable for asyncio contexts.

        Args:
            message_id: UUID returned from send()
            timeout: Maximum seconds to wait for the response

        Returns:
            Response object containing success status and result or error.
            If timeout is reached, returns a Response with success=False and error='Timeout'

        Usage:
            msg_id = mq.send('process_data', data_id=123)
            response = await mq.async_receive(msg_id, timeout=5.0)
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            if message_id in self.response_map:
                return self.response_map.pop(message_id)
            await asyncio.sleep(0.01)
        return Response(id=message_id, success=False, error="Timeout", result=None)

    def send_and_receive(self, job_type: str, priority: int = 5, timeout: float = 5.0, **kwargs) -> Response:
        """
        Send a message and immediately wait for its response (convenience method).

        Combines send() and receive() into a single blocking call for simple
        request-response patterns.

        Args:
            job_type: String name of the job type to execute
            priority: Priority level (0=highest, 9=lowest, default=5)
            timeout: Maximum seconds to wait for the response
            **kwargs: Arbitrary keyword arguments to pass to the job's execute method

        Returns:
            Response object containing success status and result or error

        Raises:
            ValueError: If job_type is not registered

        Usage:
            response = mq.send_and_receive('calculate', priority=0, x=10, y=20, timeout=2.0)
            if response.success:
                print(f"Result: {response.result}")
        """
        message_id = self.send(job_type, priority=priority, **kwargs)
        return self.receive(message_id, timeout=timeout)

    def batch_send(self, messages: dict[str, Message]) -> dict[str, UUID]: #dict format rather than list for easy retrieval
        message_ids = {}
        for key in messages:
            item = messages[key]
            message_id = self.send(item.job_type, **item.payload)
            message_ids[key] = message_id
        return message_ids

    def batch_receive(self, message_ids: dict[str, UUID], min_timeout: float = 1.0, max_iteration: int = 10) -> BatchResponse:
        attempt_tracker = {key: 0 for key in message_ids.keys()}
        pending_responses: dict[str, Response | None] = {key: None for key in message_ids.keys()}
        responses: dict[str, Response] = {}
        timed_out: dict[str, Response] = {}
        start_time = time.time()

        while None in pending_responses.values():
            for key in message_ids:
                if pending_responses[key] is not None: continue
                response = self.receive(message_ids[key], 0.1)
                if response.error == "Timeout":
                    attempt_tracker[key] += 1
                else:
                    pending_responses[key] = response
                    responses[key] = response

            elapsed_time = time.time() - start_time

            if elapsed_time >= min_timeout:
                for key in list(message_ids.keys()):
                    if pending_responses[key] is None and attempt_tracker[key] >= max_iteration:
                        pending_responses.pop(key)
                        timed_out[key] = Response(id=message_ids[key], success=False, error="Timeout", result=None)

                if not any(r is None for r in pending_responses.values()):
                    break

        return BatchResponse(
            responses = responses,
            timed_out = timed_out,
        )

    def batch_send_and_receive(self, messages: dict[str, Message], min_timeout: float = 1.0, max_iteration: int = 10) -> BatchResponse:
        return self.batch_receive(self.batch_send(messages), min_timeout=min_timeout, max_iteration=max_iteration)