# FastAPI Logging (beans-logging-fastapi)

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit)
[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/bybatkhuu/module-fastapi-logging/2.build-publish.yml?logo=GitHub)](https://github.com/bybatkhuu/module-fastapi-logging/actions/workflows/2.build-publish.yml)
[![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/bybatkhuu/module-fastapi-logging?logo=GitHub&color=blue)](https://github.com/bybatkhuu/module-fastapi-logging/releases)

This is a middleware for FastAPI HTTP access logs. It is based on **'beans-logging'** package.

## ✨ Features

- **Logger** based on **'beans-logging'** package
- **FastAPI** HTTP access logging **middleware**

---

## 🛠 Installation

### 1. 🚧 Prerequisites

- Install **Python (>= v3.10)** and **pip (>= 23)**:
    - **[RECOMMENDED] [Miniconda (v3)](https://www.anaconda.com/docs/getting-started/miniconda/install)**
    - *[arm64/aarch64] [Miniforge (v3)](https://github.com/conda-forge/miniforge)*
    - *[Python virutal environment] [venv](https://docs.python.org/3/library/venv.html)*

[OPTIONAL] For **DEVELOPMENT** environment:

- Install [**git**](https://git-scm.com/downloads)
- Setup an [**SSH key**](https://docs.github.com/en/github/authenticating-to-github/connecting-to-github-with-ssh)

### 2. 📦 Install the package

[NOTE] Choose one of the following methods to install the package **[A ~ F]**:

**OPTION A.** [**RECOMMENDED**] Install from **PyPi**:

```sh
pip install -U beans-logging-fastapi
```

**OPTION B.** Install latest version directly from **GitHub** repository:

```sh
pip install git+https://github.com/bybatkhuu/module-fastapi-logging.git
```

**OPTION C.** Install from the downloaded **source code**:

```sh
git clone https://github.com/bybatkhuu/module-fastapi-logging.git && \
    cd ./module-fastapi-logging

# Install directly from the source code:
pip install .

# Or install with editable mode:
pip install -e .
```

**OPTION D.** Install for **DEVELOPMENT** environment:

```sh
pip install -e .[dev]

# Install pre-commit hooks:
pre-commit install
```

**OPTION E.** Install from **pre-built release** files:

1. Download **`.whl`** or **`.tar.gz`** file from [**releases**](https://github.com/bybatkhuu/module-fastapi-logging/releases)
2. Install with pip:

```sh
# Install from .whl file:
pip install ./beans_logging_fastapi-[VERSION]-py3-none-any.whl

# Or install from .tar.gz file:
pip install ./beans_logging_fastapi-[VERSION].tar.gz
```

**OPTION F.** Copy the **module** into the project directory (for **testing**):

```sh
# Install python dependencies:
pip install -r ./requirements.txt

# Copy the module source code into the project:
cp -r ./src/beans_logging_fastapi [PROJECT_DIR]
# For example:
cp -r ./src/beans_logging_fastapi /some/path/project/
```

## 🚸 Usage/Examples

To use `beans_logging_fastapi`:

### **FastAPI**

[**`configs/logger.yml`**](./examples/configs/logger.yml):

```yaml
logger:
  app_name: "fastapi-app"
  intercept:
    mute_modules: ["uvicorn.access"]
  handlers:
    default.all.file_handler:
      enabled: true
    default.err.file_handler:
      enabled: true
    default.all.json_handler:
      enabled: true
    default.err.json_handler:
      enabled: true
  extra:
    http_std_debug_format: '<n>[{request_id}]</n> {client_host} {user_id} "<u>{method} {url_path}</u> HTTP/{http_version}"'
    http_std_msg_format: '<n><w>[{request_id}]</w></n> {client_host} {user_id} "<u>{method} {url_path}</u> HTTP/{http_version}" {status_code} {content_length}B {response_time}ms'
    http_file_enabled: true
    http_file_format: '{client_host} {request_id} {user_id} [{datetime}] "{method} {url_path} HTTP/{http_version}" {status_code} {content_length} "{h_referer}" "{h_user_agent}" {response_time}'
    http_file_tz: "localtime"
    http_log_path: "http/{app_name}.http.access.log"
    http_err_path: "http/{app_name}.http.err.log"
    http_json_enabled: true
    http_json_path: "http.json/{app_name}.http.json.access.log"
    http_json_err_path: "http.json/{app_name}.http.json.err.log"
```

[**`.env`**](./examples/.env):

```sh
ENV=development
DEBUG=true
```

[**`logger.py`**](./examples/logger.py):

```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from loguru import Record

from beans_logging import Logger, LoggerLoader
from beans_logging_fastapi import (
    add_http_file_handler,
    add_http_file_json_handler,
    http_file_format,
)

logger_loader = LoggerLoader()
logger: Logger = logger_loader.load()


def _http_file_format(record: "Record") -> str:
    _format = http_file_format(
        record=record,
        msg_format=logger_loader.config.extra.http_file_format,  # type: ignore
        tz=logger_loader.config.extra.http_file_tz,  # type: ignore
    )
    return _format


if logger_loader.config.extra.http_file_enabled:  # type: ignore
    add_http_file_handler(
        logger_loader=logger_loader,
        log_path=logger_loader.config.extra.http_log_path,  # type: ignore
        err_path=logger_loader.config.extra.http_err_path,  # type: ignore
        formatter=_http_file_format,
    )

if logger_loader.config.extra.http_json_enabled:  # type: ignore
    add_http_file_json_handler(
        logger_loader=logger_loader,
        log_path=logger_loader.config.extra.http_json_path,  # type: ignore
        err_path=logger_loader.config.extra.http_json_err_path,  # type: ignore
    )


__all__ = [
    "logger",
    "logger_loader",
]
```

[**`main.py`**](./examples/main.py):

```python
#!/usr/bin/env python

from typing import Union
from contextlib import asynccontextmanager

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse

load_dotenv()

from beans_logging_fastapi import (
    HttpAccessLogMiddleware,
    RequestHTTPInfoMiddleware,
    ResponseHTTPInfoMiddleware,
)

from logger import logger, logger_loader
from __version__ import __version__


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Preparing to startup...")
    logger.success("Finished preparation to startup.")
    logger.info(f"API version: {__version__}")

    yield
    logger.info("Praparing to shutdown...")
    logger.success("Finished preparation to shutdown.")


app = FastAPI(lifespan=lifespan, version=__version__)

app.add_middleware(ResponseHTTPInfoMiddleware)
app.add_middleware(
    HttpAccessLogMiddleware,
    debug_format=logger_loader.config.extra.http_std_debug_format,  # type: ignore
    msg_format=logger_loader.config.extra.http_std_msg_format,  # type: ignore
)
app.add_middleware(
    RequestHTTPInfoMiddleware, has_proxy_headers=True, has_cf_headers=True
)


@app.get("/")
def root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/continue", status_code=100)
def get_continue():
    return {}


@app.get("/redirect")
def redirect():
    return RedirectResponse("/")


@app.get("/error")
def error():
    raise HTTPException(status_code=500)


if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host="0.0.0.0",
        port=8000,
        access_log=False,
        server_header=False,
        proxy_headers=True,
        forwarded_allow_ips="*",
    )
```

Run the [**`examples`**](./examples):

```sh
cd ./examples
# Install python dependencies for examples:
pip install -r ./requirements.txt

uvicorn main:app --host=0.0.0.0 --port=8000
```

**Output**:

```txt
[2025-12-01 00:00:00.735 +09:00 | TRACE | beans_logging._intercept:96]: Intercepted modules: ['potato_util.io', 'concurrent', 'potato_util', 'fastapi', 'uvicorn.error', 'dotenv.main', 'potato_util._base', 'watchfiles.watcher', 'dotenv', 'potato_util.io._sync', 'asyncio', 'uvicorn', 'concurrent.futures', 'watchfiles', 'watchfiles.main']; Muted modules: ['uvicorn.access'];
[2025-12-01 00:00:00.735 +09:00 | INFO  | uvicorn.server:84]: Started server process [13580]
[2025-12-01 00:00:00.735 +09:00 | INFO  | uvicorn.lifespan.on:48]: Waiting for application startup.
[2025-12-01 00:00:00.735 +09:00 | INFO  | main:25]: Preparing to startup...
[2025-12-01 00:00:00.735 +09:00 | OK    | main:26]: Finished preparation to startup.
[2025-12-01 00:00:00.735 +09:00 | INFO  | main:27]: API version: 0.0.0
[2025-12-01 00:00:00.735 +09:00 | INFO  | uvicorn.lifespan.on:62]: Application startup complete.
[2025-12-01 00:00:00.735 +09:00 | INFO  | uvicorn.server:216]: Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
[2025-12-01 00:00:00.736 +09:00 | DEBUG | anyio._backends._asyncio:986]: [4386400aab364895ba272f3200d2a778] 127.0.0.1 - "GET / HTTP/1.1"
[2025-12-01 00:00:00.736 +09:00 | OK    | anyio._backends._asyncio:986]: [4386400aab364895ba272f3200d2a778] 127.0.0.1 - "GET / HTTP/1.1" 200 17B 0.9ms
^C[2025-12-01 00:00:00.750 +09:00 | INFO  | uvicorn.server:264]: Shutting down
[2025-12-01 00:00:00.750 +09:00 | INFO  | uvicorn.lifespan.on:67]: Waiting for application shutdown.
[2025-12-01 00:00:00.750 +09:00 | INFO  | main:30]: Praparing to shutdown...
[2025-12-01 00:00:00.750 +09:00 | OK    | main:31]: Finished preparation to shutdown.
[2025-12-01 00:00:00.750 +09:00 | INFO  | uvicorn.lifespan.on:76]: Application shutdown complete.
[2025-12-01 00:00:00.750 +09:00 | INFO  | uvicorn.server:94]: Finished server process [13580]
```

👍

---

## ⚙️ Configuration

[**`templates/configs/config.yml`**](./templates/configs/config.yml):

```yaml
logger:
  # app_name: "app"
  default:
    level:
      base: INFO
      err: WARNING
    format_str: "[{time:YYYY-MM-DD HH:mm:ss.SSS Z} | {extra[level_short]:<5} | {name}:{line}]: {message}"
    file:
      logs_dir: "./logs"
      rotate_size: 10000000
      rotate_time: "00:00:00"
      retention: 90
      encoding: utf8
    custom_serialize: false
  intercept:
    enabled: true
    only_base: false
    ignore_modules: []
    include_modules: []
    mute_modules: ["uvicorn.access"]
  handlers:
    default.all.std_handler:
      type: STD
      format: "[<c>{time:YYYY-MM-DD HH:mm:ss.SSS Z}</c> | <level>{extra[level_short]:<5}</level> | <w>{name}:{line}</w>]: <level>{message}</level>"
      colorize: true
      enabled: true
    default.all.file_handler:
      type: FILE
      sink: "{app_name}.all.log"
      enabled: true
    default.err.file_handler:
      type: FILE
      sink: "{app_name}.err.log"
      error: true
      enabled: true
    default.all.json_handler:
      type: FILE
      sink: "json/{app_name}.json.all.log"
      serialize: true
      enabled: true
    default.err.json_handler:
      type: FILE
      sink: "json/{app_name}.json.err.log"
      serialize: true
      error: true
      enabled: true
  extra:
    http_std_debug_format: '<n>[{request_id}]</n> {client_host} {user_id} "<u>{method} {url_path}</u> HTTP/{http_version}"'
    http_std_msg_format: '<n><w>[{request_id}]</w></n> {client_host} {user_id} "<u>{method} {url_path}</u> HTTP/{http_version}" {status_code} {content_length}B {response_time}ms'
    http_file_enabled: true
    http_file_format: '{client_host} {request_id} {user_id} [{datetime}] "{method} {url_path} HTTP/{http_version}" {status_code} {content_length} "{h_referer}" "{h_user_agent}" {response_time}'
    http_file_tz: "localtime"
    http_log_path: "http/{app_name}.http.access.log"
    http_err_path: "http/{app_name}.http.err.log"
    http_json_enabled: true
    http_json_path: "http.json/{app_name}.http.json.access.log"
    http_json_err_path: "http.json/{app_name}.http.json.err.log"
```

### 🌎 Environment Variables

[**`.env.example`**](./.env.example):

```sh
# ENV=LOCAL
# DEBUG=false
# TZ=UTC
```

---

## 🧪 Running Tests

To run tests, run the following command:

```sh
# Install python test dependencies:
pip install .[test]

# Run tests:
python -m pytest -sv -o log_cli=true
# Or use the test script:
./scripts/test.sh -l -v -c
```

## 🏗️ Build Package

To build the python package, run the following command:

```sh
# Install python build dependencies:
pip install -r ./requirements/requirements.build.txt

# Build python package:
python -m build
# Or use the build script:
./scripts/build.sh
```

## 📝 Generate Docs

To build the documentation, run the following command:

```sh
# Install python documentation dependencies:
pip install -r ./requirements/requirements.docs.txt

# Serve documentation locally (for development):
mkdocs serve -a 0.0.0.0:8000
# Or use the docs script:
./scripts/docs.sh

# Or build documentation:
mkdocs build
# Or use the docs script:
./scripts/docs.sh -b
```

## 📚 Documentation

- [Docs](./docs)

---

## 📑 References

- <https://packaging.python.org/en/latest/tutorials/packaging-projects>
- <https://python-packaging.readthedocs.io/en/latest>
