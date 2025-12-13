# 🔧 Configuration 

**HESTIA Asynchronous Logger** relies on environment variables and Docker secrets to securely store configuration values. Below is a guide on how to configure the service.


## 🌍 Environment Variables 

**HESTIA** loads configuration from a `.env` file or system environment variables. The following default `.env.example` file is provided for local development. 

Create a copy of `.env.example` file in the project root:

```sh
cp .env.example .env
```

To use this configuration, and modify the values as needed.

!!! tip "Note" 

    **HESTIA** accepts `.env` as little as:
    
    ```sh title=".env" linenums="1"
    # ========================
    # 🏷️ Application Version
    # ========================
    APP_VERSION=1.0.0

    # ========================
    # 🌍 Runtime Environment
    # Options: local, container, production
    # ========================
    ENVIRONMENT=local

    # ========================
    # 🔊 Logging Level
    # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
    # ========================
    LOG_LEVEL=INFO
    ```


---

Now that environment variables are set, continue with **installation**. 🎯
