from typing import Any, Dict, Union
from collections.abc import MutableMapping

class Dictionary:
    """
    A flexible dictionary class that allows both dictionary-style and dot notation access.
    Handles nested dictionaries by converting them to Dictionary objects recursively.
    
    Example:
        >>> data = Dictionary({'a': {'b': 1}, 'c': 2})
        >>> data.a.b  # dot notation
        1
        >>> data['a']['b']  # dict notation
        1
    """

    def __init__(self, data: Dict[str, Any]):
        for key, value in data.items():
            # Convert nested dictionaries recursively
            if isinstance(value, (dict, MutableMapping)):
                setattr(self, key, Dictionary(value))
            # Convert lists and check for dictionaries within them
            elif isinstance(value, list):
                setattr(self, key, [
                    Dictionary(item) if isinstance(item, (dict, MutableMapping)) else item
                    for item in value
                ])
            else:
                setattr(self, key, value)

    def __getitem__(self, key: str) -> Any:
        """Enable dictionary-style access: obj['key']"""
        return getattr(self, key)

    def __setitem__(self, key: str, value: Any) -> None:
        """Enable dictionary-style assignment: obj['key'] = value"""
        setattr(self, key, value)

    def __delitem__(self, key: str) -> None:
        """Enable dictionary-style deletion: del obj['key']"""
        delattr(self, key)

    def __contains__(self, key: str) -> bool:
        """Enable 'in' operator: 'key' in obj"""
        return hasattr(self, key)

    def __repr__(self) -> str:
        """Return a string representation of the object"""
        items = [f"{k}={repr(v)}" for k, v in self.__dict__.items()]
        return f"Dictionary({', '.join(items)})"

    def to_dict(self) -> Dict[str, Any]:
        """Convert the Dictionary back to a regular dictionary"""
        result = {}
        for key, value in self.__dict__.items():
            if isinstance(value, Dictionary):
                result[key] = value.to_dict()
            elif isinstance(value, list):
                result[key] = [
                    item.to_dict() if isinstance(item, Dictionary) else item
                    for item in value
                ]
            else:
                result[key] = value
        return result

    def get(self, key: str, default: Any = None) -> Any:
        """Dictionary-style get method with default value"""
        return getattr(self, key, default)

    def update(self, other: Union[Dict[str, Any], 'Dictionary']) -> None:
        """Update the Dictionary with another dictionary or Dictionary"""
        if isinstance(other, Dictionary):
            other = other.to_dict()
        for key, value in other.items():
            if isinstance(value, (dict, MutableMapping)):
                if key in self and isinstance(self[key], Dictionary):
                    self[key].update(value)
                else:
                    self[key] = Dictionary(value)
            else:
                self[key] = value

    def keys(self):
        """Return a view of dictionary keys"""
        return self.__dict__.keys()

    def values(self):
        """Return a view of dictionary values"""
        return self.__dict__.values()

    def items(self):
        """Return a view of dictionary items as (key, value) pairs"""
        return self.__dict__.items()