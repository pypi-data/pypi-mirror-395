from collections import deque
import inspect
from math import floor
import asyncio, os, traceback
from datetime import datetime, timedelta
from enum import Enum
from typing import Annotated, Coroutine, Literal, TypeVar, Optional, Dict, Union, Any, Callable
from pydantic import BaseModel, ConfigDict, Field, computed_field
from uuid import uuid4
from fastapi import APIRouter, HTTPException
from ws_bom_robot_app.config import config
from ws_bom_robot_app.llm.models.base import IdentifiableEntity
from ws_bom_robot_app.llm.utils.webhooks import WebhookNotifier
from ws_bom_robot_app.util import _log
from sqlalchemy import create_engine, Column, String, JSON, DateTime, Enum
from sqlalchemy.orm import sessionmaker, registry
from abc import ABC, abstractmethod
from ws_bom_robot_app.subprocess_runner import _start_subprocess_for_coroutine, _recv_from_connection_async, _pickler
from ws_bom_robot_app.config import config

T = TypeVar('T')

#region models
class TaskHeader(BaseModel):
    """
    TaskHeader model representing the header information for a task.
    Example:
    ```bash
    curl -X POST "http://localhost:6001/api/llm/kb/task"
      -H  "x-ws-bom-msg-id: 1234"
      -H  "x-ws-bom-msg-type: generate.knowledgebase"
      -H  "x-ws-bom-msg-extra: key1=value1,key2=value2"
      -H  "x-ws-bom-webhooks: http://localhost:8000/api/webhook"
      -d "{\"api_key\":\"string\"}"
    ```
    Attributes:
      x_ws_bom_msg_id (Optional[str]): The message ID for the task. If not provided, a UUID will be generated.
      x_ws_bom_msg_type (Optional[str]): The message type for the task, e.g. "send.email" or "generate.knowledgebase".
      x_ws_bom_msg_extra (Optional[str]): Any extra information for the task, in comma separated key=value pairs. e.g. "key1=value1,key2=value2".
      x_ws_bom_webhooks (Optional[str]): Webhooks associated with the task, called when the task is completed or failed.
    """
    x_ws_bom_msg_id: Optional[str] = None
    x_ws_bom_msg_type: Optional[str] = None
    x_ws_bom_msg_extra: Optional[str] = None
    x_ws_bom_webhooks: Optional[str] = None
    model_config = ConfigDict(
        extra='allow'
    )

class TaskMetaData(BaseModel):
    created_at: str
    start_at: Optional[str] = None
    end_at: Optional[str] = None
    @computed_field
    @property
    def elapsed_time(self) -> Union[str, None]:
        return str(
            (datetime.now() if not self.end_at else datetime.fromisoformat(self.end_at))
            - datetime.fromisoformat(self.created_at if not self.start_at else self.start_at)
            )
    source: Optional[str] = None
    pid: Optional[int] = None
    pid_child: Optional[int] = None
    extra: Optional[dict[str,Union[str,int,bool]]] = None

class TaskStatus(IdentifiableEntity):
    type: Optional[str] = None
    status: Literal["pending", "completed", "failure"]
    result: Optional[T] = None
    metadata: TaskMetaData = None
    error: Optional[str] = None
    retry: int = 0
    model_config = ConfigDict(
        arbitrary_types_allowed=True
    )

class TaskEntry(IdentifiableEntity):
    task: Annotated[Union[asyncio.Task, Callable], Field(default=None, validate_default=False)] = None
    coroutine: Any = None
    headers: TaskHeader | None = None
    status: Union[TaskStatus, None] = None
    queue: Literal["slow", "fast"] | None = "slow"
    def _get_coroutine_name(self, func: Any) -> str:
        if inspect.iscoroutine(func):
            return func.cr_code.co_name
        return func.__qualname__ if callable(func) else str(func)
    def __init__(self, **data):
        def _metadata_extra(data: str) -> dict[str,str] | None:
            if data:
                _values = data.split(",")
                if _values:
                    try:
                        return {k: v for k,v in [val.split("=") for val in _values]}
                    except Exception as e:
                        return None
            return None
        #separate task from data to handle asyncio.Task
        task = data.pop('task',None)
        super().__init__(**data)
        #bypass pydantic validation
        object.__setattr__(self, 'task', task)
        #init status
        if not self.status:
          self.status = TaskStatus(
              id=self.id,
              type=self.headers.x_ws_bom_msg_type if self.headers and self.headers.x_ws_bom_msg_type else self._get_coroutine_name(self.coroutine) if self.coroutine else None,
              status="pending",
              metadata=TaskMetaData(
                 created_at=str(datetime.now().isoformat()),
                 source=self._get_coroutine_name(self.coroutine) if self.coroutine else None,
                 pid=os.getpid(),
                 extra=_metadata_extra(self.headers.x_ws_bom_msg_extra) if self.headers and self.headers.x_ws_bom_msg_extra else None
                 )
              )
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        validate_assignment=True
    )

