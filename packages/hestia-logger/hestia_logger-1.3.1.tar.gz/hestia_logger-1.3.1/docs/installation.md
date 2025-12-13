# 📥 Installation

**HESTIA** uses the following dependencies which will be installed automatically:

1. **[`python-dotenv`](https://pypi.org/project/python-dotenv/)** – Loads environment variables from `.env`.  
2. **[`coloredlogs`](https://pypi.org/project/coloredlogs/)** – Provides colored log output for better readability.  
3. **[`elasticsearch`](https://pypi.org/project/elasticsearch/)** – Required for sending logs to Elasticsearch.  
4. **[`python-json-logger`](https://pypi.org/project/python-json-logger/)** – Formats logs as structured JSON (useful for Logstash & Kibana).  
5. **[`fastapi`](https://fastapi.tiangolo.com/)** – Likely used for exposing logs via an API endpoint.  
6. **[`requests`](https://pypi.org/project/requests/)** – Standard HTTP library for making API calls.  
7. **[`structlog`](https://pypi.org/project/structlog/)** – Enhances logging with structured data.  
8. **[`httpx`](https://pypi.org/project/httpx/)** – Async HTTP client (may be used for async logging or external APIs).  


## 🌞 uv Python Package Manager

We highly recommend using **uv** for its fast dependency management and built-in virtual environment handling.

**To start a new project:**

```bash
uv init my_project
cd my_project
``` 

This creates a structured Python project with `pyproject.toml` (and a uv.lock file once dependencies are synced).

**Using uv in an existing project:**

If you already have a project folder (optionally with a `pyproject.toml`), you can initialize it with:

```bash
uv init 
``` 

Then add dependencies as needed:

```bash
uv add <package-name>
``` 

**Creating & Using a Virtual Environment:**

```bash
uv venv 
``` 

uv creates and manages a .venv for your project when you install dependencies. To install everything from `pyproject.toml`:

```bash
uv sync
``` 

This will sync  all the dependencies into the virtual environment.

**Install HESTIA:**

Inside your project directory, run:

```bash
uv add hestia-logger
uv sync
``` 

This adds **HESTIA** to your dependencies and installs it into the project’s virtual environment.

---

## 📦 pip 

**HESTIA Asynchronous Logger** is published as a python package and can be installed with
`pip`, ideally by using a [virtual environment]. Open up a terminal and install with:

=== "Latest"

    ``` sh
    pip install hestia-logger
    ```

=== "1.x"

    ``` sh
    pip install hestia-logger=="1.*" # (1)!
    ```

    1.  **HESTIA** uses [semantic versioning].

        This will make sure that you don't accidentally [upgrade to the next
        major version], which may include breaking changes that silently corrupt
        your site. Additionally, you can use `pip freeze` to create a lockfile,
        so builds are reproducible at all times:

        ```
        pip freeze > requirements.txt
        ```

        Now, the lockfile can be used for installation:

        ```
        pip install -r requirements.txt
        ```

This will automatically install compatible versions of all dependencies. **HESTIA** always strives to support the latest versions, so there's no need to
install those packages separately.

---

## 🐙 GitHub

**HESTIA** can be directly used from [GitHub] by cloning the
repository into a subfolder of your project root which might be useful if you
want to use the very latest version:

```bash
git clone https://github.com/fox-techniques/hestia-logger.git
cd hestia-logger
pip install -e .

```

---

🤩 **CONGRAGULATIONS!** Continue to the **usage**. Let's keep going...🚀
