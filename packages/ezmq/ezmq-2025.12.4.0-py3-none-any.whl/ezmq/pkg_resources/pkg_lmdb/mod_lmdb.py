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
            if value is None:
                return None

            entry = pickle.loads(value)

            if not entry:
                return None

            if not isinstance(entry, LMDBEntry):
                log.warning(f"Stale pickle detected: expected LMDBEntry, got {entry.__class__.__name__}")
                return None

            return entry

        except (AttributeError, ImportError, ModuleNotFoundError) as e:
            # Class definition moved or not found - treat as cache miss
            log.warning(f"Failed to deserialize cached entry (stale pickle): {e}")
            return None

        except Exception as e:
            # Other errors should still raise
            raise Exception(f"Failed to deserialize LMDBEntry: {e}") from e

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

            entry = self.get(key)

            if entry is None:
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
            data = txn.get(key.encode())
            if data is None:
                return None

            entry = LMDBEntry.from_lmdb(value=data)

            # If entry is None (stale pickle), delete it
            if entry is None:
                log.warning(f"Removing stale cache entry: {key}")
                self._delete_raw(key)

            return entry

    def _delete_raw(self, key: str) -> bool:
        """Internal delete without existence check"""
        try:
            with self.write_lock:
                with self.env.begin(write=True) as txn:
                    return txn.delete(key.encode())
        except Exception as e:
            log.error(f"Failed to delete stale entry {key}: {e}")
            return False

    def delete(self, key: str) -> LMDBReceipt:
        try:
            start_time = time.perf_counter()

            # Check if key exists (this will also clean stale entries)
            entry = self.get(key)
            if entry is None:
                return LMDBReceipt(
                    time_to_execute=0,
                    success=False,
                    error=f"Key '{key}' does not exist"
                )

            # Key exists and is valid, delete it
            deleted = self._delete_raw(key)

            end_time = time.perf_counter()

            return LMDBReceipt(
                time_to_execute=end_time - start_time,
                success=deleted,
                error=None if deleted else "Failed to delete key"
            )

        except Exception as e:
            log.error(f"{self}: Failed to delete from LMDB: {e}")
            traceback.print_exc()
            return LMDBReceipt(time_to_execute=0, success=False, error=str(e))

    def keys(self, contains: str = None) -> list[str]:
        """Get all valid keys, automatically cleaning stale entries"""
        with self.env.begin(write=False) as txn:
            cursor = txn.cursor()
            valid_keys = []
            stale_keys = []

            for key, value in cursor:
                key_str = key.decode()

                # Try to deserialize to check if stale
                entry = LMDBEntry.from_lmdb(value=value)
                if entry is None:
                    stale_keys.append(key_str)
                    continue

                # Filter by substring if provided
                if contains is None or contains in key_str:
                    valid_keys.append(key_str)

            # Clean up stale entries
            if stale_keys:
                log.warning(f"Cleaning {len(stale_keys)} stale cache entries")
                for stale_key in stale_keys:
                    self._delete_raw(stale_key)

        return valid_keys

    def items(self, contains: str = None) -> list[tuple[str, LMDBEntry]]:
        """Get all valid key-entry pairs, automatically cleaning stale entries"""
        with self.env.begin(write=False) as txn:
            cursor = txn.cursor()
            valid_items = []
            stale_keys = []

            for key, value in cursor:
                key_str = key.decode()
                entry = LMDBEntry.from_lmdb(value=value)

                if entry is None:
                    stale_keys.append(key_str)
                    continue

                if contains is None or contains in key_str:
                    valid_items.append((key_str, entry))

            # Clean up stale entries
            if stale_keys:
                log.warning(f"Cleaning {len(stale_keys)} stale cache entries")
                for stale_key in stale_keys:
                    self._delete_raw(stale_key)

        return valid_items

    def count(self, contains: str = None) -> int:
        """Count valid keys (excluding stale entries)"""
        return len(self.keys(contains=contains))

    def clean_all_stale(self) -> int:
        """Explicitly clean all stale entries. Returns count removed."""
        stale_keys = []

        with self.env.begin(write=False) as txn:
            cursor = txn.cursor()
            for key, value in cursor:
                if LMDBEntry.from_lmdb(value=value) is None:
                    stale_keys.append(key.decode())

        for key in stale_keys:
            self._delete_raw(key)

        if stale_keys:
            log.info(f"Cleaned {len(stale_keys)} stale cache entries")

        return len(stale_keys)

    def close(self):
        self.env.close()

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

    # def test_from_lmdb_raises_on_invalid_data(self):
    #     invalid_data = pickle.dumps({"not": "an_entry"})
    #
    #     with pytest.raises(TypeError):
    #         LMDBEntry.from_lmdb(value=invalid_data)


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


