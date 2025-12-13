# jps-llm-prompt-app

![Build](https://github.com/jai-python3/jps-llm-prompt-app/actions/workflows/test.yml/badge.svg)
![Publish to PyPI](https://github.com/jai-python3/jps-llm-prompt-app/actions/workflows/publish-to-pypi.yml/badge.svg)
[![codecov](https://codecov.io/gh/jai-python3/jps-llm-prompt-app/branch/main/graph/badge.svg)](https://codecov.io/gh/jai-python3/jps-llm-prompt-app)

A lightweight command-line application for interactively browsing, filtering, and selecting prompts for Large Language Models (LLMs).  
Built using **Prompt Toolkit** for a responsive, modern CLI experience with incremental search and auto-completion.

---

## 🚀 Overview

`jps-llm-prompt-app` streamlines prompt selection for developers who frequently interact with LLMs (e.g., ChatGPT, Claude, Gemini, local models).

Key goals:

- Maintain a curated catalog of reusable prompts (e.g., coding requests, refactoring templates, testing prompts).
- Search prompts interactively by keyword as you type.
- Narrow the menu dynamically using fuzzy/incremental search.
- Select a prompt and either:
  - print it to stdout,
  - copy to clipboard (optional feature),
  - or pass it directly to another tool.

Ideal for engineers who reuse structured prompts or maintain prompt libraries.

---

## ✨ Features

### ✅ Interactive Prompt Navigator
- Incremental search while typing  
- Auto-completion based on available prompts  
- Keyboard-driven navigation (arrows, tab completion, enter to select)

### ✅ Flexible Prompt Catalog
- Load prompts from:
  - built-in prompt sets  
  - user-defined YAML/JSON files  
  - additional plugin directories (future enhancement)

### ✅ CLI Tools
- `jps-llm-prompt-app` → interactive interface  
- Options for outputting or piping selected prompts  
- Rich text preview before selection

### 🔧 Extensible Architecture
- Clean separation of:
  - prompt data source manager  
  - search engine  
  - UI components (Prompt Toolkit-based)  
- Easily integrate with wrappers for API clients or shell workflows

---

## 📘 Example Usage

### Start the interactive prompt selector:

```bash
jps-llm-prompt-app
```

### Search Behavior
As you type:

- Prompts are dynamically filtered
- Matching text is highlighted
- You may select using ↑/↓ and press Enter

## 📦 Installation

Install locally for development:

```bash
make install
```

Or via pip (after PyPI publish):

```bash
pip install jps-llm-prompt-app
```

## 🧪 Development

```bash
make fix && make format && make lint
make test
```

To run the app directly during development:

```bash
python -m jps_llm_prompt_app
```

## 📜 License
MIT License © Jaideep Sundaram