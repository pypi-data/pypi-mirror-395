#!/usr/bin/env python3
"""
LLM Prompt + Smart File Injector
Now supports: .py, Makefile, pyproject.toml, .md, .yaml/.yml
Auto-replaces {__FILE__} and wraps content in correct code block!
"""

import os
import time
import typer
import re
import yaml
import pyperclip
from pathlib import Path
from typing import List, Optional

from rich.console import Console

from prompt_toolkit.application import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import HSplit, VSplit, Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.layout import Layout as PTLayout
from prompt_toolkit.keys import Keys
from prompt_toolkit.styles import Style

# === Constants fallback ===
try:
    from .constants import (
        DEFAULT_PROMPTS_YAML_FILE,
        DEFAULT_SEARCH_BAR_STYLE,
        DEFAULT_STATUS_BAR_STYLE,
        DEFAULT_SLEEP_SECONDS,
        IGNORE_DIRS,
    )
except ImportError:
    DEFAULT_PROMPTS_YAML_FILE = "prompts.yaml"
    DEFAULT_SEARCH_BAR_STYLE = "bold white on #003366"
    DEFAULT_STATUS_BAR_STYLE = "dim white on black"
    DEFAULT_SLEEP_SECONDS = 0.7
    IGNORE_DIRS = {"__pycache__", ".git", ".venv", "venv", "env", ".env", "build", "dist", "node_modules"}

console = Console()
app = typer.Typer()

# === CONFIG ===
def get_prompts_yaml_path(prompts_file: Optional[str] = None) -> str:
    """Get the prompts YAML file path with fallback strategy."""
    if prompts_file:
        # User specified a prompts file via --prompts parameter
        if not os.path.isfile(prompts_file):
            console.print(f"[red]Error:[/red] Specified prompts file '{prompts_file}' not found or empty.")
            raise typer.Exit(1)
        if os.path.getsize(prompts_file) == 0:
            console.print(f"[red]Error:[/red] Specified prompts file '{prompts_file}' is empty.")
            raise typer.Exit(1)
        return prompts_file
    
    # Use default fallback strategy
    prompts_yaml_path = os.path.expanduser("~/.config/jps-llm-prompt-app/prompts.yaml")
    if not os.path.isfile(prompts_yaml_path):
        console.print(f"[yellow]Warning:[/yellow] Custom prompts not found. Using fallback.")
        prompts_yaml_path = DEFAULT_PROMPTS_YAML_FILE
    return prompts_yaml_path

# === DATA MODEL ===
class Item:
    def __init__(self, name: str, content: str, path: str = ""):
        self.name = name
        self.content = content.strip()
        self.path = path

    def __str__(self):
        return self.name

# === FILE LOADER WITH SMART FENCING ===
def get_fence_for_path(path: Path) -> str:
    """Return correct code fence language for file type."""
    name = path.name.lower()
    if name.endswith(".py"): return "python"
    if name == "makefile": return "makefile"
    if name == "pyproject.toml": return "toml"
    if name.endswith((".yaml", ".yml")): return "yaml"
    if name.endswith(".md"): return "markdown"
    return "text"

def load_files() -> List[Item]:
    """Load all supported files with proper display names and fencing."""
    patterns = ["*.py", "*.md", "*.yaml", "*.yml", "Makefile", "pyproject.toml"]
    items = []

    for pattern in patterns:
        for p in Path(".").rglob(pattern):
            if any(part in IGNORE_DIRS or part.startswith(".") for part in p.parts):
                continue
            if p.name.startswith(".") and p.name not in {"Makefile", "pyproject.toml"}:
                continue
            try:
                rel = p.relative_to(".")
                display_name = str(rel)
                content = p.read_text(encoding="utf-8")
                items.append(Item(display_name, content, str(p)))
            except Exception:
                pass
    return sorted(items, key=lambda x: x.name.lower())

