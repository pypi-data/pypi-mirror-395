"""Unique data generation."""

import string
import sys
import time
from datetime import datetime, timezone
from functools import partial
from pathlib import PurePath
from random import sample
from uuid import UUID

from attr import define, field

from pytest_unique.count import memory_count
from pytest_unique.registry import registry_load


def count_factory():
    """Create a counter that increases with each unique call."""
    start = int(time.mktime(datetime.now(timezone.utc).timetuple()))
    return memory_count(start)


@define(frozen=True)
class Unique:
    """Generate data using plugins.

    Plugins are read from the `pytest_unique` entrypoints.
    """

    count = field(factory=count_factory)
    registry = field(factory=partial(registry_load, "pytest_unique"))

    def __call__(self, _name, *args, **kwargs):
        """Invoke the unique plugin."""
        plugin = self.get_plugin(_name)
        return plugin(*args, **kwargs)

    def get_plugin(self, _name, *args, **kwargs):
        """Find plugin in the registry."""
        try:
            plugins = self.registry["pytest_unique"]
        except KeyError:
            raise KeyError("No plugins found") from None

        try:
            plugin = plugins[_name]
        except KeyError:
            raise KeyError(f"No matching plugin found for {_name!r}") from None

        return partial(plugin, self, *args, **kwargs)


def unique_bytes(unique):
    """Return bytes unique to this factory instance."""
    return unique("text", suffix="\xfe").encode("latin-1")


def unique_digits(unique, *args, **kwargs):
    """Return digits unique to this factory instance.

    Takes the same arguments as `integer`.
    """
    return str(unique("integer", *args, **kwargs))


def unique_email(unique, *args, **kwargs):
    """Return an email unique to this factory instance.

    Takes the same arguments as `text`.

    :param domain: Optional domain, defaults to `example.com`.
    """
    domain = kwargs.pop("domain", "example.com")
    username = unique("text", *args, **kwargs)
    return f"{username}@{domain}"


def unique_float(unique):
    """Return a float unique to this factory instance.

    The floating point number by making an integer for the whole
    part and another integer for the decimal part.
    """
    whole = unique("integer")
    decimal = unique("integer")
    return float(f"{whole}.{decimal}")


def unique_integer(unique, base=None, mod=None):
    """Return an integer unique to this factory instance.

    :param base: Optional base to add to the integer.
    :param mod: Optional modulo to apply on the integer.
    """
    integer = next(unique.count)
    if mod is not None:
        integer %= mod
    if base is not None:
        integer += base

    return integer


def unique_password(unique, lowercase=4, uppercase=2, digits=1, punctuation=1):
    """Return a password unique to this factory instance.

    :param lowercase: Number of lowercase letters, defaults to 4.
    :param uppercase: Number of uppercase letters, defaults to 2.
    :param digits: Number of digits, defaults to 1.
    :param punctuation: Number of punctuation characters, defaults to 1.
    """
    chars = (
        sample(string.ascii_lowercase, lowercase)
        + sample(string.ascii_uppercase, uppercase)
        + sample(string.digits, digits)
        + sample(string.punctuation, punctuation)
    )

    return "".join(sample(chars, lowercase + uppercase + digits + punctuation))


def unique_text(unique, prefix=None, suffix=None, separator="-", limit=None):
    """Return text unique to this factory instance.

    :param prefix: Used as a prefix for the unique string, defaults
        to a generated string from the stack frame.
    :param suffix: Optional suffix for the unique string.
    :param separator: Separator between parts of the string,
        defaults to '-'.
    :param limit: Optional limit for the unique string.
    """
    if prefix is None:
        frame = sys._getframe(2)
        source_filename = frame.f_code.co_filename
        # Dots and dashes cause trouble with some consumers of these
        # names.
        source = (
            PurePath(source_filename)
            .name.replace("-", separator)
            .replace("_", separator)
            .replace(".", separator)
        )
        prefix = separator.join([
            "unique",
            "from",
            source,
            f"line{frame.f_lineno}",
        ])

    text = separator.join([prefix, str(unique("integer"))])
    if suffix is not None:
        text = separator.join([text, suffix])

    if limit is not None:
        # Truncate from the end.
        text = text[-limit:]

    return text


def unique_uuid(unique, integer=None):
    """Return a UUID unique to this factory instance.

    This method provides a more predictable alternative to `uuid4()`.
    """
    if integer is None:
        integer = unique("integer")

    return UUID(int=integer)
