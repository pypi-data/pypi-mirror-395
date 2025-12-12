from tpath._core import TPath


def test_owner_permissions_nonexistent(tmp_path):
    # Path does not exist -> stat() will raise FileNotFoundError
    p = TPath(tmp_path / "no_such_file.txt")

    # Methods catch FileNotFoundError/OSError and should return False
    assert p.owner_readable is False
    assert p.owner_writable is False
    assert p.owner_executable is False


def test_owner_permissions_stat_raises(tmp_path, monkeypatch):
    # Create an actual file, then force its instance stat() to raise OSError
    f = tmp_path / "exists.txt"
    f.write_text("hello")

    p = TPath(str(f))

    def _raise(*a, **k):
        raise OSError("simulated stat failure")

    # Patch the instance stat method to raise OSError
    monkeypatch.setattr(p, "stat", _raise)

    # All owner_* properties should catch the OSError and return False
    assert p.owner_readable is False
    assert p.owner_writable is False
    assert p.owner_executable is False
