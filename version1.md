**Documenation when we switch to uv**

- uv package manager (use `uv pip install` to install dependencies)

2. Setup and activate virtual environement
First, follow ultraviolet ssh installation instructions: https://github.com/astral-sh/uv
```bash
uv init
source .venv/bin/activate # On Unix/MacOS
# or
.venv/Scripts/activate # On Windows
```

3. Install dependencies:
```bash
uv pip install streamlit pandas ollama plotly
```