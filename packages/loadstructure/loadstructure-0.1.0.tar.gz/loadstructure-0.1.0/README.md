# loadstructure

A versatile Python library for loading and managing configuration files (JSON, YAML, XML, TOML, and INI/DEF-style) with **attribute-style access**, merging capabilities.

## ✨ Features

* **Multiple Formats:** Load configurations from **JSON, YAML, XML, TOML, and INI/DEF** files.
* **Attribute Access:** Access settings using dot notation (e.g., `config.server.port`).
* **Merging:** Easily merge multiple configuration files, with later files overriding earlier settings.
* **Saving:** Write your data in form of dictionary back to any supported file format.

---

## Installation

Using **uv**:

```bash
uv add loadstructure
```

Using **pip**
```bash
pip install loadstructure
```
## 📦 Dependencies

The following dependencies are required and will be installed automatically if you use standard Python packaging practices:

* **YAML:** `pyyaml >=6.0.3`
* **TOML:** `toml >=0.10.2`
* **XML:** `xmltodict >=1.0.2`
## 📖 Usage

### Basic Loading

Instantiate `ConfigManager` with the path to your config file and call `.load()`.

**`config.json`:**
```json
{
  "app": {
    "name": "App",
    "version": "1.0.0",
    "features": {
      "login": true,
      "analytics": false,
      "dark_mode": true,
      "notifications": true
    },
    "ui": {
      "theme": "light",
      "language": "en"
    }
  },
  "modules": {
    "editor": {
      "enabled": true,
      "autosave_interval": 5
    },
    "export": {
      "formats": ["pdf", "html", "md"],
      "compress_output": false
    }
  }
}

```
### Load a configuration file
```python
from loadstructure import ConfigManager

cfg = ConfigManager("app_config.json")
cfg.load()

# Attribute-style access
print(cfg.app.name)                       # App
print(cfg.app.ui.theme)                   # light
print(cfg.modules.editor.autosave_interval)  # 5

# Dictionary-style access
print(cfg["app"]["features"]["dark_mode"])  # True

```
### Nested key access using dotted paths
```python
theme = cfg.get("app.ui.theme")
print(theme)  # light

```
### Modifying and saving values
```python
cfg.app.features.analytics = True
cfg.modules.export.compress_output = True
fg.app.tech = {
    'frontend':'(html,css,js)',
    'backend':'electron'
}

# Save changes back to JSON
cfg.save()
```
## Write 
### Merging multiple configuration files
```python
# app_config_override.json can override some settings
merged_cfg = ConfigManager.merge(["app_config.json", "app_config_override.json"])
print(merged_cfg.app.features.analytics)
```
## License
This project is licensed under the [MIT License](https://github.com/TechRuler/loadstructure/blob/main/LICENSE) for full details.