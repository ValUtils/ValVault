from dataclasses import dataclass

from dataclasses_json import DataClassJsonMixin


@dataclass
class Settings(DataClassJsonMixin):
    insecure: bool = False