class TaskStatistics(BaseModel):
    class TaskStatisticExecutionInfo(BaseModel):
        retention_days: float = config.robot_task_retention_days
        max_parallelism: int
        slot_available: dict[str,int]
        pid: int = os.getpid()
        running: list[TaskStatus]
        slowest: list
    class TaskStatisticExecutionTime(BaseModel):
        min: str
        max: str
        avg: str
    total: int
    pending: int
    completed: int
    failure: int
    exec_time: TaskStatisticExecutionTime
    exec_info: TaskStatisticExecutionInfo

#endregion

#region interface
class TaskManagerStrategy(ABC):
    def __init__(self, max_concurrent_tasks: Optional[int] = None):
        if max_concurrent_tasks is None:
            workers = config.runtime_options().number_of_workers
            max_concurrent_tasks = max(1, floor(config.robot_task_max_total_parallelism / max(1, workers)))
        self.max_parallelism = max_concurrent_tasks
        self.semaphore = {"slow": asyncio.Semaphore(max_concurrent_tasks), "fast": asyncio.Semaphore(max_concurrent_tasks*2)}
        self.running_tasks = dict[str, TaskEntry]()
        self.loop = asyncio.get_event_loop()

    @abstractmethod
    def create_task(self, coroutine, headers: TaskHeader | None = None, queue: Literal["slow", "fast"] | None = "slow") -> IdentifiableEntity:
        """Create a new task.
        Args:
            coroutine (_type_): coroutine or callable to be executed.
            headers (TaskHeader | None, optional): for api call, http headers to include with the task. Defaults to None.
        Returns:
            IdentifiableEntity: The created task id.
        Usage:
            from ws_bom_robot_app.task_manager import task_manager
            task_manager.create_task(my_coroutine, headers=my_headers) -> coroutine executed in-process
            task_manager.create_task(lambda: my_coroutine, headers=my_headers) -> callable using subprocess
            task_manager.create_task(lambda: my_coroutine, headers=my_headers, queue="fast") -> callable using subprocess with "fast" queue
        """
        pass

    @abstractmethod
    def update_task_status(self, task: TaskEntry) -> None:
        """Hook for additional behavior, such as persisting the task status."""
        pass

    @abstractmethod
    def get_task(self, id: str) -> TaskStatus | None:
        pass

    @abstractmethod
    def get_tasks(self) -> list[TaskStatus]:
        pass

    @abstractmethod
    def remove_task(self, id: str) -> None:
        pass

    @abstractmethod
    def cleanup_task(self) -> None:
        pass

    @abstractmethod
    def stats(self) -> TaskStatistics:
        pass

    def task_cleanup_rule(self, task: TaskEntry) -> bool:
        return task.status.metadata.start_at and datetime.fromisoformat(task.status.metadata.start_at) < datetime.now() - timedelta(days=config.robot_task_retention_days)

    def _update_task_by_event(self, task_entry: TaskEntry, status: str, output: Any) -> None:
        if status == "completed":
          task_entry.status.status = "completed"
          task_entry.status.result = output
        elif status == "failure":
          task_entry.status.status = "failure"
          task_entry.status.error = str(output)
          _log.error(f"Task {task_entry.id} failed with error: {output}")
        else:
          task_entry.status.metadata.end_at = str(datetime.now().isoformat())
          #strategy-specific behavior
          self.update_task_status(task_entry)
          #remove from running tasks
          if task_entry.id in self.running_tasks:
              del self.running_tasks[task_entry.id]
          #notify webhooks: a task has completed or failed, if failed with retry policy the task remains in pending state, and will not be notified until complete/failure
          if task_entry.status.status in ["completed","failure"]:
            if task_entry.headers and task_entry.headers.x_ws_bom_webhooks:
              try:
                  asyncio.create_task(
                      WebhookNotifier().notify_webhook(task_entry.status, task_entry.headers.x_ws_bom_webhooks)
                  )
              except Exception as e:
                  _log.error(f"Failed to schedule webhook notification for task {task_entry.id}: {e}")

    def task_done_callback(self, task_entry: TaskEntry) -> Callable:
        def callback(task: asyncio.Task, context: Any | None = None):
            try:
                result = task.result()
                self._update_task_by_event(task_entry, "completed", result)
            except Exception as e:
                self._update_task_by_event(task_entry, "failure", e)
            finally:
                self._update_task_by_event(task_entry, "callback", None)
        return callback

    def create_task_entry(self, coroutine_or_callable: Any, headers: TaskHeader | None = None, queue: Literal["slow", "fast"] | None = "slow") -> TaskEntry:
        """Create a new task entry.

        Args:
            coroutine_or_callable (Any): The coroutine or callable to be executed.
            headers (TaskHeader | None, optional): Headers to include with the task. Defaults to None.
        Raises:
            TypeError: If the input is not a coroutine or callable.
        Returns:
            TaskEntry: The created task entry.
        """
        _id = headers and headers.x_ws_bom_msg_id or str(uuid4())
        # Detect coroutine object
        if inspect.iscoroutine(coroutine_or_callable):
            can_use_subprocess = False
        elif callable(coroutine_or_callable):
            can_use_subprocess = True
        else:
            raise TypeError(
                f"Expected coroutine object or callable, got {type(coroutine_or_callable)}"
            )
        task_entry = TaskEntry(
            id=_id,
            coroutine=coroutine_or_callable,
            headers=headers,
            queue=queue
        )
        # Store hint for subprocess capability
        task_entry.status.metadata.extra = task_entry.status.metadata.extra or {}
        task_entry.status.metadata.extra["can_use_subprocess"] = can_use_subprocess
        try:
          asyncio.create_task(self._run_task_with_semaphore(task_entry)) # run the task
        except Exception as e:
          _log.error(f"Error occurred while creating task {task_entry.id}: {e}")
        return task_entry

    async def _run_task_with_semaphore(self, task_entry: TaskEntry):
        """Run a task with semaphore control to limit concurrency."""
        async with self.semaphore[task_entry.queue]:
          await self._execute_task(task_entry)

    async def _monitor_subprocess(self, task_entry: TaskEntry, proc, conn):
        try:
            # Wait for the worker to send bytes (this blocks, so run via executor wrapper)
            data_bytes = await _recv_from_connection_async(conn)
            # unpickle bytes to get payload
            try:
                payload = _pickler.loads(data_bytes)
            except Exception:
                # fallback if pickler fails
                payload = ("err", {"error": "Failed to unpickle subprocess result"})
            if isinstance(payload, tuple) and payload[0] == "ok":
                result = payload[1]
                # write results into task_entry
                self._update_task_by_event(task_entry, "completed", result)
            else:
                # error
                err_info = payload[1]["error"] if isinstance(payload, tuple) else str(payload)
                self._update_task_by_event(task_entry, "failure", err_info) # give up, no retry
        except Exception:
            # maybe subprocess is no more alive / killed due to memory pressure
            if task_entry.status.retry < config.robot_task_mp_max_retries:
                task_entry.status.retry += 1
                _log.warning(f"Task {task_entry.id} failure, retrying {task_entry.status.retry}...")
                async def delayed_retry():
                    _delay = config.robot_task_mp_retry_delay # help to backpressure when overloaded
                    if self.semaphore[task_entry.queue]._value > 0:  # free semaphore slots available
                        _delay = 5  # small/no delay if retry can run immediately
                    await asyncio.sleep(_delay)  # delay in seconds
                    await self._run_task_with_semaphore(task_entry)
                asyncio.create_task(delayed_retry())
                # semaphore is released, so new task can be executed
                return
            else:
                self._update_task_by_event(task_entry, "failure", "subprocess monitor error: failed to receive data from connection")
        finally:
            # ensure process termination / cleanup
            try:
                conn.close()
            except Exception:
                pass
            try:
              if proc.is_alive():
                  proc.terminate()
              proc.join(timeout=1)
            except Exception:
                pass
            # callback
            self._update_task_by_event(task_entry, "callback", None)

    async def _execute_task(self, task_entry: TaskEntry):
        """
        Execute the task. Try to run it inside a subprocess (if serializable).
        If subprocess is used, we create a monitor asyncio.Task that waits for the subprocess result
        and then calls the same task_done_callback to finalize and persist state.
        If subprocess cannot be used, fall back to in-process behavior.
        """
        self.running_tasks[task_entry.id]=task_entry
        task_entry.status.metadata.start_at = str(datetime.now().isoformat())
        # try to spawn subprocess (non-blocking)
        can_use_subprocess = task_entry.status.metadata.extra.get("can_use_subprocess", False)
        if config.robot_task_mp_enable and can_use_subprocess:
            proc, conn, used_subprocess = _start_subprocess_for_coroutine(task_entry.coroutine)
            if used_subprocess and proc is not None and conn is not None:
                # monitor subprocess asynchronously
                task_entry.status.status = "pending"
                task_entry.status.metadata.pid_child = proc.pid
                _log.info(f"Task {task_entry.id} started in subprocess (pid={proc.pid})")
                # await monitor process, then return: important to acquire semaphore
                await self._monitor_subprocess(task_entry, proc, conn)
                return
        # default fallback (in-process)
        try:
            async def _callable_to_coroutine(func: Any) -> Any:
                if callable(func) and not inspect.iscoroutine(func):
                    result = func()
                    if inspect.iscoroutine(result):
                        return await result
                    return result
                elif inspect.iscoroutine(func):
                    return await func
                return func
            task_entry.task = asyncio.create_task(_callable_to_coroutine(task_entry.coroutine))
            task_entry.task.add_done_callback(self.task_done_callback(task_entry))
            _log.info(f"Starting task {task_entry.id} in-process with coroutine {task_entry._get_coroutine_name(task_entry.coroutine)}")
            await task_entry.task
        except Exception as e:
            _error = f"Error occurred while executing task {task_entry.id}: {e}"
            _log.error(_error)
            self._update_task_by_event(task_entry, "failure", _error)
            self._update_task_by_event(task_entry, "callback", None)

    def running_task(self):
        return self.running_tasks.values()
    def stats(self) -> TaskStatistics:
        def __string_to_timedelta(value: str) -> timedelta:
            if "." in value:
                time_format = "%H:%M:%S.%f"
            else:
                time_format = "%H:%M:%S"
            time_obj = datetime.strptime(value, time_format)
            return timedelta(hours=time_obj.hour, minutes=time_obj.minute, seconds=time_obj.second, microseconds=time_obj.microsecond)
        def __timedelta_to_string(td):
            hours, remainder = divmod(td.total_seconds(), 3600)
            minutes, seconds = divmod(remainder, 60)
            return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}.{td.microseconds}"
        _all = self.get_tasks()
        _not_pending = _all and [task for task in _all if task.status != "pending"] or []
        _total_not_pending = _not_pending and len(_not_pending) if _not_pending else 0
        elapsed_times = _not_pending and [__string_to_timedelta(task.metadata.elapsed_time) for task in _not_pending]
        _avg_exec_time = sum(elapsed_times, timedelta()) / _total_not_pending if elapsed_times and _total_not_pending > 0 else timedelta()
        _min_exec_time = min(elapsed_times) if elapsed_times and _total_not_pending > 0 else timedelta()
        _max_exec_time = max(elapsed_times) if elapsed_times and _total_not_pending > 0 else timedelta()
        _slowest: list[TaskStatus] = _not_pending and sorted(_not_pending, key=lambda x: __string_to_timedelta(x.metadata.elapsed_time), reverse=True)[:3]
        return TaskStatistics(
            total= _all and len(_all) or 0,
            pending=_all and len([task for task in _all if task.status == "pending"]) or 0,
            completed=_all and len([task for task in _all if task.status == "completed"]) or 0,
            failure=_all and len([task for task in _all if task.status == "failure"]) or 0,
            exec_time=TaskStatistics.TaskStatisticExecutionTime(
                min=__timedelta_to_string(_min_exec_time),
                max=__timedelta_to_string(_max_exec_time),
                avg=__timedelta_to_string(_avg_exec_time)
            ),
            exec_info=TaskStatistics.TaskStatisticExecutionInfo(
                retention_days=config.robot_task_retention_days,
                max_parallelism=self.max_parallelism,
                slot_available={queue: self.semaphore[queue]._value for queue in self.semaphore},
                running=[task.status for task in self.running_task()],
                slowest=_slowest
            )
        )