# Add these test cases to the existing test suite

class TestStaleEntryHandling:
    """Tests for automatic stale pickle detection and cleanup"""

    def test_get_removes_stale_entry(self, temp_db):
        # Manually insert a stale pickle (simulating old class definition)
        stale_data = pickle.dumps({"fake": "entry"})
        with temp_db.write_lock:
            with temp_db.env.begin(write=True) as txn:
                txn.put(b"stale_key", stale_data)

        # Getting stale entry should return None and remove it
        result = temp_db.get("stale_key")
        assert result is None

        # Verify it was actually deleted
        with temp_db.env.begin(write=False) as txn:
            assert txn.get(b"stale_key") is None

    def test_keys_cleans_stale_entries(self, temp_db):
        # Add valid entries
        temp_db.set("valid1", "data1")
        temp_db.set("valid2", "data2")

        # Add stale entry
        stale_data = pickle.dumps({"fake": "entry"})
        with temp_db.write_lock:
            with temp_db.env.begin(write=True) as txn:
                txn.put(b"stale_key", stale_data)

        # keys() should only return valid keys and clean stale ones
        keys = temp_db.keys()
        assert len(keys) == 2
        assert "valid1" in keys
        assert "valid2" in keys
        assert "stale_key" not in keys

        # Verify stale was deleted
        with temp_db.env.begin(write=False) as txn:
            assert txn.get(b"stale_key") is None

    def test_items_cleans_stale_entries(self, temp_db):
        # Add valid entries
        temp_db.set("valid1", "data1")
        temp_db.set("valid2", "data2")

        # Add stale entry
        stale_data = pickle.dumps({"fake": "entry"})
        with temp_db.write_lock:
            with temp_db.env.begin(write=True) as txn:
                txn.put(b"stale_key", stale_data)

        # items() should only return valid items
        items = temp_db.items()
        assert len(items) == 2

        keys = [k for k, _ in items]
        assert "valid1" in keys
        assert "valid2" in keys
        assert "stale_key" not in keys

    def test_count_excludes_stale_entries(self, temp_db):
        # Add valid entries
        temp_db.set("valid1", "data1")
        temp_db.set("valid2", "data2")

        # Add stale entries
        for i in range(3):
            stale_data = pickle.dumps({"fake": f"entry{i}"})
            with temp_db.write_lock:
                with temp_db.env.begin(write=True) as txn:
                    txn.put(f"stale_{i}".encode(), stale_data)

        # Count should only include valid entries
        assert temp_db.count() == 2

    def test_clean_all_stale_removes_all_stale_entries(self, temp_db):
        # Add valid entries
        temp_db.set("valid1", "data1")
        temp_db.set("valid2", "data2")

        # Add multiple stale entries
        stale_count = 5
        for i in range(stale_count):
            stale_data = pickle.dumps({"fake": f"entry{i}"})
            with temp_db.write_lock:
                with temp_db.env.begin(write=True) as txn:
                    txn.put(f"stale_{i}".encode(), stale_data)

        # Clean all stale entries
        removed = temp_db.clean_all_stale()
        assert removed == stale_count

        # Only valid entries should remain
        keys = temp_db.keys()
        assert len(keys) == 2
        assert "valid1" in keys
        assert "valid2" in keys

    def test_clean_all_stale_with_no_stale_entries(self, temp_db):
        temp_db.set("valid1", "data1")
        temp_db.set("valid2", "data2")

        removed = temp_db.clean_all_stale()
        assert removed == 0
        assert temp_db.count() == 2

    def test_clean_all_stale_empty_database(self, temp_db):
        removed = temp_db.clean_all_stale()
        assert removed == 0

    def test_set_overwrites_stale_entry(self, temp_db):
        # Insert stale entry
        stale_data = pickle.dumps({"fake": "entry"})
        with temp_db.write_lock:
            with temp_db.env.begin(write=True) as txn:
                txn.put(b"my_key", stale_data)

        # Setting a new value should work (get returns None, so creates new)
        receipt = temp_db.set("my_key", "new_value")
        assert receipt.success is True

        # Should be able to retrieve the new value
        entry = temp_db.get("my_key")
        assert entry is not None
        assert entry.value == "new_value"

    def test_delete_stale_entry_returns_not_exists(self, temp_db):
        # Insert stale entry
        stale_data = pickle.dumps({"fake": "entry"})
        with temp_db.write_lock:
            with temp_db.env.begin(write=True) as txn:
                txn.put(b"stale_key", stale_data)

        # Trying to delete should return "does not exist"
        # because get() returns None for stale entries
        receipt = temp_db.delete("stale_key")
        assert receipt.success is False
        assert "does not exist" in receipt.error


