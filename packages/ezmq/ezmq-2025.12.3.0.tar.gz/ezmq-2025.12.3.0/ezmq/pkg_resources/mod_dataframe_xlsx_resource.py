from pathlib import Path
import tempfile
import threading
import time
import os
import sys

import pandas
import pytest

from .. import Resource
from pandas import DataFrame


class DataFrameXLSXResource(Resource):
    def __init__(self, path: Path = None, identifier: str = None, max_retries: int = 10, retry_delay: float = 0.1):
        if path and identifier:
            self.path = path
            self.identifier = identifier
        elif path and not identifier:
            self.path = path
            if not self.path.exists():
                raise FileNotFoundError(f"File '{path}' does not exist")
            self.identifier = path.stem
        elif not path and identifier:
            self.path = Path.cwd() / f"{identifier}.xlsx"
            self.identifier = identifier
        else:
            raise ValueError("Either path or identifier must be specified")

        if not self.path.suffix == ".xlsx":
            raise ValueError(f"Path must be an xlsx file, got {self.path} instead")

        if not self.path.exists():
            pandas.DataFrame().to_excel(self.path, index=False)

        self.data: DataFrame = None #type: ignore
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self._load_with_retry()

        super().__init__(identifier=self.identifier)

    def _load_with_retry(self):
        attempts = 0
        last_error = None

        while attempts <= self.max_retries:
            try:
                self.data = pandas.read_excel(self.path)
                return
            except PermissionError as e:
                last_error = e
                attempts += 1
                if attempts <= self.max_retries:
                    time.sleep(self.retry_delay)

        raise PermissionError(f"Failed to read {self.path} after {self.max_retries} attempts") from last_error

    def _enter(self) -> DataFrame:
        self.data = pandas.read_excel(self.path)
        return self.data

    def _exit(self):
        self.data.to_excel(self.path, index=False)

    def _peek(self) -> DataFrame:
        return pandas.read_excel(self.path)


@pytest.fixture
def temp_xlsx_path():
    with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as f:
        path = Path(f.name)

    pandas.DataFrame().to_excel(path, index=False)
    yield path

    if path.exists():
        try:
            path.unlink()
        except PermissionError:
            time.sleep(0.5)
            path.unlink()


@pytest.fixture
def df_xlsx_resource(temp_xlsx_path):
    return DataFrameXLSXResource(path=temp_xlsx_path, identifier="test_resource")


def test_resource_initialization_with_both_args(temp_xlsx_path):
    resource = DataFrameXLSXResource(path=temp_xlsx_path, identifier="custom_id")
    assert resource.identifier == "custom_id"
    assert resource.path == temp_xlsx_path


def test_resource_initialization_with_path_only(temp_xlsx_path):
    resource = DataFrameXLSXResource(path=temp_xlsx_path)
    assert resource.identifier == temp_xlsx_path.stem


def test_resource_initialization_with_identifier_only():
    identifier = "test_identifier"
    resource = DataFrameXLSXResource(identifier=identifier)
    expected_path = Path.cwd() / f"{identifier}.xlsx"

    assert resource.identifier == identifier
    assert resource.path == expected_path
    assert resource.path.exists()

    expected_path.unlink()


def test_resource_initialization_with_no_args():
    with pytest.raises(ValueError, match="Either path or identifier must be specified"):
        DataFrameXLSXResource()


def test_resource_initialization_with_non_xlsx_path():
    path = Path("test.csv")
    with pytest.raises(FileNotFoundError):
        DataFrameXLSXResource(path=path)


def test_context_manager_basic_read_write(df_xlsx_resource):
    test_data = DataFrame({"name": ["Alice", "Bob"], "age": [25, 30]})

    with df_xlsx_resource as df:
        df["name"] = test_data["name"]
        df["age"] = test_data["age"]

    loaded_data = pandas.read_excel(df_xlsx_resource.path)
    pandas.testing.assert_frame_equal(loaded_data, test_data)


def test_context_manager_appends_data(df_xlsx_resource):
    initial_data = DataFrame({"value": [1, 2, 3]})
    initial_data.to_excel(df_xlsx_resource.path, index=False)

    with df_xlsx_resource as df:
        new_row = pandas.DataFrame({"value": [4]})
        df_xlsx_resource.data = pandas.concat([df, new_row], ignore_index=True)

    loaded_data = pandas.read_excel(df_xlsx_resource.path)
    assert len(loaded_data) == 4
    assert loaded_data["value"].tolist() == [1, 2, 3, 4]


def test_context_manager_modifies_in_place(df_xlsx_resource):
    initial_data = DataFrame({"value": [1, 2, 3]})
    initial_data.to_excel(df_xlsx_resource.path, index=False)

    with df_xlsx_resource as df:
        df["value"] = df["value"] * 2

    loaded_data = pandas.read_excel(df_xlsx_resource.path)
    assert loaded_data["value"].tolist() == [2, 4, 6]


def test_peek_returns_current_data(df_xlsx_resource):
    test_data = DataFrame({"col": ["x", "y", "z"]})
    test_data.to_excel(df_xlsx_resource.path, index=False)

    peeked_data = df_xlsx_resource.peek()
    pandas.testing.assert_frame_equal(peeked_data, test_data)


