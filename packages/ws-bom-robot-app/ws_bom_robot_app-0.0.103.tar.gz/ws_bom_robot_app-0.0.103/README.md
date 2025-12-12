# 🤖 ws-bom-robot-app

A `FastAPI` application serving ws bom/robot/llm platform ai

## 🌵 Minimal app structure

```env
app/
|-- .env
|-- main.py
```

Fill `main.py` with the following code:

```python
from ws_bom_robot_app import main
app = main.app
```

Create a `.env` file in the root directory with the following configuration:

```properties
# robot configuration
robot_env=development
robot_user=your_username
USER_AGENT=ws-bom-robot-app

# cms (bowl) configuration
robot_cms_host='http://localhost:4000'
robot_cms_auth='users API-Key your-api-key-here'

# llm providers: fill one or more of these with your API keys
DEEPSEEK_API_KEY="your-deepseek-api-key"
OPENAI_API_KEY="your-openai-api-key"
GOOGLE_API_KEY="your-google-api-key"
ANTHROPIC_API_KEY="your-anthropic-api-key"
GROQ_API_KEY="your-groq-api-key"
# ibm
WATSONX_URL="https://eu-gb.ml.cloud.ibm.com"
WATSONX_APIKEY="your-watsonx-api-key"
WATSONX_PROJECTID="your-watsonx-project-id"
# gvertex: ensure to mount the file in docker
GOOGLE_APPLICATION_CREDENTIALS="./.data/secrets/google-credentials.json" 
```

## 🚀 Run the app

- development

  ```bash
  fastapi dev --port 6001
  #uvicorn main:app --app-dir ./ws_bom_robot_app --reload --reload-dir ws_bom_robot_app --host 0.0.0.0 --port 6001 
  #uvicorn main:app --app-dir ./ws_bom_robot_app --host 0.0.0.0 --port 6001 
  ```  

- production

  ```bash  
  uvicorn main:app --host 0.0.0.0 --port 6001  
  ```

