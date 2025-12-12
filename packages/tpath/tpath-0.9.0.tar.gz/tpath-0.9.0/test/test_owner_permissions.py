import pathlib

from tpath._core import TPath


def test_access_mode_all_windows(monkeypatch, tmp_path: pathlib.Path):
    monkeypatch.setattr("platform.system", lambda: "Windows")

    f: pathlib.Path = tmp_path / "file.txt"
    f.write_text("x")

    p: TPath = TPath(str(f))

    # on Windows executable is implemented as exists check, so this should hold:
    assert p.executable is True
    # read and write depend on os.access under test runner; usually True for tmp_path file
    assert p.access_mode("ALL") == (p.readable and p.writable and p.executable)