#endregion

#region memory implementation
class MemoryTaskManagerStrategy(TaskManagerStrategy):
    def __init__(self, max_concurrent_tasks: Optional[int] = None):
        super().__init__(max_concurrent_tasks)
        self.tasks: Dict[str, TaskEntry] = {}

    def create_task(self, coroutine: Any, headers: TaskHeader | None = None, queue: Literal["slow", "fast"] | None = "slow") -> IdentifiableEntity:
        task = self.create_task_entry(coroutine, headers, queue)
        self.tasks[task.id] = task
        return IdentifiableEntity(id=task.id)

    def update_task_status(self, task: TaskEntry) -> None:
        """no-op for memory strategy."""
        pass

    def get_task(self, id: str) -> TaskStatus | None:
        if _task := self.tasks.get(id):
            return _task.status
        return None

    def get_tasks(self) -> list[TaskStatus] | None:
        return [task.status for task in self.tasks.values()]

    def remove_task(self, id: str) -> None:
        if id in self.tasks:
            del self.tasks[id]

    def cleanup_task(self):
        keys = [task.id for task in self.tasks.values() if self.task_cleanup_rule(task)]
        for key in keys:
            self.remove_task(key)

#endregion

#region db implementation
Base = registry().generate_base()
class TaskEntryModel(Base):
    __tablename__ = "entry"
    id = Column(String, primary_key=True)
    status = Column(JSON)
    model_config = ConfigDict(
        arbitrary_types_allowed=True
    )
