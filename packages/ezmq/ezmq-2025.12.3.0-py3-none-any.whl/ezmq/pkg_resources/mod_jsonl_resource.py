import json
import tempfile
import time
import signal
import subprocess
import sys
import os
from pathlib import Path

import pytest
from loguru import logger as log
from .. import Resource


class JSONLResource(Resource):
    def __init__(self, identifier: str, cwd: Path = Path.cwd(), initial_data: list[dict] = None):
        if not identifier:
            identifier = self.__class__.__name__.lower()
        if not cwd.is_dir():
            raise FileExistsError("Param 'cwd' must be a directory")

        self.identifier = identifier
        self.cwd = cwd
        self.file_path = self.cwd / f"{self.identifier}.jsonl"

        self.file_path.parent.mkdir(parents=True, exist_ok=True)

        super().__init__(identifier=identifier)

        #Attempt to fill with initial data if specified
        self.data: list[dict] = []
        if not self.peek() and initial_data:
            if not isinstance(initial_data, list):
                raise TypeError(f"Initial data must be list of dicts, got {initial_data} instead")
            with self as data:
                data.extend(initial_data)

    def _enter(self):
        self.data = []
        if self.file_path.exists():
            max_retries = 100
            retry_delay = 0.01

            for attempt in range(max_retries):
                try:
                    with self.file_path.open('r') as f:
                        for line_num, line in enumerate(f, 1):
                            line = line.strip()
                            if line:
                                try:
                                    self.data.append(json.loads(line))
                                except json.JSONDecodeError as e:
                                    log.warning(f"Skipping corrupted line {line_num}: {e}")
                    break
                except (FileNotFoundError, PermissionError) as e:
                    if attempt < max_retries - 1:
                        time.sleep(retry_delay)
                        retry_delay *= 2
                    else:
                        log.warning(f"Could not read file after {max_retries} attempts: {e}")
                except Exception as e:
                    log.error(f"Failed to read JSONL file: {e}")
                    raise
        return self.data

    def _exit(self):
        with tempfile.NamedTemporaryFile(
                mode='w',
                dir=self.file_path.parent,
                delete=False,
                encoding='utf-8',
                suffix='.jsonl'
        ) as temp_file:
            for record in self.data:
                temp_file.write(json.dumps(record) + '\n')
            temp_filename = temp_file.name

        max_retries = 10
        retry_delay = 0.01

        for attempt in range(max_retries):
            try:
                if sys.platform == 'win32':
                    if self.file_path.exists():
                        try:
                            self.file_path.unlink()
                        except PermissionError:
                            if attempt < max_retries - 1:
                                time.sleep(retry_delay)
                                continue
                            raise
                    Path(temp_filename).rename(self.file_path)
                else:
                    Path(temp_filename).replace(self.file_path)
                break
            except (OSError, PermissionError) as e:
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    retry_delay *= 2
                else:
                    log.error(f"Error replacing file after {max_retries} attempts: {e}")
                    Path(temp_filename).unlink(missing_ok=True)
                    raise

    def _peek(self):
        if self.file_path.exists():
            data = []
            max_retries = 5
            retry_delay = 0.01

            for attempt in range(max_retries):
                try:
                    with self.file_path.open('r') as f:
                        for line_num, line in enumerate(f, 1):
                            line = line.strip()
                            if line:
                                try:
                                    data.append(json.loads(line))
                                except json.JSONDecodeError as e:
                                    log.warning(f"Peek: Skipping corrupted line {line_num}: {e}")
                    return data
                except (PermissionError, FileNotFoundError) as e:
                    if attempt < max_retries - 1:
                        time.sleep(retry_delay)
                        retry_delay *= 2
                    else:
                        log.warning(f"Could not peek file after {max_retries} attempts: {e}")
                        return []
        return []


@pytest.fixture
def temp_dir(tmp_path):
    return tmp_path


@pytest.fixture
def jsonl_resource(temp_dir):
    return JSONLResource("test_jsonl", cwd=temp_dir)