def test_peek_does_not_lock(df_xlsx_resource):
    test_data = DataFrame({"value": [1]})
    test_data.to_excel(df_xlsx_resource.path, index=False)

    with df_xlsx_resource as df:
        peeked = df_xlsx_resource.peek()
        assert "value" in peeked.columns


def test_concurrent_access_with_locking(df_xlsx_resource):
    results = []
    errors = []

    def writer_task(resource, value, delay=0):
        try:
            time.sleep(delay)
            with resource as df:
                df["counter"] = [value]
                time.sleep(0.1)
            results.append(value)
        except Exception as e:
            errors.append(e)

    threads = [
        threading.Thread(target=writer_task, args=(df_xlsx_resource, i, i * 0.05))
        for i in range(5)
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    assert len(errors) == 0
    assert len(results) == 5

    final_data = pandas.read_excel(df_xlsx_resource.path)
    assert final_data["counter"].iloc[0] in range(5)


def test_timeout_on_lock_acquisition(df_xlsx_resource):
    df_xlsx_resource.timeout = 0.5

    def blocking_task():
        with df_xlsx_resource as df:
            time.sleep(2)

    thread = threading.Thread(target=blocking_task)
    thread.start()

    time.sleep(0.1)

    with pytest.raises(TimeoutError, match="Could not acquire"):
        with df_xlsx_resource as df:
            pass

    thread.join()


def test_multiple_sequential_accesses(df_xlsx_resource):
    for i in range(3):
        with df_xlsx_resource as df:
            df["iteration"] = [i]

        loaded = pandas.read_excel(df_xlsx_resource.path)
        assert loaded["iteration"].iloc[0] == i


def test_resource_state_persists_between_contexts(df_xlsx_resource):
    with df_xlsx_resource as df:
        df["step"] = [1]

    with df_xlsx_resource as df:
        assert df["step"].iloc[0] == 1
        df["step"] = [2]

    final_data = pandas.read_excel(df_xlsx_resource.path)
    assert final_data["step"].iloc[0] == 2


def test_concurrent_readers_with_peek(df_xlsx_resource):
    test_data = DataFrame({"value": [100]})
    test_data.to_excel(df_xlsx_resource.path, index=False)

    results = []

    def reader_task():
        for _ in range(10):
            peeked = df_xlsx_resource.peek()
            results.append(peeked["value"].iloc[0])
            time.sleep(0.01)

    threads = [threading.Thread(target=reader_task) for _ in range(3)]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    assert all(value == 100 for value in results)
    assert len(results) == 30


def test_retry_logic_with_mock(temp_xlsx_path, monkeypatch):
    test_data = DataFrame({"value": [1, 2, 3]})
    test_data.to_excel(temp_xlsx_path, index=False)

    original_read = pandas.read_excel
    call_count = [0]

    def failing_read(*args, **kwargs):
        call_count[0] += 1
        if call_count[0] <= 3:
            raise PermissionError("Simulated lock")
        return original_read(*args, **kwargs)

    monkeypatch.setattr(pandas, "read_excel", failing_read)

    resource = DataFrameXLSXResource(path=temp_xlsx_path, max_retries=10, retry_delay=0.05)

    assert resource.data is not None
    assert len(resource.data) == 3
    assert call_count[0] == 4


def test_retry_logic_exceeds_max_attempts(temp_xlsx_path, monkeypatch):
    test_data = DataFrame({"value": [1, 2, 3]})
    test_data.to_excel(temp_xlsx_path, index=False)

    def always_failing_read(*args, **kwargs):
        raise PermissionError("Persistent lock")

    monkeypatch.setattr(pandas, "read_excel", always_failing_read)

    with pytest.raises(PermissionError, match="Failed to read .* after 3 attempts"):
        DataFrameXLSXResource(path=temp_xlsx_path, max_retries=3, retry_delay=0.05)


def test_retry_logic_custom_parameters():
    identifier = "test_retry_custom"
    resource = DataFrameXLSXResource(identifier=identifier, max_retries=5, retry_delay=0.2)

    assert resource.max_retries == 5
    assert resource.retry_delay == 0.2
    assert resource.data is not None

    resource.path.unlink()


def test_no_retry_needed_for_available_file(temp_xlsx_path):
    start_time = time.time()
    resource = DataFrameXLSXResource(path=temp_xlsx_path, max_retries=10, retry_delay=0.5)
    elapsed = time.time() - start_time

    assert elapsed < 0.1
    assert resource.data is not None


@pytest.mark.skipif(sys.platform != "win32", reason="Windows-specific test")
def test_retry_with_write_lock(temp_xlsx_path):
    import msvcrt

    test_data = DataFrame({"value": [1, 2, 3]})
    test_data.to_excel(temp_xlsx_path, index=False)

    lock_released = threading.Event()

    def file_locker():
        with open(temp_xlsx_path, 'r+b') as f:
            msvcrt.locking(f.fileno(), msvcrt.LK_NBLCK, 1)
            time.sleep(0.3)
            msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)
        lock_released.set()

    locker_thread = threading.Thread(target=file_locker)
    locker_thread.start()

    time.sleep(0.1)

    resource = DataFrameXLSXResource(path=temp_xlsx_path, max_retries=10, retry_delay=0.1)

    locker_thread.join()

    assert resource.data is not None
    assert len(resource.data) == 3
    assert lock_released.is_set()