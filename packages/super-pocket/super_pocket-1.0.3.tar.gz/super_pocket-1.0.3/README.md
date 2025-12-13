# Super Pocket
<div align="center">
  <a href="https://pocketdocs.readthedocs.io/en/latest/?badge=latest&style=plastic&logo=readthedocs">
    <img src="https://readthedocs.org/projects/pocketdocs/badge/?version=latest">
  </a>
  <a href="https://www.python.org/downloads/">
    <img src="https://img.shields.io/badge/python-3.11%2B-blue?style=plastic&logo=python&logoColor=yellow">
  </a>
  <a href="https://opensource.org/licenses/MIT">
    <img src="https://img.shields.io/badge/License-MIT-pink.svg?style=plastic">
  </a>
  <a href="https://pypi.org/project/super-pocket/">
    <img src="https://img.shields.io/pypi/v/super-pocket?style=plastic&logo=python&logoColor=yellow">
  </a>
  
</div>

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
  brew tap dim-gggl/brew && brew install super-pocket
  ```

- **With uv (recommended):**
  ```bash
  uv tool install super-pocket
  ```

- **With pip/pipx:**
It is **Highly recommended** to use a virtual environment.
  ```bash
  python3 -m venv venv
  source venv/bin/activate

  pip install super-pocket
  # or
  pipx install super-pocket
  ```

- Quick check: `pocket --version` should answer without whining.
- Double check: `which pocket`, in this case should return `your/project/path/venv/bin/pocket`

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

- List: `pocket documents list`  
- Copy a template: `pocket documents copy unit_tests_agent -o .AGENTS/`  
- Initialize everything at once: `pocket documents init -o .AGENTS`

### Convert a file to PDF

- `pocket pdf convert README.md -o README.pdf`  
- Output: a clean PDF without fighting LaTeX.

### Web goodies

- Favicons: `pocket web favicon logo.png -o favicon.ico --sizes "64x64,32x32"`  
- Job search: `pocket web job-search "python developer" --work_from_home -o jobs.json` (set `RAPIDAPI_API_KEY` in your env).

### Generate LLM-friendly XML

- `pocket xml "note:<hello world>"`  
- Output: `<note>hello world</note>` (chain multiple tags, it keeps up).

### Quick cheatsheets

- View in 2s: `pocket documents view SQL -t cheatsheet`  
- Local copy to work offline: `pocket documents copy git -o docs/cheats/`

### Stand-alone mode (scripts)

Everything above works directly from the CLI without the interactive UI. Perfect for CI or your own automation scripts.

The initial command `pocket` is a way to unify all these tools, but it also works to do:
`req-to-date requirements.txt`
`proj2md -p . -o proj2md.md`
`xml "context:<Job interview post:<back-end developer>>"`
> This last command should return:
> <context>
>  Job interview
>  <post>back-end developer</post>
> </context>