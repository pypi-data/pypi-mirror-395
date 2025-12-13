# src/rich_json_tree/tree.py
from dataclasses import dataclass
from typing import Any, Set, Optional
from rich.tree import Tree
from rich.console import Console
from rich.text import Text


@dataclass
class JsonTreeConfig:
    max_items: int = 5        # max list items to show per list
    max_depth: Optional[int] = None  # None = unlimited
    max_string: int = 40      # max chars to show for leaf previews
    sort_keys: bool = True    # sort dict keys alphabetically
    show_types: bool = True   # show type names at leaves
    show_lengths: bool = True # show “N keys/items” on containers


TYPE_ICONS = {
    "dict": "📁",
    "list": "📚",
    "str": "🔤",
    "int": "🔢",
    "float": "🔢",
    "bool": "✅",
    "NoneType": "∅",
}


def _format_label(name: str, value: Any, cfg: JsonTreeConfig) -> Text:
    t = type(value).__name__
    icon = TYPE_ICONS.get(t, "•")

    label = Text()
    label.append(f"{icon} ", style="dim")
    label.append(str(name), style="bold cyan")

    if isinstance(value, dict):
        if cfg.show_lengths:
            label.append("  ", style="")
            label.append(f"({t}, {len(value)} keys)", style="dim")
    elif isinstance(value, list):
        if cfg.show_lengths:
            label.append("  ", style="")
            label.append(f"({t}, {len(value)} items)", style="dim")
    else:
        preview = repr(value)
        if len(preview) > cfg.max_string:
            preview = preview[: cfg.max_string - 3] + "..."
        label.append(" = ", style="dim")
        label.append(preview, style="magenta")
        if cfg.show_types:
            label.append(f"  ({t})", style="dim")

    return label


def _make_tree(
    name: str,
    data: Any,
    cfg: JsonTreeConfig,
    *,
    depth: int = 0,
    _seen: Optional[Set[int]] = None,
) -> Tree:
    if _seen is None:
        _seen = set()

    node_id = id(data)
    if node_id in _seen:
        return Tree(f"[bold red]{name}[/] [dim](cycle detected)[/]")
    _seen.add(node_id)

    if cfg.max_depth is not None and depth > cfg.max_depth:
        return Tree(f"[bold]{name}[/] [dim](max depth reached)[/]")

    tree = Tree(_format_label(name, data, cfg), guide_style="dim")

    if isinstance(data, dict):
        items = data.items()
        if cfg.sort_keys:
            items = sorted(items, key=lambda kv: str(kv[0]))
        for key, value in items:
            subtree = _make_tree(
                str(key), value, cfg, depth=depth + 1, _seen=_seen
            )
            tree.add(subtree)

    elif isinstance(data, list):
        length = len(data)
        shown = min(length, cfg.max_items)
        for i in range(shown):
            value = data[i]
            subtree = _make_tree(
                f"[{i}]", value, cfg, depth=depth + 1, _seen=_seen
            )
            tree.add(subtree)
        if shown < length:
            tree.add(f"[dim]… ({length - shown} more items)[/]")

    return tree


def print_json_tree(data: Any, name: str = "root", **config_overrides) -> None:
    """
    Pretty-print a JSON-like object as a Rich tree.

    Example:
        from rich_json_tree import print_json_tree
        print_json_tree(data, name="documents", max_items=3)
    """
    cfg = JsonTreeConfig(**config_overrides)
    console = Console()
    tree = _make_tree(name, data, cfg)
    console.print(tree)
