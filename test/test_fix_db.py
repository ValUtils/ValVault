import pytest

from ValVault.database import EncryptedDB

from .mockup import EntryMockup


def test_delete():
    entry = EntryMockup(username=None, password=None)
    EncryptedDB.fix_entry(entry)
    assert entry._deleted, "Entry not deleted"


def test_fix_username():
    entry = EntryMockup(username=None)
    EncryptedDB.fix_entry(entry)
    assert entry.username == f"NoUsername{entry.ctime}", "Username not fixed"


def test_fix_password():
    entry = EntryMockup(password=None)
    EncryptedDB.fix_entry(entry)
    assert isinstance(entry.password, str), "Password not fixed"


def test_fix_alias():
    entry = EntryMockup(alias=None)
    EncryptedDB.fix_entry(entry)
    alias = entry.custom_properties["alias"]
    assert alias == entry.username, "Alias not fixed"


def test_fix_missing_alias():
    entry = EntryMockup(alias=None)
    entry._custom_properties.pop("alias")
    EncryptedDB.fix_entry(entry)
    alias = entry.custom_properties["alias"]
    assert alias == entry.username, "Alias not fixed"


def test_fix_alt():
    entry = EntryMockup()
    entry._custom_properties["alt"] = None
    EncryptedDB.fix_entry(entry)
    alt = entry.custom_properties["alt"]
    assert alt == "0", "Alt not fixed"


def test_fix_missing_alt():
    entry = EntryMockup()
    entry._custom_properties.pop("alt")
    EncryptedDB.fix_entry(entry)
    alt = entry.custom_properties["alt"]
    assert alt == "0", "Alt not fixed"