class TestDeleteRaw:
    """Tests for internal _delete_raw method"""

    def test_delete_raw_removes_key(self, temp_db):
        temp_db.set("key1", "value1")

        result = temp_db._delete_raw("key1")
        assert result is True
        assert temp_db.get("key1") is None

    def test_delete_raw_nonexistent_key(self, temp_db):
        result = temp_db._delete_raw("nonexistent")
        # LMDB returns False for deleting nonexistent keys
        assert result is False

    def test_delete_raw_handles_errors_gracefully(self, temp_db):
        temp_db.close()

        # Should handle error and return False
        result = temp_db._delete_raw("any_key")
        assert result is False


class TestKeysFilteringEdgeCases:
    """Additional edge cases for keys/items/count with filtering"""

    def test_keys_with_empty_string_filter(self, temp_db):
        temp_db.set("key1", "value1")
        temp_db.set("key2", "value2")

        # Empty string should match all keys
        keys = temp_db.keys(contains="")
        assert len(keys) == 2

    def test_keys_with_special_characters(self, temp_db):
        temp_db.set("user:123:email", "test@example.com")
        temp_db.set("user:456:email", "other@example.com")
        temp_db.set("user:123:name", "Alice")

        email_keys = temp_db.keys(contains=":email")
        assert len(email_keys) == 2
        assert "user:123:email" in email_keys
        assert "user:456:email" in email_keys

    def test_items_preserves_entry_metadata(self, temp_db):
        temp_db.set("key1", "value1", signature="user1")
        time.sleep(0.01)
        temp_db.set("key2", "value2", signature="user2")

        items = temp_db.items()

        for key, entry in items:
            assert isinstance(entry, LMDBEntry)
            assert entry.key == key
            assert entry.signature in ["user1", "user2"]
            assert isinstance(entry.created_time, float)

    def test_count_with_overlapping_substrings(self, temp_db):
        temp_db.set("test", "value1")
        temp_db.set("testing", "value2")
        temp_db.set("test_case", "value3")
        temp_db.set("other", "value4")

        assert temp_db.count(contains="test") == 3
        assert temp_db.count(contains="testing") == 1
        assert temp_db.count(contains="_") == 1


class TestConcurrentStaleHandling:
    """Test stale entry handling under concurrent access"""

    def test_concurrent_reads_with_stale_entries(self, temp_db):
        import threading

        # Add valid and stale entries
        temp_db.set("valid", "data")
        stale_data = pickle.dumps({"fake": "entry"})
        with temp_db.write_lock:
            with temp_db.env.begin(write=True) as txn:
                txn.put(b"stale", stale_data)

        results = []

        def read_keys():
            keys = temp_db.keys()
            results.append(len(keys))

        threads = [threading.Thread(target=read_keys) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # All threads should see only valid key
        assert all(count == 1 for count in results)

    def test_concurrent_clean_all_stale(self, temp_db):
        import threading

        # Add stale entries
        for i in range(20):
            stale_data = pickle.dumps({"fake": f"entry{i}"})
            with temp_db.write_lock:
                with temp_db.env.begin(write=True) as txn:
                    txn.put(f"stale_{i}".encode(), stale_data)

        results = []

        def clean_stale():
            removed = temp_db.clean_all_stale()
            results.append(removed)

        # Run multiple concurrent cleanups
        threads = [threading.Thread(target=clean_stale) for _ in range(3)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # Each thread reads the stale list independently, so all might see all 20
        # The total could be anywhere from 20 (if serialized perfectly) to 60 (if all read before any delete)
        # Just verify cleanup happened and no stale entries remain
        assert sum(results) >= 20  # At least 20 were reported cleaned
        assert temp_db.count() == 0  # All stale entries are gone