def test_basic_write_read(jsonl_resource):
    with jsonl_resource as data:
        data.append({"a": 1, "b": 2})
        data.append({"c": 3, "d": 4})

    assert jsonl_resource.peek() == [{"a": 1, "b": 2}, {"c": 3, "d": 4}]


def test_thread_safety_concurrent_writes_single_resource(temp_dir):
    """Thread safety when sharing a single Resource instance"""
    resource = JSONLResource("thread_test", cwd=temp_dir)
    errors = []

    def writer(thread_id, count):
        try:
            for i in range(count):
                with resource as data:
                    data.append({"thread": thread_id, "count": i})
                time.sleep(0.001)
        except Exception as e:
            errors.append(e)

    import threading
    threads = []
    thread_count = 10
    writes_per_thread = 20

    for i in range(thread_count):
        t = threading.Thread(target=writer, args=(i, writes_per_thread))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    assert not errors, f"Thread errors occurred: {errors}"

    final_data = resource.peek()
    assert len(final_data) == thread_count * writes_per_thread

    thread_counts = {}
    for record in final_data:
        thread_id = record['thread']
        thread_counts[thread_id] = thread_counts.get(thread_id, 0) + 1

    for thread_id in range(thread_count):
        assert thread_counts[thread_id] == writes_per_thread


def test_thread_safety_read_while_write(temp_dir):
    resource = JSONLResource("read_write_test", cwd=temp_dir)
    errors = []
    read_results = []

    def writer():
        try:
            for i in range(50):
                with resource as data:
                    data.append({"write": i})
                time.sleep(0.01)
        except Exception as e:
            errors.append(('writer', e))

    def reader():
        try:
            for _ in range(100):
                data = resource.peek()
                read_results.append(len(data))
                time.sleep(0.005)
        except Exception as e:
            errors.append(('reader', e))

    import threading
    writer_thread = threading.Thread(target=writer)
    reader_threads = [threading.Thread(target=reader) for _ in range(3)]

    writer_thread.start()
    for t in reader_threads:
        t.start()

    writer_thread.join()
    for t in reader_threads:
        t.join()

    assert not errors, f"Thread errors: {errors}"

    final_data = resource.peek()
    assert len(final_data) == 50

    assert max(read_results) <= 50
    assert all(isinstance(x, int) for x in read_results)


def test_corrupted_line_recovery(temp_dir):
    resource = JSONLResource("corrupted_test", cwd=temp_dir)

    with resource as data:
        data.append({"valid": 1})

    with resource.file_path.open('a') as f:
        f.write('{"invalid": json syntax\n')
        f.write('incomplete line without newline')

    with resource.file_path.open('a') as f:
        f.write('\n{"valid": 2}\n')

    data = resource.peek()
    assert len(data) >= 2
    assert {"valid": 1} in data
    assert {"valid": 2} in data


def test_partial_write_atomicity(temp_dir):
    resource = JSONLResource("atomic_test", cwd=temp_dir)

    with resource as data:
        data.append({"initial": 1})
        data.append({"initial": 2})

    class WriteInterruptException(Exception):
        pass

    if sys.platform == 'win32':
        original_unlink = Path.unlink

        def failing_unlink(self, *args, **kwargs):
            raise WriteInterruptException("Simulated crash during unlink")

        Path.unlink = failing_unlink
    else:
        original_replace = Path.replace

        def failing_replace(self, target):
            raise WriteInterruptException("Simulated crash during replace")

        Path.replace = original_replace

    try:
        with pytest.raises(WriteInterruptException):
            with resource as data:
                data.append({"new": 3})
    finally:
        if sys.platform == 'win32':
            Path.unlink = original_unlink
        else:
            Path.replace = original_replace

    recovered_data = resource.peek()
    assert recovered_data == [{"initial": 1}, {"initial": 2}]


