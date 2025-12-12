import datetime
from fastapi import FastAPI
from ws_bom_robot_app.util import is_app_subprocess
_uptime = datetime.datetime.now()
app = FastAPI(redoc_url=None,docs_url=None,openapi_url=None)

if not is_app_subprocess():
  import platform
  from fastapi.responses import FileResponse
  import os, sys
  from fastapi import Depends
  from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
  from fastapi.openapi.utils import get_openapi
  from ws_bom_robot_app.auth import authenticate
  from ws_bom_robot_app.config import config
  from ws_bom_robot_app.util import _log
  from ws_bom_robot_app.llm.api import router as llm
  from ws_bom_robot_app.task_manager import router as task
  from ws_bom_robot_app.cron_manager import (
      router as cron,
      cron_manager)
  cron_manager.start()
  app.include_router(llm,dependencies=[Depends(authenticate)])
  app.include_router(task,dependencies=[Depends(authenticate)])
  app.include_router(cron,dependencies=[Depends(authenticate)])

  @app.get("/")
  async def root():
      return health()
  @app.get("/favicon.ico")
  async def favicon():
      return FileResponse("./favicon.ico")

  @app.get("/docs", include_in_schema=False)
  async def get_swagger_documentation(authenticate: bool = Depends(authenticate)):
      return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")
  @app.get("/redoc", include_in_schema=False)
  async def get_redoc_documentation(authenticate: bool = Depends(authenticate)):
      return get_redoc_html(openapi_url="/openapi.json", title="docs")
  @app.get("/openapi.json", include_in_schema=False)
  async def openapi(authenticate: bool = Depends(authenticate)):
      return get_openapi(title=app.title, version=app.version, routes=app.routes)

  @app.get("/api/health",tags=["diag"])
  def health():
      return {"status": "ok"}
  def __get_size(bytes, suffix="B"):
      """
      Scale bytes to its proper format
      e.g:
          1253656 => '1.20MB'
          1253656678 => '1.17GB'
      """
      factor = 1024
      for unit in ["", "K", "M", "G", "T", "P"]:
          if bytes < factor:
              return f"{bytes:.2f}{unit}{suffix}"
          bytes /= factor
  def __get_disk_info():
      import psutil
      partitions = psutil.disk_partitions()
      _disks:list = []
      for partition in partitions:
          device = partition.device
          mountpoint = partition.mountpoint
          fstype = partition.fstype
          try:
              usage = psutil.disk_usage(mountpoint)
          except PermissionError:
              continue
          total = __get_size(usage.total)
          used = __get_size(usage.used)
          free = __get_size(usage.free)
          percent = f"{usage.percent}%"
          _disks.append({"device": device, "mountpoint": mountpoint, "fstype": fstype, "total": total, "used": used, "free": free, "percent": percent})
      return _disks
  @app.get("/api/diag",tags=["diag"])
  def diag(authenticate: bool = Depends(authenticate)):
      import importlib,psutil
      from ws_bom_robot_app.llm.providers.llm_manager import LlmManager as wsllm
      from ws_bom_robot_app.llm.vector_store.db.manager import VectorDbManager as wsdb
      from ws_bom_robot_app.llm.vector_store.loader.base import Loader as wsldr
      from ws_bom_robot_app.llm.vector_store.integration.manager import IntegrationManager as wsim
      from ws_bom_robot_app.llm.tools.tool_manager import ToolManager as wstm
      from ws_bom_robot_app.llm.agent_description import AgentDescriptor as wsad

      svmem = psutil.virtual_memory()
      swap = psutil.swap_memory()
      try:
        ws_bom_robot_app_version = importlib.metadata.version("ws_bom_robot_app")
      except:
        ws_bom_robot_app_version = "unknown"
      peer_process_ids = [c.pid for c in psutil.Process(os.getppid()).children()] if config.runtime_options().is_multi_process else None
      return {
          "status":"ok",
          "uptime": {'from':_uptime,'elapsed':str(datetime.datetime.now()-_uptime)},
          "system": {
              "platform": {
                  "node": platform.node(),
                  "system": platform.system(),
                  "platform": platform.platform(),
                  "version": platform.version(),
                  "type": platform.machine(),
                  "processor": platform.processor(),
                  "architecture": platform.architecture()
              },
              "cpu": {
                  "physical_core": psutil.cpu_count(logical=False),
                  "total_core": psutil.cpu_count(logical=True),
                  "load": f"{psutil.cpu_percent(interval=1)}%"
              },
              "memory": {
                  "total": f"{__get_size(svmem.total)}",
                  "available": f"{__get_size(svmem.available)}",
                  "used": f"{__get_size(svmem.used)}",
                  "free": f"{__get_size(svmem.free)}",
                  "percent": f"{svmem.percent}%"
              },
              "swap": {
                  "total": f"{__get_size(swap.total)}",
                  "used": f"{__get_size(swap.used)}",
                  "free": f"{__get_size(swap.free)}",
                  "percent": f"{swap.percent}%"
              },
              "disk": __get_disk_info(),
              "sys": {
                  "version": sys.version,
                  "platform": sys.platform,
                  "executable": sys.executable,
                  "args": {k: arg for k, arg in enumerate(sys.argv)}
              },
              "os": {
                  "ppid": os.getppid(),
                  "pid": os.getpid(),
                  "pids": peer_process_ids,
                  "cwd": os.getcwd(),
                  "ws_bom_robot_app": ws_bom_robot_app_version,
                  "env": os.environ,
              },
          },
          "config":config,
          "runtime":config.runtime_options(),
          "extension": {
              "provider":({item[0]: type(item[1]).__name__} for item in wsllm._list.items()),
              "db":({item[0]: type(item[1]).__name__} for item in wsdb._list.items()),
              "loader": ({item[0]: item[1].loader.__name__ if item[1] else None} for item in sorted(wsldr._list.items(), key=lambda x: x[0]) if item[1]),
              "integration":({item[0]: type(item[1]).__name__} for item in wsim._list.items()),
              "tool": ({item[0]: item[1].function.__name__} for item in wstm._list.items()),
              "agent":({item[0]: type(item[1]).__name__} for item in wsad._list.items())
              }
          }
  @app.post("/diag/reload",tags=["diag"])
  def reset(authenticate: bool = Depends(authenticate)):
      _log.info("restart server")
      with open(".reloadfile","w") as f:
          f.write("")