- production with [multipler workers](https://fastapi.tiangolo.com/deployment/server-workers/#multiple-workers)

  ```bash
  fastapi run --port 6001 --workers 4
  #uvicorn main:app --host 0.0.0.0 --port 6001 --workers 4
  #gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind
  ```

## 📖 API documentation

- [swagger](http://localhost:6001/docs)
- [redoc](http://localhost:6001/redoc)

---

## 🐳 Docker

dockerize base image

```pwsh
<# cpu #>
docker build -f Dockerfile-robot-base-cpu -t ws-bom-robot-base:cpu .
docker tag ws-bom-robot-base:cpu ghcr.io/websolutespa/ws-bom-robot-base:cpu
docker push ghcr.io/websolutespa/ws-bom-robot-base:cpu
<# gpu #>
docker build -f Dockerfile-robot-base-gpu -t ws-bom-robot-base:gpu .
docker tag ws-bom-robot-base:gpu ghcr.io/websolutespa/ws-bom-robot-base:gpu
docker push ghcr.io/websolutespa/ws-bom-robot-base:gpu
```

dockerize app (from src)

- cpu
```pwsh
docker build -f Dockerfile -t ws-bom-robot-app:cpu --build-arg DEVICE=cpu .
docker run --rm -d --name ws-bom-robot-app --env-file .env -p 6001:6001 ws-bom-robot-app:cpu
```
- gpu
```pwsh
docker build -f Dockerfile -t ws-bom-robot-app:gpu --build-arg DEVICE=gpu .
docker run --rm -d --name ws-bom-robot-app --gpus all --env-file .env -p 6001:6001 ws-bom-robot-app:gpu
```

dockerize app (from latest)

- cpu
```pwsh
docker build -f Dockerfile-pkg -t ws-bom-robot-app-pkg:cpu --build-arg DEVICE=cpu .
docker run --rm -d --name ws-bom-robot-app-pkg --env-file .env -p 6001:6001 ws-bom-robot-app-pkg:cpu
```
- gpu
```pwsh
docker build -f Dockerfile-pkg -t ws-bom-robot-app-pkg:gpu --build-arg DEVICE=gpu .
docker run --rm -d --name ws-bom-robot-app-pkg --gpus all --env-file .env -p 6001:6001 ws-bom-robot-app-pkg:gpu
<# test gpu: nvidia-smi #>
```

docker run mounted to src (dev mode)

```pwsh
docker run --rm  -d --env-file .env -v "$(pwd)/.data:/app/.data" -p 6001:6001 ws-bom-robot-app fastapi dev ./ws_bom_robot_app/main.py --host 0.0.0.0 --port 6001
docker run --rm  -d --env-file .env -v "$(pwd)/.data:/app/.data" -p 6001:6001 ws-bom-robot-app uvicorn ws_bom_robot_app.main:app --reload --host 0.0.0.0 --port 6001
```

---

## 🔖 Windows requirements (for RAG functionality only)

> ⚠️ While it's strongly recommended to use a docker container for development, you can run the app on Windows with the following requirements

### libmagic (mandatory)

  ```bash
  py -m pip install --upgrade python-magic-bin
  ```
  
### tesseract-ocr (mandatory)

  [Install tesseract](https://github.com/UB-Mannheim/tesseract/wiki)
  [Last win-64 release](https://github.com/tesseract-ocr/tesseract/releases/download/5.5.0/tesseract-ocr-w64-setup-5.5.0.20241111.exe)

  Add tesseract executable (C:\Program Files\Tesseract-OCR) to system PATH
  
  ```pwsh
  $pathToAdd = "C:\Program Files\Tesseract-OCR"; `
  $currentPath = [System.Environment]::GetEnvironmentVariable("Path", [System.EnvironmentVariableTarget]::Machine); `
  if ($currentPath -split ';' -notcontains $pathToAdd) { `
    [System.Environment]::SetEnvironmentVariable("Path", "$currentPath;$pathToAdd", [System.EnvironmentVariableTarget]::Machine) `
  }
  ```

### docling

  Set the following environment variables

  ```pwsh
  KMP_DUPLICATE_LIB_OK=TRUE
  ```    

### libreoffice (optional: for robot_env set to development/production)

  [Install libreoffice](https://www.libreoffice.org/download/download-libreoffice/)
  [Last win-64 release](https://download.documentfoundation.org/libreoffice/stable/24.8.2/win/x86_64/LibreOffice_24.8.2_Win_x86-64.msi)

  Add libreoffice executable (C:\Program Files\LibreOffice\program) to system PATH

  ```pwsh
  $pathToAdd = "C:\Program Files\LibreOffice\program"; `
  $currentPath = [System.Environment]::GetEnvironmentVariable("Path", [System.EnvironmentVariableTarget]::Machine); `
  if ($currentPath -split ';' -notcontains $pathToAdd) { `
    [System.Environment]::SetEnvironmentVariable("Path", "$currentPath;$pathToAdd", [System.EnvironmentVariableTarget]::Machine) `
  }
  ```

### poppler (optional: for robot_env set to development/production)

  [Download win poppler release](https://github.com/oschwartz10612/poppler-windows/releases)
  Extract the zip, copy the nested folder "poppler-x.x.x." to a program folder (e.g. C:\Program Files\poppler-24.08.0)
  Add poppler executable (C:\Program Files\poppler-24.08.0\Library\bin) to system PATH

  ```pwsh
  $pathToAdd = "C:\Program Files\poppler-24.08.0\Library\bin"; `
  $currentPath = [System.Environment]::GetEnvironmentVariable("Path", [System.EnvironmentVariableTarget]::Machine); `
  if ($currentPath -split ';' -notcontains $pathToAdd) { `
    [System.Environment]::SetEnvironmentVariable("Path", "$currentPath;$pathToAdd", [System.EnvironmentVariableTarget]::Machine) `
  }
  ```

---

## 👷 Contributors

Build/distribute pkg from `websolutespa` bom [[Github](https://github.com/websolutespa/bom)]

> dir in `robot` project folder

```bash
  cd ./src/robot
```

### 🔖 requirements

- install uv venv package management

```bash
py -m pip install --upgrade uv
# create venv
uv venv
# activate venv
#win: .venv/Scripts/activate
#linux: source .venv/bin/activate
```

- project requirements update

```bash
uv pip install --upgrade -r requirements.txt
```

- build tools

```bash
uv pip install --upgrade setuptools build twine streamlit 
```

### 🪛 build

- clean dist and build package
```pwsh
if (Test-Path ./dist) {rm ./dist -r -force}; `
py -m build && twine check dist/*
```
- linux/mac
```bash
[ -d ./dist ] && rm -rf ./dist
python -m build && twine check dist/*
```

### 📦 test / 🧪 debugger

Install the package in editable project location

```pwsh
uv pip install -U -e .
uv pip show ws-bom-robot-app
```

code quality tools
  
```pwsh
# .\src\robot
!py -m uv pip install -U scanreq prospector[with_everything]
## unused requirements
scanreq -r requirements.txt -p ./ws_bom_robot_app
## style/linting
prospector ./ws_bom_robot_app -t pylint -t pydocstyle
## code quality/complexity
prospector ./ws_bom_robot_app -t vulture -t mccabe -t mypy 
## security
prospector ./ws_bom_robot_app -t dodgy -t bandit
## package
prospector ./ws_bom_robot_app -t pyroma
```

#### 🧪 run tests

```pwsh
!py -m uv pip install -U pytest pytest-asyncio pytest-mock pytest-cov pyclean
# clean cache if needed
# pyclean --verbose .
pytest --cov=ws_bom_robot_app --log-cli-level=info
# directory
# pytest --cov=ws_bom_robot_app.llm.vector_store --log-cli-level=info ./tests/app/llm/vector_store
```

#### 🐞 start debugger

```pwsh
streamlit run debugger.py --server.port 8051
```

### ✈️ publish

- [testpypi](https://test.pypi.org/project/ws-bom-robot-app/)

  ```pwsh
  twine upload --verbose -r testpypi dist/*
  #pip install -i https://test.pypi.org/simple/ -U ws-bom-robot-app 
  ```

- [pypi](https://pypi.org/project/ws-bom-robot-app/)

  ```pwsh
  twine upload --verbose dist/* 

  ```