class DatabaseTaskManagerStrategy(TaskManagerStrategy):
    def __init__(self, db_url: str = f"sqlite:///{config.robot_data_folder}/db/tasks.sqlite", max_concurrent_tasks: Optional[int] = None):
        super().__init__(max_concurrent_tasks)
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)

    def create_task(self, coroutine: asyncio.coroutines, headers: TaskHeader | None = None) -> IdentifiableEntity:
        task = self.create_task_entry(coroutine, headers)
        with self.Session() as session:
            session.add(TaskEntryModel(id=task.id, status=task.status.model_dump()))
            session.commit()
        return IdentifiableEntity(id=task.id)

    def update_task_status(self, task: TaskEntry) -> None:
        with self.Session() as session:
          session.query(TaskEntryModel).filter_by(id=task.id).update(
              {"status": task.status.model_dump()}
          )
          session.commit()

    def get_task(self, id: str) -> TaskStatus | None:
        with self.Session() as session:
            task = session.query(TaskEntryModel).filter_by(id=id).first()
            if task:
                return TaskEntry(**task.__dict__).status
        return None

    def get_tasks(self) -> list[TaskStatus]:
        with self.Session() as session:
            tasks = session.query(TaskEntryModel).all()
            if tasks:
                return [TaskEntry(**task.__dict__).status for task in tasks]
        return []

    def remove_task(self, id: str) -> None:
        with self.Session() as session:
            session.query(TaskEntryModel).filter_by(id=id).delete()
            session.commit()

    def cleanup_task(self):
        with self.Session() as session:
            for task in session.query(TaskEntryModel).all():
                _task = TaskEntry(**task.__dict__)
                if self.task_cleanup_rule(_task):
                    session.query(TaskEntryModel).filter_by(id=task.id).delete()
            session.commit()
