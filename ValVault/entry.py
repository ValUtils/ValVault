from pykeepass.entry import Entry as KpEntry


class Entry():
    entry: KpEntry
    username: str = ""
    password: str = ""
    alias: str = ""
    alt: bool = False

    def set_custom_property(self, key, value):
        self.entry.set_custom_property(key, value)

    def __init__(self, entry: KpEntry):
        assert isinstance(entry.username, str)
        assert isinstance(entry.password, str)
        assert "alias" in entry.custom_properties
        assert isinstance(entry.custom_properties["alias"], str)
        assert "alt" in entry.custom_properties
        assert isinstance(entry.custom_properties["alt"], str)
        self.username = entry.username
        self.password = entry.password
        self.alias = entry.custom_properties["alias"]
        self.alt = bool(int(entry.custom_properties["alt"]))
        self.entry = entry

    def __repr__(self) -> str:
        return f"Entry(username={self.username}, alias={self.alias}, alt={self.alt})"
