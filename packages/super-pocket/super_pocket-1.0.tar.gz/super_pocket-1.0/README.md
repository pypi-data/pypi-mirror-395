# Super Pocket

[![Documentation Status](https://readthedocs.org/projects/pocketdocs/badge/?version=latest)](https://pocketdocs.readthedocs.io/en/latest/?badge=latest)
[![Static Badge](https://img.shields.io/badge/python-3.11%2B-blue?style=plastic&logo=python&logoColor=yellow)
](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)


![](./pocket_shaded.png)

## What's in the pocket ?

- **Readme Generator**: Analyze your project (FastAPI project, CLI Tool, Python Package) and generate the best README.md possible for the purpose.
  
- **Codebase to Markdown**: Scan the codebase of your project and generate a unique Markdown file containing all the project files with project tree. Perfect to share with LLMs.
  
- **XML Tags easy**: Using a custom syntax on format `tag:<content>`, it produces the XML tags -> `<tag>content</tag>`. Also LLM's friendly.
  
- **Agent Templates**: Manage and distribute AI agent configuration templates such as AGENTS.md.
- **Cheatsheets**: Quick access to development cheatsheets
- **Dependencies Scanner**: Scan a requirements.txt or pyproject.toml and gives you the outdated packages in a well-printed list (with colors !)

## Install it fast

- **With Homebrew (macOS/Linux):**
  ```bash
  brew tap dim-gggl/super-pocket && brew install super-pocket
  ```

- **With uv (recommended):**
  ```bash
  uv tool install super-pocket
  ```

- **With pip/pipx:**
  ```bash
  pip install super-pocket
  # or
  pipx install super-pocket
  ```

- Local wheel: `pip install dist/super_pocket-*.whl` if you build it yourself.
- Quick check: `pocket --version` should answer without whining.

## Quick usage

### Interactive mode (the easy way)

Don't know where to start? Just type:
```bash
pocket
```
This launches a guided interactive menu. Navigate through tools, get prompted for parameters, and explore features without memorizing commands. Type `exit` or `Q` to quit.

### Direct commands

- Terminal power-users: `pocket --help` for the menu, then `pocket <group> --help` to zoom in.
- Concrete examples below (all available stand-alone).

### Craft a README without sweating

- `pocket project readme -p .` scans the repo, asks a few questions, and spits out a full README.  
- Expected output: a push-ready README.md with sections and badges aligned to your stack.

### Dump the whole codebase into one Markdown

- `pocket project to-file -p . -o project-all-in-one.md`  
- Output: one file with the tree + every file inline. Perfect to drop into an LLM.

### Render Markdown nicely in the terminal

- `pocket markdown render README.md -w 100`  
- Output: your Markdown with colors and aligned titles directly in the terminal.

### Spot the dusty dependencies

- `pocket project req-to-date requirements.txt`  
- Typical output: `fastapi 0.110.0 -> 0.121.3` (red for the old, green for the new).

### Agent templates and cheatsheets

- List: `pocket templates list`  
- Copy a template: `pocket templates copy unit_tests_agent -o .AGENTS/`  
- Initialize everything at once: `pocket templates init -o .AGENTS`

### Convert a file to PDF

- `pocket pdf convert README.md -o README.pdf`  
- Output: a clean PDF without fighting LaTeX.

### Web goodies

- Favicons: `pocket web favicon logo.png -o favicon.ico --sizes "64x64,32x32"`  
- Job search: `pocket web job-search "python developer" --work_from_home -o jobs.json` (set `RAPIDAPI_API_KEY` in your env).

### Generate LLM-friendly XML

- `pocket xml "note:hello world"`  
- Output: `<note>hello world</note>` (chain multiple tags, it keeps up).

### Quick cheatsheets

- View in 2s: `pocket templates view SQL -t cheatsheet`  
- Local copy to work offline: `pocket templates copy git -o docs/cheats/`

### Stand-alone mode (scripts)

Everything above works directly from the CLI without the interactive UI. Perfect for CI or your own automation scripts.
