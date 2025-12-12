import ctypes
from pathlib import Path


def _find_library() -> Path:
    """Find the tokatami shared library."""
    package_dir = Path(__file__).parent
    repo_root = package_dir.parent.parent.parent

    possible_paths = [
        # Bundled in package (for installed wheels)
        package_dir / "libtokatami.so",
        package_dir / "libtokatami.dylib",
        package_dir / "tokatami.dll",
        # Development: zig-out directory
        repo_root / "zig-out" / "lib" / "libtokatami.so",
        repo_root / "zig-out" / "lib" / "libtokatami.dylib",
        repo_root / "zig-out" / "lib" / "tokatami.dll",
    ]

    for path in possible_paths:
        if path.exists():
            return path

    raise FileNotFoundError(
        f"Could not find tokatami library. "
        f"Please run 'make python' from the repository root first. "
        f"Searched in: {[str(p) for p in possible_paths]}"
    )


def _load_library() -> ctypes.CDLL:
    """Load the tokatami shared library."""
    lib_path = _find_library()
    return ctypes.CDLL(str(lib_path))


_lib = None


def _get_lib() -> ctypes.CDLL:
    """Get or load the library (lazy loading)."""
    global _lib
    if _lib is None:
        _lib = _load_library()
        _lib.tokatami_hello.restype = ctypes.c_char_p
        _lib.tokatami_hello.argtypes = []
    return _lib


def hello() -> str:
    """Return a greeting from Zig."""
    lib = _get_lib()
    result = lib.tokatami_hello()
    return result.decode("utf-8")