def test_keyboard_interrupt_simulation(temp_dir):
    test_script = f'''
import sys
import time
from pathlib import Path

sys.path.insert(0, r"{Path(__file__).parent.parent}")

from pkg_resources.mod_jsonl_resource import JSONLResource

resource = JSONLResource("interrupt_test", cwd=Path(r"{temp_dir}"))

with resource as data:
    data.append({{"before_interrupt": 1}})

sys.stdout.write("CHECKPOINT_1\\n")
sys.stdout.flush()

time.sleep(10)
'''

    script_path = temp_dir / "test_interrupt_script.py"
    script_path.write_text(test_script)

    proc = subprocess.Popen(
        [sys.executable, str(script_path)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    time.sleep(0.5)

    stdout_data = []
    while True:
        line = proc.stdout.readline()
        if "CHECKPOINT_1" in line:
            break
        if line == '' and proc.poll() is not None:
            break
        time.sleep(0.1)

    proc.terminate()
    proc.wait(timeout=3)

    resource = JSONLResource("interrupt_test", cwd=temp_dir)
    data = resource.peek()

    assert len(data) >= 1, f"Expected data but got: {data}"
    assert {"before_interrupt": 1} in data


def test_empty_file_handling(temp_dir):
    resource = JSONLResource("empty_test", cwd=temp_dir)
    resource.file_path.touch()

    data = resource.peek()
    assert data == []

    with resource as data:
        data.append({"first": 1})

    assert resource.peek() == [{"first": 1}]


def test_multiple_resource_instances_same_file(temp_dir):
    """
    EXPECTED BEHAVIOR: Multiple Resource instances = lost updates.
    This is BY DESIGN - each instance has its own lock.
    Users must share a single Resource instance for thread safety.
    """
    errors = []
    success_count = []

    def create_and_write(thread_id):
        try:
            resource = JSONLResource("multi_instance_test", cwd=temp_dir)
            with resource as data:
                data.append({"thread": thread_id})
            success_count.append(thread_id)
        except Exception as e:
            errors.append((thread_id, e))

    import threading
    threads = [threading.Thread(target=create_and_write, args=(i,)) for i in range(10)]

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert not errors, f"Unexpected errors: {errors}"
    assert len(success_count) == 10, f"All threads should complete, got {len(success_count)}/10"

    resource = JSONLResource("multi_instance_test", cwd=temp_dir)
    data = resource.peek()

    assert len(data) < 10, f"Multiple instances cause lost updates - expected < 10, got {len(data)}"
    log.info(f"Lost update test: {len(data)}/10 records survived (expected < 10)")


def test_large_dataset_atomicity(temp_dir):
    resource = JSONLResource("large_test", cwd=temp_dir)

    large_data = [{"id": i, "data": "x" * 100} for i in range(1000)]

    with resource as data:
        data.extend(large_data)

    recovered = resource.peek()
    assert len(recovered) == 1000
    assert recovered[0] == {"id": 0, "data": "x" * 100}
    assert recovered[-1] == {"id": 999, "data": "x" * 100}

def test_initial_data_creates_file(temp_dir):
    initial_data = [{"id": 1, "name": "first"}, {"id": 2, "name": "second"}]
    resource = JSONLResource("initial_test", cwd=temp_dir, initial_data=initial_data)

    assert resource.file_path.exists()
    assert resource.peek() == initial_data


def test_initial_data_not_applied_to_existing_file(temp_dir):
    existing_data = [{"existing": "data"}]
    resource1 = JSONLResource("existing_test", cwd=temp_dir, initial_data=existing_data)

    new_initial_data = [{"new": "data"}]
    resource2 = JSONLResource("existing_test", cwd=temp_dir, initial_data=new_initial_data)

    assert resource2.peek() == existing_data


def test_initial_data_empty_list(temp_dir):
    resource = JSONLResource("empty_initial_test", cwd=temp_dir, initial_data=[])

    assert resource.peek() == []


def test_initial_data_none(temp_dir):
    resource = JSONLResource("none_initial_test", cwd=temp_dir, initial_data=None)

    assert resource.peek() == []


def test_initial_data_not_provided(temp_dir):
    resource = JSONLResource("no_initial_test", cwd=temp_dir)

    assert resource.peek() == []


def test_initial_data_invalid_type_string(temp_dir):
    with pytest.raises(TypeError, match="Initial data must be list of dicts"):
        JSONLResource("invalid_test", cwd=temp_dir, initial_data="not a list")


def test_initial_data_invalid_type_dict(temp_dir):
    with pytest.raises(TypeError, match="Initial data must be list of dicts"):
        JSONLResource("invalid_test", cwd=temp_dir, initial_data={"key": "value"})


def test_initial_data_invalid_type_number(temp_dir):
    with pytest.raises(TypeError, match="Initial data must be list of dicts"):
        JSONLResource("invalid_test", cwd=temp_dir, initial_data=123)


def test_initial_data_with_nested_structures(temp_dir):
    initial_data = [
        {"id": 1, "nested": {"key": "value"}},
        {"id": 2, "list": [1, 2, 3]}
    ]
    resource = JSONLResource("nested_test", cwd=temp_dir, initial_data=initial_data)

    assert resource.peek() == initial_data


def test_initial_data_large_dataset(temp_dir):
    initial_data = [{"id": i, "value": f"item_{i}"} for i in range(1000)]
    resource = JSONLResource("large_initial_test", cwd=temp_dir, initial_data=initial_data)

    result = resource.peek()
    assert len(result) == 1000
    assert result[0] == {"id": 0, "value": "item_0"}
    assert result[-1] == {"id": 999, "value": "item_999"}


def test_initial_data_can_be_modified_after_creation(temp_dir):
    initial_data = [{"id": 1}]
    resource = JSONLResource("modify_test", cwd=temp_dir, initial_data=initial_data)

    with resource as data:
        data.append({"id": 2})

    assert resource.peek() == [{"id": 1}, {"id": 2}]


def test_initial_data_persists_across_instances(temp_dir):
    initial_data = [{"persistent": "data"}]
    resource1 = JSONLResource("persist_test", cwd=temp_dir, initial_data=initial_data)

    resource2 = JSONLResource("persist_test", cwd=temp_dir)

    assert resource2.peek() == initial_data


def test_initial_data_with_special_characters(temp_dir):
    initial_data = [
        {"text": "Special chars: 你好, émoji 🎉"},
        {"unicode": "\u2665 \u2764"}
    ]
    resource = JSONLResource("special_chars_test", cwd=temp_dir, initial_data=initial_data)

    assert resource.peek() == initial_data


def test_initial_data_preserves_types(temp_dir):
    initial_data = [
        {"string": "text", "number": 42, "float": 3.14, "bool": True, "null": None}
    ]
    resource = JSONLResource("types_test", cwd=temp_dir, initial_data=initial_data)

    result = resource.peek()
    assert result[0]["string"] == "text"
    assert result[0]["number"] == 42
    assert result[0]["float"] == 3.14
    assert result[0]["bool"] is True
    assert result[0]["null"] is None


def test_initial_data_empty_file_already_exists(temp_dir):
    file_path = temp_dir / "preexisting_test.jsonl"
    file_path.touch()

    initial_data = [{"should": "apply"}]
    resource = JSONLResource("preexisting_test", cwd=temp_dir, initial_data=initial_data)

    assert resource.peek() == initial_data


def test_multiple_resources_same_identifier_initial_data(temp_dir):
    initial_data1 = [{"first": "instance"}]
    resource1 = JSONLResource("shared_test", cwd=temp_dir, initial_data=initial_data1)

    initial_data2 = [{"second": "instance"}]
    resource2 = JSONLResource("shared_test", cwd=temp_dir, initial_data=initial_data2)

    assert resource1.peek() == initial_data1
    assert resource2.peek() == initial_data1


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])