# === LOAD PROMPTS ===
def load_prompts(prompts_yaml_path: str) -> List[Item]:
    try:
        with open(prompts_yaml_path, encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        return [Item(p["name"], p["text"]) for p in data.get("prompts", [])]
    except Exception as e:
        console.print(f"[red]Failed to load prompts: {e}[/red]")
        return []

# === STATE ===
mode = "file"  # start in file mode
all_items = {"file": [], "prompt": []}  # Will be populated in main()
current_items = []
filtered = []
selected_idx = 0
search_term = ""
selected_file: Optional[Item] = None
prompt_items = []  # Renamed to avoid conflict with typer parameter
files = []

# === SMART INJECTION ===
def inject_file_content(prompt_text: str, file_item: Item) -> str:
    rel_path = Path(file_item.path).relative_to(".")
    fence_lang = get_fence_for_path(Path(file_item.path))
    code_block = f"```{fence_lang}\n{file_item.content}\n```"

    # Replace {__FILE__} first
    text = prompt_text.replace("{__FILE__}", str(rel_path))

    # Find first code block opening
    match = re.search(r"```", text)
    if not match:
        return text.rstrip() + "\n\n" + code_block

    # Insert right after the first ```
    pos = match.end()
    return text[:pos] + "\n" + code_block + text[pos:]

# === KEY BINDINGS (only enter changed) ===
kb = KeyBindings()

@kb.add("c-c")
@kb.add("escape")
def _exit(event):
    event.app.exit()

@kb.add("enter")
def _copy(event):
    global selected_file, mode, current_items, filtered, selected_idx, search_term

    if not filtered:
        return

    chosen = filtered[selected_idx]

    if mode == "file":
        selected_file = chosen
        console.print(f"\n[bold green]Selected:[/bold green] {chosen.name}")
        mode = "prompt"
        current_items = all_items["prompt"]
        search_term = ""
        selected_idx = 0
        update_filter()
        event.app.invalidate()
        return

    # mode == "prompt"
    if chosen.name.strip().lower() == "current directory structure":
        # Run the tree command and copy output in a bash code block
        import subprocess
        try:
            tree_output = subprocess.check_output("tree", encoding="utf-8", stderr=subprocess.STDOUT)
        except Exception as e:
            tree_output = f"[tree command failed: {e}]"
        bash_block = f"Here is the current directory structure:\n```bash\n{tree_output}\n```"
        pyperclip.copy(bash_block)
        console.print(f"\n[bold yellow]Directory structure copied as bash code block![/bold yellow]")
        console.print(f"   Prompt: {chosen.name}")
    elif selected_file:
        final_text = inject_file_content(chosen.content, selected_file)
        pyperclip.copy(final_text + "\n")
        console.print(f"\n[bold magenta]Injected & copied![/bold magenta]")
        console.print(f"   File: {selected_file.name}")
        console.print(f"   Prompt: {chosen.name}")
    else:
        pyperclip.copy(chosen.content + "\n")
        console.print(f"\n[bold cyan]Copied prompt (no file):[/] {chosen.name}")

    time.sleep(DEFAULT_SLEEP_SECONDS)
    event.app.exit()

# === MODE SWITCHING (unchanged except f now doesn't clear selected_file) ===
@kb.add("escape", "p")   # Alt+P
def _(event):
    global mode, current_items, filtered, selected_idx, search_term
    mode = "prompt"
    current_items = all_items["prompt"]
    search_term = ""
    selected_idx = 0
    update_filter()
    event.app.invalidate()

@kb.add("escape", "f")   # Alt+F
def _(event):
    global mode, current_items, filtered, selected_idx, search_term
    mode = "file"
    current_items = all_items["file"]
    search_term = ""
    selected_idx = 0
    update_filter()
    event.app.invalidate()
    
# === Navigation & search (100% your original code) ===
@kb.add("up")
def _(event):
    global selected_idx
    if filtered:
        selected_idx = (selected_idx - 1) % len(filtered)
    event.app.invalidate()

@kb.add("down")
def _(event):
    global selected_idx
    if filtered:
        selected_idx = (selected_idx + 1) % len(filtered)
    event.app.invalidate()

@kb.add("backspace")
def _(event):
    global search_term, selected_idx
    if search_term:
        search_term = search_term[:-1]
        selected_idx = 0
        update_filter()
        event.app.invalidate()

@kb.add(Keys.Any)
def _(event):
    global search_term, selected_idx
    if len(event.data) == 1 and event.data.isprintable():
        search_term += event.data
        selected_idx = 0
        update_filter()
        event.app.invalidate()

# === FILTERING ===
def update_filter():
    global filtered
    term = search_term.lower()
    if not term:
        filtered = current_items.copy()
    else:
        filtered = [i for i in current_items if term in i.name.lower()]

# === UI (only small enhancement to show selected file) ===
def get_left_panel():
    lines = []
    for i, item in enumerate(filtered):
        prefix = ">" if i == selected_idx else " "
        lines.append(f"{prefix} {item}")
    return "\n".join(lines) or "No items"

def get_right_panel():
    if not filtered:
        return "No matches"
    item = filtered[selected_idx]
    header = f"Preview — {item.name}"

    if mode == "file":
        fence = get_fence_for_path(Path(item.path))
        preview_block = f"```{fence}\n{item.content}\n```"
        note = "\n\n[bold green]Press Enter to select → then pick a prompt[/]"
        return f"{header}\n{'─' * 60}\n{preview_block}{note}"

    # Prompt mode
    if selected_file:
        preview = inject_file_content(item.content, selected_file)
        note = "\n\n[bold magenta]This is exactly what will be copied on Enter[/]"
    else:
        preview = item.content
        note = "\n\n[dim](Select a file first with F to see injection preview)[/]"

    return f"{header}\n{'─' * 60}\n{preview}{note}"


def get_ui():
    file_info = f" | [bold greenFile:[/] {selected_file.name}" if selected_file else ""

    return HSplit([
        VSplit([
            Window(content=FormattedTextControl(get_left_panel), width=50, wrap_lines=True),
            Window(width=1, char="│"),
            Window(content=FormattedTextControl(get_right_panel), wrap_lines=True),
        ]),
        Window(height=1, char="─"),
        Window(
            content=FormattedTextControl(lambda: f" > {search_term or '(type to search)'}"),
            height=1,
            style="class:search-bar"
        ),
        Window(
            content=FormattedTextControl(
                lambda: f" Mode: {'Prompts' if mode == 'prompt' else 'Files'} {file_info}  •  "
                        f"{len(filtered)} shown  •  P/F switch  •  Enter = select"
            ),
            height=1,
            style="class:status-bar"
        ),
    ])

# === APP ===
style = Style.from_dict({
    'search-bar': DEFAULT_SEARCH_BAR_STYLE,
    'status-bar': DEFAULT_STATUS_BAR_STYLE,
})

@app.command()
def main(
    prompts: Optional[str] = typer.Option(
        None,
        "--prompts",
        help="Path to custom prompts YAML file. If not specified, uses default fallback strategy."
    )
):
    """LLM Prompt + Smart File Injector with support for custom prompts file."""
    global prompt_items, files, all_items, current_items, filtered
    
    # Initialize prompts and files with the resolved path
    prompts_yaml_path = get_prompts_yaml_path(prompts)
    prompt_items = load_prompts(prompts_yaml_path)
    files = load_files()
    
    # Update global state
    all_items = {"file": files, "prompt": prompt_items}
    current_items = all_items[mode]
    update_filter()
    
    console.print(
        "[bold cyan]F[/]irst pick a file  →  [bold magenta]P[/]ick a prompt  →  "
        "[bold green]Auto-injects with correct code block & {__FILE__} replaced![/]"
    )
    
    # Create and run the prompt-toolkit app
    prompt_app = Application(
        layout=PTLayout(get_ui()),
        full_screen=True,
        key_bindings=kb,
        mouse_support=True,
        style=style,
    )
    prompt_app.run()

if __name__ == "__main__":
    app()