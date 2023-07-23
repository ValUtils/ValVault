import pytest

from ValVault.entry import Entry, EntryException

from .mockup import EntryMockup


def add_path():
    import os.path
    import sys
    path = os.path.realpath(os.path.abspath(__file__))
    sys.path.insert(0, os.path.dirname(os.path.dirname(path)))


add_path()


def test_valid():
    entry = EntryMockup()
    Entry(entry)


def test_missing_username():
    entry = EntryMockup(username=None)
    with pytest.raises(EntryException):
        Entry(entry)


def test_missing_password():
    entry = EntryMockup(password=None)
    with pytest.raises(EntryException):
        Entry(entry)


def test_missing_alias():
    entry = EntryMockup(alias=None)
    entry._custom_properties.pop("alias")
    with pytest.raises(EntryException):
        Entry(entry)


def test_alias_is_none():
    entry = EntryMockup(alias=None)
    with pytest.raises(EntryException):
        Entry(entry)


def test_missing_alt():
    entry = EntryMockup()
    entry._custom_properties.pop("alt")
    with pytest.raises(EntryException):
        Entry(entry)


def test_alt_is_none():
    entry = EntryMockup()
    entry._custom_properties["alt"] = None
    with pytest.raises(EntryException):
        Entry(entry)
