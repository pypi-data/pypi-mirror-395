import os


DEFAULT_PROMPTS_YAML_FILE = os.path.join(os.path.dirname(__file__), "conf", "prompts.yaml")

DEFAULT_SLEEP_SECONDS = 3

DEFAULT_SEARCH_BAR_STYLE = 'bg:#003366 #ffffff bold'
DEFAULT_STATUS_BAR_STYLE = 'bg:#000000 #888888'

IGNORE_DIRS = {
    ".git",
    "__pycache__",
    ".venv",
    "venv",
    "env",
    ".env",
    "build",
    "dist",
    ".git",
    ".hg",
    ".svn",
    "node_modules",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".tox",
}