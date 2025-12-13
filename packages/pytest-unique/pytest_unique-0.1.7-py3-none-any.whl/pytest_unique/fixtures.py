"""Unique fixture."""

import time
from datetime import datetime, timezone
from pathlib import Path

import pytest

from pytest_unique.count import file_count
from pytest_unique.unique import Unique


@pytest.fixture(scope="session")
def unique_in_memory():
    """Memory backed unique."""
    return Unique()


@pytest.fixture(scope="session")
def unique_in_file(request):
    """File backed unique."""
    directory = Path(request.config.cache.makedir("unique"))
    countfile = directory / "count"
    # Use the current timestamp for the count start because the count can
    # be used to create artifacts in databases across test environments,
    # like users in api-stg.webarmor.io.
    start = int(time.mktime(datetime.now(timezone.utc).timetuple()))
    count = file_count(countfile, start)
    return Unique(count)


# Default to in-file counter to be more conservative.
unique = unique_in_file
