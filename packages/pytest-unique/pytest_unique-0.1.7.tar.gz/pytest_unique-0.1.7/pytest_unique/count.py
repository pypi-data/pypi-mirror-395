"""Counters for iterating over evenly spaced values.

Here is an example of using an in-memory counter:

    >>> counter = memory_count(10, step=2)
    >>> next(counter)
    10
    >>> next(counter)
    12
"""

from pathlib import Path

from pytest_unique.lock import FileLock


def file_count(countfile, start=0, step=1):
    """In-file counter.

    :param countfile: Path to count file for persistence.
    :param start: Optional first count, defaults to 0.
    :param step: Optional increment between counts, defaults to 1.
    :raises ValueError: On next() when the countfile doesn't contain a count.
    """
    lockfile = FileLock(countfile)
    while True:
        with lockfile:  # noqa: SIM117
            # The lock file will create the count file.
            with Path(countfile).open("r+") as f:
                data = f.read()
                count = int(data) + step if data else start

                f.seek(0)
                f.write(f"{count}")

        yield count


def memory_count(start=0, step=1):
    """In-memory counter.

    :param start: Optional first count, defaults to 0.
    :param step: Optional increment between counts, defaults to 1.
    """
    n = start
    while True:
        yield n
        n += step
