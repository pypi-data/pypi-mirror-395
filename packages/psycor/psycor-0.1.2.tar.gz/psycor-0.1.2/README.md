# Psycor

Psycor is a lightweight CLI tool for generating Python project scaffolding, managing virtual environments, and installing dependencies — all driven by a simple `psycor.toml` configuration file.

It combines template-based project creation with minimal dependency and environment management, offering a consistent workflow for Python, FastAPI, and Flask projects.

> **Status:** Experimental (v0.1.2). API and template structure may evolve.

---

## Features

- Generate new projects from predefined templates  
- Automatically create and manage virtual environments  
- Install runtime and development dependencies defined in `psycor.toml`  
- Add new dependencies dynamically with `psycor add`  
- Launch an activated shell inside the project's virtual environment (`psycor venv`)  
- Simple, extensible configuration system  
- Built-in templates for Python, FastAPI, and Flask

---

## Installation

Install from PyPI:

```
pip install psycor
```

Verify installation:

```
psycor --help
```

---

## Quick Start

### 1. Create a new project

```
psycor create my-app --template python
```

List available templates:

```
psycor create --list
```

### OR initialize Psycor in an existing directory

```
cd my-app
psycor init
```

This creates the Psycor configuration file for the project.

### 2. Install dependencies and create the virtual environment

```
cd my-app
psycor install
```

### 3. Activate the virtual environment

```
psycor venv
```

Type `exit` to return to your previous shell.

### 4. Add new dependencies

```
psycor add requests httpx
```

This installs the packages and updates your `psycor.toml`.

---

## Project Configuration (`psycor.toml`)

Each generated project includes a configuration file that defines metadata, dependency groups, and virtual environment behavior.

Example:

```
[project]
name = "my-app"

[venv]
path = ".venv"

[dependencies]
runtime = ["fastapi", "uvicorn"]
dev = ["pytest"]

[commands]
# Reserved for future use
```

Psycor relies on this file to manage environments and installation logic.

---

## Templates

Psycor templates live under:

```
psycor/templates/<template-name>/
```

A template folder typically contains:

- Directory structure to copy  
- A `psycor.toml` file  
- Starter code files  

Built-in templates include:

- `python` — minimal Python project  
- `fastapi` — basic FastAPI application  
- `flask` — basic Flask application  

You can add additional templates by simply creating new folders under `templates/`.

---

## CLI Commands

| Command | Description |
|--------|-------------|
| `psycor create NAME --template T` | Create a new project from a template |
| `psycor create --list` | List available templates |
| `psycor init` | Initialize Psycor configuration in an existing directory |
| `psycor install` | Create the virtual environment and install dependencies |
| `psycor venv` | Open a shell with the environment activated |
| `psycor add pkg1 pkg2 ...` | Install and register additional dependencies |

---

## Experimental Status

This project is early-stage (v0.1.2).  
Behavior and APIs may change as development continues.  
Feedback and contributions are welcome.

---

## License

This project is licensed under the MIT License.  
See the `LICENSE` file for more details.