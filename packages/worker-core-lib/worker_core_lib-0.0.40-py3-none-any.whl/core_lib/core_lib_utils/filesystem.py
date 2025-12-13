import tempfile
import shutil
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

@contextmanager
def managed_temp_dir() -> Iterator[Path]:
    """
    A context manager for creating and cleaning up temporary directories.

    Yields:
        A Path object representing the temporary directory.
    """
    temp_dir = tempfile.mkdtemp()
    print(f"Created temporary directory: {temp_dir}")
    try:
        yield Path(temp_dir)
    finally:
        print(f"Cleaning up temporary directory: {temp_dir}")
        shutil.rmtree(temp_dir)