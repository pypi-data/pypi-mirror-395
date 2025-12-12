import pickle
import time
import traceback
from pathlib import Path
from threading import Lock
from typing import Any

import lmdb
from annotated_dict import AnnotatedDict
from loguru import logger as log

DATABASE_CWD = Path(__file__).parent / "lmdb_store"


class LMDBEntry(AnnotatedDict):
    key: str
    ttl: int
    created_time: float
    created_by: str
    last_modified: float
    last_modified_by: str
    signature: str
    value: Any

    @classmethod
    def from_lmdb(cls, value: bytes) -> 'LMDBEntry | None':
        try:
            if value is None or not (entry := pickle.loads(value)): return None
        except Exception as e:
            raise Exception(f"Failed to deserialize LMDBEntry: {e}") from e
        if not isinstance(entry, LMDBEntry):
            raise TypeError(f"Value returned is not 'LMDBEntry', got '{entry.__class__.__name__} 'instead: {entry}")
        return entry

    @classmethod
    def from_py(cls, key: str, ttl: int, signature: str, value: Any):
        return cls(
            key=key,
            ttl=ttl,
            created_time=time.time(),
            created_by=signature,
            last_modified=time.time(),
            last_modified_by=signature,
            signature=signature,
            value=value,
        )

    @property
    def as_bytes(self):
        return pickle.dumps(self)

    def _update(self, signature: str, value: Any) -> 'LMDBEntry':
        self.last_modified = time.time()
        self.last_modified_by = signature
        self.value = value
        return self


class LMDBReceipt(AnnotatedDict):
    time_to_execute: float | None
    success: bool
    error: str | None


class LMDB:
    def __init__(self, name: str, gb_limit: float = 10.0, ttl: int = 60400):
        (path := DATABASE_CWD / name).mkdir(exist_ok=True, parents=True)
        if gb_limit <= 0 or gb_limit >= 20:
            raise ValueError("GB limit must be positive and less than 20")
        self.ttl = ttl
        self.env = lmdb.open(
            str(path),
            map_size=int(gb_limit * 1e9)
        )
        self.write_lock = Lock()

    def set(self, key: str, value: Any, signature="Anonymous") -> LMDBReceipt:
        try:
            start_time = time.perf_counter()

            if not (entry := self.get(key)):
                entry = LMDBEntry.from_py(
                    key=key,
                    ttl=self.ttl,
                    signature=signature,
                    value=value
                )
            else:
                entry._update(signature, value)

            with self.write_lock:
                with self.env.begin(write=True) as txn:
                    txn.put(key.encode(), entry.as_bytes)

            end_time = time.perf_counter()

            return LMDBReceipt(
                time_to_execute=end_time - start_time,
                success=True,
                error=None
            )

        except Exception as e:
            log.error(f"{self}: Failed to write to LMDB: {e}")
            traceback.print_exc()
            return LMDBReceipt(time_to_execute=0, success=False, error=str(e))

    def get(self, key: str) -> LMDBEntry | None:
        with self.env.begin(write=False) as txn:
            return LMDBEntry.from_lmdb(
                value=txn.get(key.encode())
            )

    def delete(self, key: str) -> LMDBReceipt:
        try:
            start_time = time.perf_counter()

            if not self.get(key):
                return LMDBReceipt(
                    time_to_execute=0,
                    success=False,
                    error=f"Key '{key}' does not exist"
                )

            with self.write_lock:
                with self.env.begin(write=True) as txn:
                    txn.delete(key.encode())

            end_time = time.perf_counter()

            return LMDBReceipt(
                time_to_execute=end_time - start_time,
                success=True,
                error=None
            )

        except Exception as e:
            log.error(f"{self}: Failed to delete from LMDB: {e}")
            traceback.print_exc()
            return LMDBReceipt(time_to_execute=0, success=False, error=str(e))

    def close(self):
        self.env.close()

    def keys(self, contains: str = None) -> list[str]:
        """
        Get all keys in the database, optionally filtered by substring.

        Args:
            contains: Optional substring to filter keys by

        Returns:
            List of keys (as strings)
        """
        with self.env.begin(write=False) as txn:
            cursor = txn.cursor()
            all_keys = [key.decode() for key, _ in cursor]

            if contains is None:
                return all_keys

            return [key for key in all_keys if contains in key]

    def items(self, contains: str = None) -> list[tuple[str, LMDBEntry]]:
        """
        Get all key-entry pairs in the database, optionally filtered by substring.

        Args:
            contains: Optional substring to filter keys by

        Returns:
            List of (key, entry) tuples
        """
        with self.env.begin(write=False) as txn:
            cursor = txn.cursor()
            all_items = [
                (key.decode(), LMDBEntry.from_lmdb(value))
                for key, value in cursor
            ]

            if contains is None:
                return all_items

            return [(k, v) for k, v in all_items if contains in k]

    def count(self, contains: str = None) -> int:
        """
        Count keys in the database, optionally filtered by substring.

        Args:
            contains: Optional substring to filter keys by

        Returns:
            Number of matching keys
        """
        return len(self.keys(contains=contains))