#endregion

#region global
def __get_taskmanager_strategy() -> TaskManagerStrategy:
    """ Factory function to get the appropriate task manager strategy based on the runtime configuration."""
    if config.robot_task_strategy == 'memory':
        return MemoryTaskManagerStrategy()
    return DatabaseTaskManagerStrategy()
task_manager = __get_taskmanager_strategy()
_log.info(f"Task manager strategy: {task_manager.__class__.__name__}")

def task_cleanup():
    _log.info("Cleaning up tasks...")
    task_manager.cleanup_task()
    _log.info("Task cleanup complete.")
#endregion

#region api
router = APIRouter(prefix="/api/task", tags=["task"])

@router.get("/status/{id}")
async def _status_task(id: str) -> TaskStatus:
    task_status = task_manager.get_task(id)
    if not task_status:
        raise HTTPException(status_code=404, detail="Task not found")
    return task_status

@router.get("/status")
async def _status_task_list() -> list[TaskStatus]:
    return task_manager.get_tasks()

@router.delete("/status/{id}")
async def _remove_task(id: str):
   task_manager.remove_task(id)
   return {"success":"ok"}

@router.delete("/cleanup")
async def _remove_task_list():
    task_manager.cleanup_task()
    return {"success":"ok"}

@router.get("/stats")
async def _stats() -> TaskStatistics:
    return task_manager.stats()

#endregion
