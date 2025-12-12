from typing import Any
class ConfigNode:
    """Wraps a dictionary to allow attribute-style and dict-style access."""

    def __init__(self, d):
        object.__setattr__(self, "_data", {})
        for key, value in d.items():
            self._data[key] = self._wrap(value)

    def _wrap(self, value):
        if isinstance(value, dict):
            return ConfigNode(value)
        elif isinstance(value, list):
            return [self._wrap(v) for v in value]
        return value
    
    def set(self, dotted_key: str, value):
        """Set nested keys using a dotted path, auto-creating intermediate nodes."""
        parts = dotted_key.split(".")
        node = self
        for p in parts[:-1]:
            if p not in node._data or not isinstance(node._data[p], ConfigNode):
                node._data[p] = ConfigNode({})
            node = node._data[p]
        # Set final value
        node._data[parts[-1]] = self._wrap(value)

    # ---------- attribute access ----------
    def __getattr__(self, key)-> "ConfigNode | Any":
        if key in self._data:
            return self._data[key]
        raise AttributeError(f"No attribute named '{key}'")

    def __setattr__(self, key, value):
        self._data[key] = self._wrap(value)

    # ---------- dict access ----------
    def __getitem__(self, key):
        return self._data[key]

    def __setitem__(self, key, value):
        self._data[key] = self._wrap(value)
    
    # ---------- useful methods ----------
    def to_dict(self):
        def convert(v):
            if isinstance(v, ConfigNode):
                return v.to_dict()
            elif isinstance(v, list):
                return [convert(x) for x in v]
            return v
        
        return {k: convert(v) for k, v in self._data.items()}

    def get(self, dotted_key, default=None):
        """Access using dotted path: node.get('a.b.c')"""
        parts = dotted_key.split(".")
        node = self
        for p in parts:
            if isinstance(node, ConfigNode) and p in node._data:
                node = node._data[p]
            else:
                return default
        return node
    
    def items(self):
        return self._data.items()
    
    def keys(self):
        return self._data.keys()
    
    def values(self):
        return self._data.values()
    
    def __iter__(self):
        return iter(self._data)
    
    def __len__(self):
        return len(self._data)
    
    def __dir__(self):
        # include normal attributes + dynamic keys
        return list(super().__dir__()) + list(self._data.keys())
    def __repr__(self):
        return f"ConfigNode({self._data})"
