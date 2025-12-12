import json
import os
from pathlib import Path
from loguru import logger as log
from .. import Resource


class JSONResource(Resource):
    """
    Crash-safe JSON file resource using atomic write.

    Writes go to <name>.json.tmp, are flushed, fsynced, and then os.replace()s
    the original. This prevents corruption from KeyboardInterrupt and partial writes.
    """

    def __init__(self, identifier: str, cwd: Path = Path.cwd(), verbose: bool = False):
        self.identifier = identifier
        self.cwd = Path(cwd)
        self.verbose = verbose
        super().__init__(identifier=identifier)

        try:
            self.file_path = self.cwd / f"{self.identifier}.json"
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
            self.file_path.touch(exist_ok=True)

            # cleanup stale temp file
            tmp_path = self.file_path.with_suffix(".json.tmp")
            if tmp_path.exists():
                tmp_path.unlink()

            if self.verbose:
                log.debug(f"[{self}]: Initialized resource at {self.file_path}")

        except Exception:
            raise

    def _enter(self):
        if self.verbose:
            log.debug(f"[{self}]: Enter context (load JSON)")

        with open(self.file_path, "r", encoding="utf-8") as f:
            content = f.read()
            return json.loads(content) if content else {}

    def _exit(self):
        if self.verbose:
            log.debug(f"[{self}]: Exit context (atomic write)")

        self._atomic_write(self._resource)

    def _peek(self):
        if self.verbose:
            log.debug(f"[{self}]: Peeking JSON file")

        with open(self.file_path, "r", encoding="utf-8") as f:
            content = f.read()
            return json.loads(content) if content else {}

    def _atomic_write(self, data):
        """Crash-safe write: temp → fsync → atomic replace."""

        tmp_path = self.file_path.with_suffix(".json.tmp")

        try:
            # Write to temp
            with open(tmp_path, "w", encoding="utf-8") as tmpf:
                json.dump(data, tmpf, indent=2, ensure_ascii=False)
                tmpf.flush()
                os.fsync(tmpf.fileno())

            # Atomic replace
            os.replace(tmp_path, self.file_path)

            # POSIX directory fsync only
            if os.name == "posix":
                try:
                    dir_fd = os.open(str(self.file_path.parent), os.O_RDONLY)
                    try:
                        os.fsync(dir_fd)
                    finally:
                        os.close(dir_fd)
                except Exception:
                    if self.verbose:
                        log.warning(f"[{self}]: Directory fsync failed or not supported")

            if self.verbose:
                log.debug(f"[{self}]: Atomic write completed successfully")

        finally:
            # best effort cleanup
            if tmp_path.exists():
                try:
                    tmp_path.unlink()
                except Exception:
                    pass

import json
import os
import pytest
from pathlib import Path
from unittest.mock import patch

@pytest.fixture
def resource(tmp_path: Path):
    """Fresh crash-safe JSONResource."""
    return JSONResource("crash_json", cwd=tmp_path, verbose=True)


def read_json(path: Path):
    if not path.exists():
        return {}
    text = path.read_text()
    return json.loads(text) if text else {}


# ---------------------------------------------------------------------------
# Normal write behavior
# ---------------------------------------------------------------------------

def test_normal_write(resource):
    with resource as data:
        data["a"] = 1
        data["b"] = {"nested": True}

    assert read_json(resource.file_path) == {"a": 1, "b": {"nested": True}}


# ---------------------------------------------------------------------------
# Crash simulation: KeyboardInterrupt BEFORE os.replace()
# ---------------------------------------------------------------------------

def test_crash_before_atomic_replace_keeps_original(resource):
    # First write valid data
    with resource as data:
        data["safe"] = True

    original = resource.file_path.read_text()

    # Simulate error during atomic write
    with patch("os.replace", side_effect=KeyboardInterrupt):
        with pytest.raises(KeyboardInterrupt):
            with resource as data:
                data["corrupt_attempt"] = 999

    # File must remain intact
    assert resource.file_path.read_text() == original
    assert read_json(resource.file_path) == {"safe": True}


# ---------------------------------------------------------------------------
# Crash simulation: fsync throws (rare, but good to test)
# ---------------------------------------------------------------------------

def test_crash_during_fsync_keeps_original(resource):
    with resource as data:
        data["initial"] = True

    original = resource.file_path.read_text()

    with patch("os.fsync", side_effect=KeyboardInterrupt):
        with pytest.raises(KeyboardInterrupt):
            with resource as data:
                data["x"] = 123

    # Original JSON intact
    assert resource.file_path.read_text() == original
    assert read_json(resource.file_path) == {"initial": True}


# ---------------------------------------------------------------------------
# Stale .tmp file cleanup
# ---------------------------------------------------------------------------

def test_stale_tmp_file_cleanup(resource):
    tmp_path = resource.file_path.with_suffix(".json.tmp")
    tmp_path.write_text('{"half_written": "oops"')

    # Creating a new instance must clean stale tmp file
    res2 = JSONResource("crash_json", cwd=resource.cwd, verbose=True)
    assert not tmp_path.exists()


# ---------------------------------------------------------------------------
# Verify _peek() loads correct JSON
# ---------------------------------------------------------------------------

def test_peek(resource):
    with resource as data:
        data["x"] = 10

    result = resource.peek()
    assert result == {"x": 10}


# ---------------------------------------------------------------------------
# Enter returns dict, exit writes dict
# ---------------------------------------------------------------------------

def test_enter_exit_behavior(resource):
    d = resource._enter()
    assert isinstance(d, dict)

    d["foo"] = "bar"
    resource._resource = d
    resource._exit()

    assert read_json(resource.file_path) == {"foo": "bar"}