# TEST SUITE
# ==========
# TestLMDBEntry:
#   - test_from_py_creates_entry
#   - test_as_bytes_serializes
#   - test_update_modifies_metadata_and_value
#   - test_from_lmdb_deserializes
#   - test_from_lmdb_returns_none_for_none_input
#   - test_from_lmdb_raises_on_invalid_data
#
# TestLMDBReceipt:
#   - test_receipt_structure
#
# TestLMDB:
#   - test_init_creates_directory
#   - test_init_validates_gb_limit
#   - test_set_creates_new_entry_returns_success_receipt
#   - test_set_uses_anonymous_default
#   - test_set_updates_existing_entry
#   - test_set_returns_receipt_with_timing
#   - test_get_returns_none_for_missing_key
#   - test_get_retrieves_stored_entry
#   - test_set_get_complex_types
#   - test_ttl_stored_in_entry
#   - test_multiple_keys
#   - test_overwrite_preserves_creation_metadata
#   - test_delete_removes_entry
#   - test_delete_returns_success_receipt
#   - test_delete_nonexistent_key_returns_error_receipt
#   - test_delete_returns_receipt_with_timing
#   - test_close_closes_environment
#
# TestConcurrency:
#   - test_concurrent_writes
#   - test_concurrent_reads
#   - test_mixed_read_write
#   - test_concurrent_deletes

import pytest


@pytest.fixture(scope="function")
def mock_db():
    db = LMDB("test_db", gb_limit=1.0, ttl=3600)
    yield db
    db.close()
    import shutil
    db_path = Path(__file__).parent / "lmdb_store" / "test_db"
    if db_path.exists():
        shutil.rmtree(db_path)


@pytest.fixture(scope="function")
def temp_db():
    import uuid
    db_name = f"test_{uuid.uuid4().hex[:8]}"
    db = LMDB(db_name, gb_limit=1.0, ttl=3600)
    yield db
    db.close()
    import shutil
    db_path = Path(__file__).parent / "lmdb_store" / db_name
    if db_path.exists():
        shutil.rmtree(db_path)


class TestLMDBEntry:
    def test_from_py_creates_entry(self):
        entry = LMDBEntry.from_py(
            key="test_key",
            ttl=3600,
            signature="test_user",
            value={"data": "value"}
        )

        assert entry.key == "test_key"
        assert entry.ttl == 3600
        assert entry.signature == "test_user"
        assert entry.value == {"data": "value"}
        assert entry.created_by == "test_user"
        assert entry.last_modified_by == "test_user"
        assert isinstance(entry.created_time, float)
        assert isinstance(entry.last_modified, float)

    def test_as_bytes_serializes(self):
        entry = LMDBEntry.from_py(
            key="test", ttl=100, signature="user", value="data"
        )

        serialized = entry.as_bytes
        assert isinstance(serialized, bytes)

        deserialized = pickle.loads(serialized)
        assert isinstance(deserialized, LMDBEntry)
        assert deserialized.key == "test"
        assert deserialized.value == "data"

    def test_update_modifies_metadata_and_value(self):
        entry = LMDBEntry.from_py(
            key="test", ttl=100, signature="user1", value="data1"
        )

        original_modified = entry.last_modified
        time.sleep(0.01)

        result = entry._update("user2", "data2")

        assert result is entry
        assert entry.value == "data2"
        assert entry.last_modified_by == "user2"
        assert entry.last_modified > original_modified
        assert entry.created_by == "user1"

    def test_from_lmdb_deserializes(self):
        original = LMDBEntry.from_py(
            key="test", ttl=100, signature="user", value={"nested": "data"}
        )

        serialized = original.as_bytes
        restored = LMDBEntry.from_lmdb(value=serialized)

        assert restored.key == "test"
        assert restored.value == {"nested": "data"}
        assert restored.signature == "user"

    def test_from_lmdb_returns_none_for_none_input(self):
        result = LMDBEntry.from_lmdb(value=None)
        assert result is None

    def test_from_lmdb_raises_on_invalid_data(self):
        invalid_data = pickle.dumps({"not": "an_entry"})

        with pytest.raises(TypeError):
            LMDBEntry.from_lmdb(value=invalid_data)


