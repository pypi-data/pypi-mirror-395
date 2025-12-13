# `rich-json-tree`

> 🪵 Pretty-print JSON and nested Python structures as a colorful Rich-powered tree — like the `tree` command, but for data.

`rich-json-tree` helps you quickly explore deeply nested JSON, config files, API responses, schemas, or any Python dictionary/list structure — with clear formatting, icons, type hints, and size information.

If you've ever printed a messy 300-line `dict` and squinted at indentation trying to understand it — this tool is for you.

---

## ✨ Features

* 🎨 Beautiful text-tree visualization using **Rich**
* 🔤 Detects **types** automatically (`dict`, `list`, `str`, `int`, `None`, etc.)
* 📏 Shows collection sizes (keys/items)
* 💡 Configurable:

  * Max depth
  * Max list items displayed
  * Value preview length
  * Optional key sorting
* 🛑 Cycle detection (avoids infinite loops)
* 🧪 Works with standard Python objects — no JSON required

---

## 📦 Installation

```bash
pip install rich-json-tree
```

---

## 🚀 Usage Example

```python
from rich_json_tree import print_json_tree

data = {
    "user": {
        "name": "Alice",
        "age": 30,
        "skills": ["Python", "SQL"],
        "active": True
    },
    "meta": {"source": "api", "timestamp": "2025-01-08"}
}

print_json_tree(data, name="payload")
```

### Output (example)

```
📁 payload  (dict, 2 keys)
│
├── 📁 user  (dict, 4 keys)
│   ├── 🔤 name = 'Alice'  (str)
│   ├── 🔢 age = 30  (int)
│   ├── 📚 skills  (list, 2 items)
│   │   ├── [0] = 'Python'  (str)
│   │   └── [1] = 'SQL'  (str)
│   └── ✅ active = True  (bool)
│
└── 📁 meta  (dict, 2 keys)
    ├── 🔤 source = 'api'  (str)
    └── 🔤 timestamp = '2025-01-08'  (str)
```

---

## ⚙️ Configuration Options

Customize behavior by passing keyword arguments:

```python
print_json_tree(
    data,
    name="response",
    max_items=3,      # show only first 3 list items
    max_depth=4,     # stop at depth level 4
    max_string=80,   # show up to 80 characters for values
    sort_keys=True,  # sort dict keys alphabetically
)
```

---

## 🧩 API Reference

### `print_json_tree(data, name="root", **options)`

| Option         | Type          | Default | Description                         |
| -------------- | ------------- | ------- | ----------------------------------- |
| `max_items`    | `int`         | `5`     | Max list elements to print          |
| `max_depth`    | `int or None` | `None`  | Limits recursion depth              |
| `max_string`   | `int`         | `40`    | Max characters for string previews  |
| `sort_keys`    | `bool`        | `True`  | Sort dictionary keys                |
| `show_types`   | `bool`        | `True`  | Display type info on leaves         |
| `show_lengths` | `bool`        | `True`  | Display list size / dict keys count |

---

## 📁 CLI Support (optional future feature)

A CLI command may be added in future releases:

```bash
rich-json-tree data.json
```

---

## 🔧 Environment Compatibility

* Python **3.8+**
* OS: Windows, macOS, Linux
* Works in:

  * VSCode terminal
  * PyCharm
  * Jupyter
  * Standard terminals

---

## 🪪 License

MIT — free to use, modify, and contribute.

---

## 🤝 Contributing

Pull requests, ideas, and feature requests are welcome!

```bash
git clone https://github.com/<yourname>/rich-json-tree
cd rich-json-tree
```

---

## ⭐ If you find this helpful...

Please consider starring the repository — it helps others discover the tool 🌟
