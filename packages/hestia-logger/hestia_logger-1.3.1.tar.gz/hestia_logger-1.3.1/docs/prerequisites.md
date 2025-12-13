# ⚡️ Prerequisites

Before installing **HESTIA**, ensure you have the following dependencies installed:

- Python 3.10+
- uv or pip Python Package Manager
- Git
- Docker & Docker Compose
- Elasticsearch (Optional, for centralized logging)
- Kibana (Optional, for log visualization)
- Grafana (Optional, for advanced monitoring)

---

## 🐍 Python 3.10+

Ensure you have **Python 3.10+** installed. If not, download and install it from the [official Python website](https://www.python.org/downloads/). Check your version:

```bash
python --version
```
For installation guides and troubleshooting, refer to the [RealPython](https://realpython.com/installing-python/) documentation.

## 📦 Package managers


=== "uv"

    !!! tip "Why We Recommend uv Over pip"

        While pip is the standard Python package manager, **we strongly recommend using uv for managing dependencies and projects**.

        - **Lightning-fast Dependency Management** – uv resolves, installs, and locks dependencies extremely quickly, even for large projects.
        - **Built-in Virtual Environments & Python Management** – uv automatically creates and manages isolated environments and can install/manage Python versions for you.
        - **Reproducible Installs** – uv uses `pyproject.toml` and `uv.lock` to ensure consistent, repeatable environments across machines.
        - **Unified Workflow** – uv consolidates the functionality of tools like `uv`, `pip`, `pip-tools`, `pipx`, `virtualenv`, `poetry`, `pyenv`, and `twine` into a single tool.

        For long-term projects and production environments, uv provides a **robust, scalable, and fast solution** compared to plain pip.

    Install uv as package and dependency manager:

    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

    Check if uv is installed correctly:

    ```bash
    uv --version
    ```

=== "pip"

    !!! info "Knowledge"

        If you don't have prior experience with Python, we recommend reading
        [Using Python's pip to Manage Your Projects' Dependencies], which is a
        really good introduction on the mechanics of Python package management and
        helps you troubleshoot if you run into errors.

    [Python package]: https://pypi.org/project/hestia-logger/
    [virtual environment]: https://realpython.com/what-is-pip/#using-pip-in-a-python-virtual-environment
    [semantic versioning]: https://semver.org/
    [Using Python's pip to Manage Your Projects' Dependencies]: https://realpython.com/what-is-pip/

    Upgrade pip to the latest version: 

    ``` sh
    python -m pip install --upgrade pip
    ```

## 🌱 Git

Ensure you have **Git** installed. If not, download and install it from the [official Git website](https://git-scm.com/downloads). Check your version:

```bash
git --version
```

## 🐳 Docker & Docker Compose

To demonstrate **HESTIA Asynchronous Logger** using Docker, ensure you have Docker and Docker Compose installed. Download and install Docker from the official website:

- [Docker Engine](https://docs.docker.com/engine/install/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Docker Desktop](https://docs.docker.com/desktop/)

Verify installation with: 

```bash
docker version
```

```bash
docker compose version
```

### Why Docker?

- Runs Hestia services in isolated containers
- Makes it easier to deploy logging services like Elasticsearch, Kibana, and Grafana

Now that prerequisites are set, continue with **configuration**. 🎯

  [HESTIA Asynchronous Logger]: https://pypi.org/project/hestia-logger/
  [GitHub]: https://github.com/fox-techniques/hestia-logger
  [uv]: https://docs.astral.sh/uv/