class TestLMDBReceipt:
    def test_receipt_structure(self):
        receipt = LMDBReceipt(
            time_to_execute=0.123,
            success=True,
            error=None
        )

        assert receipt.time_to_execute == 0.123
        assert receipt.success is True
        assert receipt.error is None


class TestLMDB:
    def test_init_creates_directory(self, temp_db):
        db_path = Path(__file__).parent / "lmdb_store"
        assert db_path.exists()

    def test_init_validates_gb_limit(self):
        with pytest.raises(ValueError, match="GB limit must be positive and less than 20"):
            LMDB("invalid", gb_limit=0)

        with pytest.raises(ValueError, match="GB limit must be positive and less than 20"):
            LMDB("invalid", gb_limit=25)

    def test_set_creates_new_entry_returns_success_receipt(self, temp_db):
        receipt = temp_db.set("key1", "value1", signature="user1")

        assert receipt.success is True
        assert receipt.error is None
        assert receipt.time_to_execute > 0

        entry = temp_db.get("key1")
        assert entry is not None
        assert entry.key == "key1"
        assert entry.value == "value1"
        assert entry.created_by == "user1"
        assert entry.last_modified_by == "user1"

    def test_set_uses_anonymous_default(self, temp_db):
        temp_db.set("key1", "value1")

        entry = temp_db.get("key1")
        assert entry.created_by == "Anonymous"

    def test_set_updates_existing_entry(self, temp_db):
        temp_db.set("key1", "value1", signature="user1")

        original_entry = temp_db.get("key1")
        original_time = original_entry.last_modified

        time.sleep(0.01)
        temp_db.set("key1", "value2", signature="user2")

        updated_entry = temp_db.get("key1")
        assert updated_entry.value == "value2"
        assert updated_entry.last_modified > original_time
        assert updated_entry.last_modified_by == "user2"
        assert updated_entry.created_by == "user1"

    def test_set_returns_receipt_with_timing(self, temp_db):
        receipt = temp_db.set("key1", "value1")

        assert isinstance(receipt.time_to_execute, float)
        assert receipt.time_to_execute > 0

    def test_get_returns_none_for_missing_key(self, temp_db):
        result = temp_db.get("nonexistent")
        assert result is None

    def test_get_retrieves_stored_entry(self, temp_db):
        temp_db.set("key1", {"nested": "data"}, signature="user1")

        entry = temp_db.get("key1")
        assert entry.key == "key1"
        assert entry.value == {"nested": "data"}

    def test_set_get_complex_types(self, temp_db):
        complex_data = {
            "list": [1, 2, 3],
            "dict": {"a": "b"},
            "tuple": (1, 2),
            "nested": {"deep": {"value": 123}}
        }

        temp_db.set("complex", complex_data, signature="test")
        entry = temp_db.get("complex")

        assert entry.value == complex_data

    def test_ttl_stored_in_entry(self, temp_db):
        temp_db.set("key1", "value1")

        entry = temp_db.get("key1")
        assert entry.ttl == temp_db.ttl

    def test_multiple_keys(self, temp_db):
        temp_db.set("key1", "value1", signature="user1")
        temp_db.set("key2", "value2", signature="user2")
        temp_db.set("key3", "value3", signature="user3")

        assert temp_db.get("key1").value == "value1"
        assert temp_db.get("key2").value == "value2"
        assert temp_db.get("key3").value == "value3"

    def test_overwrite_preserves_creation_metadata(self, temp_db):
        temp_db.set("key1", "original", signature="creator")
        time.sleep(0.01)
        temp_db.set("key1", "updated", signature="updater")

        entry = temp_db.get("key1")
        assert entry.value == "updated"
        assert entry.created_by == "creator"
        assert entry.last_modified_by == "updater"

    def test_delete_removes_entry(self, temp_db):
        temp_db.set("key1", "value1")
        assert temp_db.get("key1") is not None

        receipt = temp_db.delete("key1")

        assert receipt.success is True
        assert temp_db.get("key1") is None

    def test_delete_returns_success_receipt(self, temp_db):
        temp_db.set("key1", "value1")
        receipt = temp_db.delete("key1")

        assert receipt.success is True
        assert receipt.error is None
        assert receipt.time_to_execute > 0

    def test_delete_nonexistent_key_returns_error_receipt(self, temp_db):
        receipt = temp_db.delete("nonexistent")

        assert receipt.success is False
        assert "does not exist" in receipt.error
        assert receipt.time_to_execute == 0

    def test_delete_returns_receipt_with_timing(self, temp_db):
        temp_db.set("key1", "value1")
        receipt = temp_db.delete("key1")

        assert isinstance(receipt.time_to_execute, float)
        assert receipt.time_to_execute > 0

    def test_close_closes_environment(self, temp_db):
        temp_db.close()

        receipt = temp_db.set("key", "value")
        assert receipt.success is False
        assert "closed" in receipt.error.lower() or "deleted" in receipt.error.lower()

    def test_keys_returns_all_keys(self, temp_db):
        temp_db.set("key1", "value1")
        temp_db.set("key2", "value2")
        temp_db.set("key3", "value3")

        keys = temp_db.keys()
        assert len(keys) == 3
        assert "key1" in keys
        assert "key2" in keys
        assert "key3" in keys

    def test_keys_filters_by_substring(self, temp_db):
        temp_db.set("user:123", "alice")
        temp_db.set("user:456", "bob")
        temp_db.set("product:789", "widget")

        user_keys = temp_db.keys(contains="user")
        assert len(user_keys) == 2
        assert "user:123" in user_keys
        assert "user:456" in user_keys
        assert "product:789" not in user_keys

    def test_keys_empty_database(self, temp_db):
        keys = temp_db.keys()
        assert keys == []

    def test_items_returns_all_entries(self, temp_db):
        temp_db.set("key1", "value1")
        temp_db.set("key2", "value2")

        items = temp_db.items()
        assert len(items) == 2

        keys = [k for k, _ in items]
        assert "key1" in keys
        assert "key2" in keys

        values = [v.value for _, v in items]
        assert "value1" in values
        assert "value2" in values

    def test_items_filters_by_substring(self, temp_db):
        temp_db.set("user:123", {"name": "alice"})
        temp_db.set("user:456", {"name": "bob"})
        temp_db.set("product:789", {"name": "widget"})

        user_items = temp_db.items(contains="user")
        assert len(user_items) == 2

        keys = [k for k, _ in user_items]
        assert "user:123" in keys
        assert "product:789" not in keys

    def test_count_returns_total(self, temp_db):
        temp_db.set("key1", "value1")
        temp_db.set("key2", "value2")
        temp_db.set("key3", "value3")

        assert temp_db.count() == 3

    def test_count_filters_by_substring(self, temp_db):
        temp_db.set("user:123", "alice")
        temp_db.set("user:456", "bob")
        temp_db.set("product:789", "widget")

        assert temp_db.count(contains="user") == 2
        assert temp_db.count(contains="product") == 1
        assert temp_db.count(contains="missing") == 0

