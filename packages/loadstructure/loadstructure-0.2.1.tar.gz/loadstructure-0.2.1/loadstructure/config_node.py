class SchemaError(Exception):
    """Raised when configuration does not match the schema rules."""
    pass


class ConfigNode:
    def __init__(self, d=None, schema=None):
        object.__setattr__(self, "_data", {})
        object.__setattr__(self, "_schema", schema)

        d = d or {}

        for key, value in d.items():
            rule = schema.get(key) if schema else None
            self._data[key] = self._wrap(value, rule)

    # ---------------------------------------------------------
    # WRAPPING + VALIDATION
    # ---------------------------------------------------------
    def _validate(self, rule, value):
        if rule is None:
            return

        # rule == dict TYPE (not schema)
        if rule == dict:
            if not isinstance(value, (dict, ConfigNode)):
                raise SchemaError(f"value must be dict, got {type(value).__name__}")
            return

        # rule is LIST TYPE
        if rule == list:
            if not isinstance(value, list):
                raise SchemaError(f"value must be list, got {type(value).__name__}")
            return

        # rule is a nested SCHEMA dict
        if isinstance(rule, dict):
            if not isinstance(value, (dict, ConfigNode)):
                raise SchemaError(f"value must be object/dict for schema field")
            return

        # primitive type
        if isinstance(rule, type):
            if not isinstance(value, rule):
                raise SchemaError(
                    f"value must be {rule.__name__}, got {type(value).__name__}"
                )

    def _wrap(self, value, rule=None):
        self._validate(rule, value)

        # case: nested schema → wrap dict
        if isinstance(rule, dict):
            return ConfigNode(value if isinstance(value, dict) else {}, rule)

        # dict type → wrap as free dict (no subschema)
        if rule == dict:
            return ConfigNode(value, None) if isinstance(value, dict) else value

        # default wrapping
        if isinstance(value, dict):
            return ConfigNode(value, None)
        if isinstance(value, list):
            return [self._wrap(v) for v in value]

        return value

    # ---------------------------------------------------------
    # ATTRIBUTE GET (AUTO-CREATE)
    # ---------------------------------------------------------
    def __getattr__(self, key):

        # free mode → always auto-create
        if self._schema is None:
            if key not in self._data:
                self._data[key] = ConfigNode({}, None)
            return self._data[key]

        # schema mode → key must exist
        if key not in self._schema:
            raise SchemaError(f"'{key}' is not allowed by the schema.")

        # already exists
        if key in self._data:
            return self._data[key]

        # rule decides auto creation
        rule = self._schema[key]

        # nested schema
        if isinstance(rule, dict):
            node = ConfigNode({}, rule)
            self._data[key] = node
            return node

        # dict allowed
        if rule == dict:
            node = ConfigNode({}, None)
            self._data[key] = node
            return node

        # primitive → cannot auto-create
        raise SchemaError(
            f"Cannot auto-create '{key}' because schema expects primitive: {rule.__name__}"
        )

    # ---------------------------------------------------------
    # ATTRIBUTE SET
    # ---------------------------------------------------------
    def __setattr__(self, key, value):

        if key in ("_data", "_schema"):
            return object.__setattr__(self, key, value)

        # free mode
        if self._schema is None:
            self._data[key] = self._wrap(value, None)
            return

        # schema mode
        if key not in self._schema:
            raise SchemaError(f"'{key}' is not allowed by the schema.")

        rule = self._schema[key]
        self._data[key] = self._wrap(value, rule)

    # ---------------------------------------------------------
    # DICT ACCESS
    # ---------------------------------------------------------
    def __getitem__(self, key):
        return self.__getattr__(key)

    def __setitem__(self, key, value):
        rule = self._schema.get(key) if self._schema else None
        self._data[key] = self._wrap(value, rule)

    # ---------------------------------------------------------
    # GET USING DOTTED PATH
    # ---------------------------------------------------------
    def get(self, dotted_key, default=None):
        node = self
        for p in dotted_key.split("."):
            if isinstance(node, ConfigNode) and p in node._data:
                node = node._data[p]
            else:
                return default
        return node

    # ---------------------------------------------------------
    # SET USING DOTTED PATH
    # ---------------------------------------------------------
    def set(self, dotted_key: str, value):
        parts = dotted_key.split(".")
        node = self

        for p in parts[:-1]:
            # determine subschema
            if node._schema is None:
                subschema = None
            else:
                if p not in node._schema:
                    raise SchemaError(f"'{p}' is not allowed by the schema.")
                rule = node._schema[p]
                if isinstance(rule, dict):
                    subschema = rule
                elif rule == dict:
                    subschema = None
                else:
                    raise SchemaError(
                        f"Cannot auto-create '{p}' because schema expects primitive {rule.__name__}"
                    )

            # create if not existing
            if p not in node._data or not isinstance(node._data[p], ConfigNode):
                node._data[p] = ConfigNode({}, subschema)

            node = node._data[p]

        last = parts[-1]

        # schema mode
        if node._schema is not None:
            if last not in node._schema:
                raise SchemaError(f"'{last}' is not allowed by the schema.")
            rule = node._schema[last]
            node._data[last] = self._wrap(value, rule)
            return

        # free mode
        node._data[last] = self._wrap(value, None)

    # ---------------------------------------------------------
    # UPDATE / REPLACE
    # ---------------------------------------------------------
    def update(self, d: dict):
        """Updates only allowed keys. Fully schema-aware."""
        for key, value in d.items():
            # Schema mode → reject undefined keys
            if self._schema is not None:
                if key not in self._schema:
                    raise SchemaError(f"'{key}' is not allowed by schema.")

                rule = self._schema[key]
                self._data[key] = self._wrap(value, rule)
                continue

            # free mode
            self._data[key] = self._wrap(value, None)


    def replace(self, new_dict: dict):
        """Replaces all data but enforces schema strictly."""
        # Schema mode → validate EVERYTHING first
        if self._schema is not None:
            # reject extra keys
            for key in new_dict:
                if key not in self._schema:
                    raise SchemaError(f"'{key}' is not allowed by schema.")

            # validate values
            for key, value in new_dict.items():
                rule = self._schema[key]
                self._validate(rule, value)

            # all valid → replace now
            self._data.clear()
            for key, value in new_dict.items():
                rule = self._schema[key]
                self._data[key] = self._wrap(value, rule)
            return

        # free mode
        self._data = {k: self._wrap(v, None) for k, v in new_dict.items()}


    # ---------------------------------------------------------
    # to_dict + iteration helpers
    # ---------------------------------------------------------
    def to_dict(self):
        def convert(v):
            if isinstance(v, ConfigNode):
                return v.to_dict()
            if isinstance(v, list):
                return [convert(x) for x in v]
            return v
        return {k: convert(v) for k, v in self._data.items()}

    def items(self): return self._data.items()
    def keys(self): return self._data.keys()
    def values(self): return self._data.values()

    def __iter__(self): return iter(self._data)
    def __len__(self): return len(self._data)
    def __repr__(self): return f"ConfigNode({self._data})"
    def __dir__(self): return list(super().__dir__()) + list(self._data.keys())
