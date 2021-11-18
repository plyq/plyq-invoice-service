"""JSON config reader."""
import json
from typing import Any, Dict


class Config(dict):
    """JSON config reader."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(Config, self).__init__(*args, **kwargs)
        self.__dict__ = self

    @classmethod
    def from_file(cls, path: str) -> "Config":
        """Read config from JSON file.

        :param path: path to file
        :returns: loaded config"""
        data: Dict[str, Any] = {}
        with open(path, "r") as json_file:
            data = json.load(json_file)
        return cls.from_nested_dicts(data)

    @classmethod
    def from_nested_dicts(cls, data: Dict[str, Any]) -> "Config":
        """Construct nested Config from nested dictionaries.

        :param data: nested dictionary
        :returns: config
        """
        if not isinstance(data, dict):
            return data
        else:
            return cls({key: cls.from_nested_dicts(data[key]) for key in data})