class TestConcurrency:
    def test_concurrent_writes(self, temp_db):
        import threading

        def write_values(thread_id):
            for i in range(10):
                temp_db.set(f"key_{thread_id}_{i}", f"value_{i}", signature=f"thread_{thread_id}")

        threads = [threading.Thread(target=write_values, args=(i,)) for i in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        for thread_id in range(5):
            for i in range(10):
                entry = temp_db.get(f"key_{thread_id}_{i}")
                assert entry is not None
                assert entry.value == f"value_{i}"

    def test_concurrent_reads(self, temp_db):
        temp_db.set("shared_key", "shared_value")

        results = []

        def read_value():
            entry = temp_db.get("shared_key")
            results.append(entry.value if entry else None)

        import threading
        threads = [threading.Thread(target=read_value) for _ in range(20)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert all(r == "shared_value" for r in results)

    def test_mixed_read_write(self, temp_db):
        temp_db.set("counter", 0)

        def increment():
            for _ in range(10):
                entry = temp_db.get("counter")
                temp_db.set("counter", entry.value + 1, signature="incrementer")

        import threading
        threads = [threading.Thread(target=increment) for _ in range(3)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        final_entry = temp_db.get("counter")
        assert final_entry.value >= 10

    def test_concurrent_deletes(self, temp_db):
        import threading

        for i in range(20):
            temp_db.set(f"key_{i}", f"value_{i}")

        def delete_values(start, end):
            for i in range(start, end):
                temp_db.delete(f"key_{i}")

        threads = [
            threading.Thread(target=delete_values, args=(0, 10)),
            threading.Thread(target=delete_values, args=(10, 20))
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        for i in range(20):
            assert temp_db.get(f"key_{i}") is None
