from loadstructure.config_node import ConfigNode
from loadstructure.utils.helper import _merge_dicts
import json
import yaml
import xmltodict
import os
import configparser
import tomllib
import toml   
import time 
import threading


class ConfigManager:
    """Load JSON/YAML/XML/TOML configs and provide attribute-style access."""

    def __init__(self, path: str, filetype: str = None):
        self.path = path
        self.filetype:str = filetype
        self._config: ConfigNode | None = None
    
    # ---------- loaders ----------
    def _load_json(self):
        with open(self.path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _load_yaml(self):
        if yaml is None:
            raise ImportError("PyYAML is not installed. Run `uv add PyYAML`.")
        with open(self.path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def _load_xml(self):
        if xmltodict is None:
            raise ImportError("xmltodict is not installed. Run `uv add xmltodict`.")
        with open(self.path, 'r', encoding='utf-8') as f:
            xml = xmltodict.parse(f.read())
        # Flatten root element if only one top-level key
        if len(xml) == 1:
            return list(xml.values())[0]
        return xml
    def _load_toml(self):
        with open(self.path, "rb") as f:
            if hasattr(tomllib, "load"):
                data = tomllib.load(f)  # Python 3.11
            else:
                data = toml.load(f)  # toml package
        return data
    def _load_def(self):
        parser = configparser.ConfigParser()
        parser.read(self.path, encoding="utf-8")
        data = {}
        for section in parser.sections():
            data[section] = {}
            for key, value in parser.items(section):
                # Try to auto-cast int, float, bool if possible
                data[section][key] = self._cast_value(value)
        return data

    def _cast_value(self, value: str):
        # Try bool
        if value.lower() in ("true", "yes", "1"):
            return True
        if value.lower() in ("false", "no", "0"):
            return False
        # Try int
        try:
            return int(value)
        except ValueError:
            pass
        # Try float
        try:
            return float(value)
        except ValueError:
            pass
        # Return as string
        return value

    # ---------- load main ----------
    def load(self):
        if not os.path.exists(self.path):
            with open(self.path, 'w') as f:
                pass
        ext = os.path.splitext(self.path)[1].lower()
        # Read raw text to detect empty file
        with open(self.path, "r", encoding="utf-8") as f:
            content = f.read().strip()

        # If file is empty → treat as empty dict
        if content == "":
            raw = {}
        else:
            # If filetype argument is forced, use that
            if self.filetype is not None:
                raw = self.select_filetype(self.filetype)
            else:
                raw = self.select_filetype(ext)

        # Wrap in ConfigNode
        self._config = ConfigNode(raw)
        return self._config
    
    def select_filetype(self, ext: str):
        if ext and not ext.startswith("."):
            ext = "." + ext
        match ext.lower():
            case ".json": return self._load_json()
            case ".yaml" | ".yml": return self._load_yaml()
            case ".xml": return self._load_xml()
            case ".def": return self._load_def()
            case ".toml": return self._load_toml()
            case _: raise ValueError(f"Unsupported file type: {ext}")
    def reload(self):
        self.load()
        return self._config
    
    # ---------- delegate attribute access ----------
    def __getattr__(self, name: str):
        if self._config is None:
            raise AttributeError("Config not loaded. Call load() first.")
        return getattr(self._config, name)
    
    def __setattr__(self, name, value):
        # Allow normal attributes for internal variables
        if name in ("path", "filetype", "_config"):
            super().__setattr__(name, value)
        elif hasattr(self, "_config") and self._config is not None:
            setattr(self._config, name, value)
        else:
            super().__setattr__(name, value)
    # -------- merging files -------------------------
    @classmethod
    def merge(cls, paths: list[str]) -> "ConfigManager":
        """
        Load and merge multiple config files (JSON/YAML/XML).
        Later files override earlier ones.
        Returns a ConfigManager instance with merged ConfigNode.
        """
        merged_data = {}
        for path in paths:
            cm = cls(path)
            cfg = cm.load()
            merged_data = _merge_dicts(merged_data, cfg.to_dict())

        # Create a ConfigManager without a path (or use first file as reference)
        merged_manager = cls(paths[0])
        merged_manager._config = ConfigNode(merged_data)
        return merged_manager
    
    def watch(self, interval=1, on_reload=None):
        """
        Auto reload the config file whenever it changes.
        interval = check frequency (seconds)
        on_reload = callback (function called after reload)
        """

        def watcher():
            last_mtime = os.path.getmtime(self.path)
            while True:
                time.sleep(interval)
                try:
                    current_mtime = os.path.getmtime(self.path)
                    if current_mtime != last_mtime:
                        last_mtime = current_mtime
                        self.reload()
                        if on_reload:
                            on_reload(self)
                except FileNotFoundError:
                    pass

        thread = threading.Thread(target=watcher, daemon=True)
        thread.start()
    # ---------- save back ----------
    def save(self, path: str | None = None, filetype: str | None = None):
        if self._config is None:
            raise RuntimeError("Nothing loaded to save.")
        path = path or self.path
        data = self._config.to_dict()
        # Priority: given filetype > manager.filetype > path extension
        if filetype:
            ext = filetype.lower()
        elif self.filetype:
            ext = self.filetype.lower()
        else:
            ext = os.path.splitext(path)[1].lower()

        # Ensure ext starts with "."
        if ext and not ext.startswith("."):
            ext = "." + ext
            

        # If path has no extension, append ext
        if os.path.splitext(path)[1] == "":
            path = path + ext

        
        if ext == ".json":
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        elif ext in (".yaml", ".yml"):
            if yaml is None:
                raise ImportError("PyYAML not installed. Run `uv add PyYAML`.")
            with open(path, "w", encoding="utf-8") as f:
                yaml.dump(data, f)
        elif ext == ".xml":
            if xmltodict is None:
                raise ImportError("xmltodict not installed. Run `uv add xmltodict`.")
            data = {"config": data}  # wrap all keys in root
            with open(path, "w", encoding="utf-8") as f:
                xmltodict.unparse(data, output=f, pretty=True)
        elif ext == ".def":
            self._save_def(path)
        elif ext == ".toml":
            self._save_toml(path)
        else:
            raise ValueError(f"Unsupported save format: {ext}")
        self.reload()
    def _save_def(self, path: str):

        if self._config is None:
            raise RuntimeError("Nothing to save.")

        parser = configparser.ConfigParser()
        data = self._config.to_dict()

        for section, values in data.items():
            parser[section] = {}
            for key, value in values.items():
                # Convert booleans to 'true'/'false' strings
                if isinstance(value, bool):
                    parser[section][key] = "true" if value else "false"
                else:
                    parser[section][key] = str(value)

        with open(path, "w", encoding="utf-8") as f:
            parser.write(f)

    def _save_toml(self, path: str):
        if self._config is None:
            raise RuntimeError("Nothing to save.")

        data = self._config.to_dict()

        with open(path, "w", encoding="utf-8") as f:
            toml.dump(data, f)

    def __repr__(self):
        return self._config.__repr__()
    
    def to_dict(self):
        return self._config.to_dict()
    
    def get(self, dotted_key, default=None):
        """Access using dotted path: node.get('a.b.c')"""
        return self._config.get(dotted_key, default)
    
    def items(self):
        return self._config.items()
    
    def keys(self):
        return self._config.keys()
    
    def values(self):
        return self._config.values()
    
    def __iter__(self):
        return self._config.__iter__()
    
    def __len__(self):
        return self._config.__len__()

