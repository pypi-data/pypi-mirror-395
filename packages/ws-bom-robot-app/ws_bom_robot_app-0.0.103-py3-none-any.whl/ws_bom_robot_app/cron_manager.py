import os
from apscheduler.schedulers.background import BackgroundScheduler
#from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.date import DateTrigger
from fastapi import APIRouter
from datetime import datetime
from ws_bom_robot_app.llm.utils.cleanup import kb_cleanup_data_file, chat_cleanup_attachment, task_cleanup_history
from ws_bom_robot_app.util import _log
from ws_bom_robot_app.config import config

class JobstoreStrategy:
    def get_jobstore(self):
        raise NotImplementedError("Subclasses should implement this method")

class MemoryJobstoreStrategy(JobstoreStrategy):
    def get_jobstore(self):
        _log.info("Using in-memory cron jobstore.")
        return {"default": MemoryJobStore()}

class PersistentJobstoreStrategy(JobstoreStrategy):
    def get_jobstore(self, db_url: str = f"sqlite:///{config.robot_data_folder}/db/jobs.sqlite"):
        _log.info(f"Using persistent cron jobstore with database URL: {db_url}.")
        return {"default": SQLAlchemyJobStore(url=db_url)}

class Job:
    def __init__(self, name: str, job_func, args: list = None, kwargs: dict = None, cron_expression: str = None, interval: int = None, run_at: datetime = None):
        """
        Job class that supports both recurring and one-time jobs.
        :param job_func: The function to execute.
        :param interval: Interval in seconds for recurring jobs.
        :param run_at: Specific datetime for one-time jobs.
        :param tags: Tags associated with the job.
        """
        if not (cron_expression or interval or run_at):
            raise ValueError("Either 'interval' or 'run_at' must be provided.")
        self.name = name
        self.job_func = job_func
        self.args: list = args or []
        self.kwargs: dict = kwargs or {}
        self.cron_expression = cron_expression
        self.interval = interval
        self.run_at = run_at

    def create_trigger(self):
        """Create the appropriate trigger based on the job type."""
        if self.cron_expression:
            return CronTrigger.from_crontab(self.cron_expression)
        if self.interval:
            return IntervalTrigger(seconds=self.interval)
        elif self.run_at:
            return DateTrigger(run_date=self.run_at)

class CronManager:
    _list_default = [
            Job('cleanup-task-history',task_cleanup_history, interval=4 * 60 * 60),
            Job('cleanup-kb-data',kb_cleanup_data_file, interval=8 * 60 * 60),
            Job('cleanup-chat-attachment',chat_cleanup_attachment, interval=6 * 60 * 60),
        ]
    def __get_jobstore_strategy(self) -> JobstoreStrategy:
        if config.robot_cron_strategy == 'memory':
            return MemoryJobstoreStrategy()
        return PersistentJobstoreStrategy()
    def __init__(self, strategy: JobstoreStrategy = None, enable_defaults: bool = True):
        self.enable_defaults = enable_defaults
        if strategy is None:
          strategy = self.__get_jobstore_strategy()
        jobstores = strategy.get_jobstore()
        self.scheduler: BackgroundScheduler = BackgroundScheduler(jobstores=jobstores)
        self.__scheduler_is_running = False

    def add_job(self, job: Job):
        """
        Adds a job to the scheduler with the specified name and job details.
        Args:
          name (str): The unique identifier for the job.
          job (Job): An instance of the Job class containing the job details.
        The job details include:
          - job_func: The function to be executed.
          - args: The positional arguments to pass to the job function.
          - kwargs: The keyword arguments to pass to the job function.
          - trigger: The trigger that determines when the job should be executed.
        The job will replace any existing job with the same name.
        Sample usage:
          recurring_job = Job(name="sample-recurring-job",job_func=example_job, interval=5, tags=tags, args=args, kwargs=kwargs)
          cron_manager.add_job(recurring_job)
          fire_once_job = Job(name="sample-fire-once-job",job_func=example_job, run_at=datetime.now(), tags=tags, args=args, kwargs=kwargs)
          cron_manager.add_job(fire_once_job)
        """
        existing_job = self.scheduler.get_job(job.name)
        if existing_job:
            _log.info(f"Job with name '{job.name}' already exists. Skip creation.")
        else:
          trigger = job.create_trigger()
          self.scheduler.add_job(
              func=job.job_func,
              args=job.args,
              kwargs=job.kwargs,
              trigger=trigger,
              id=job.name,
              name=job.name,
              replace_existing=True
          )

    def start(self):
        if not self.__scheduler_is_running:
            self.__scheduler_is_running = True
            self.scheduler.start()
            if self.enable_defaults and CronManager._list_default:
                for job in CronManager._list_default:
                    existing_job = self.scheduler.get_job(job.name)
                    if existing_job is None:
                        self.add_job(job)


    def get_job(self, job_id: str):
        return self.scheduler.get_job(job_id)

    def get_jobs(self):
        return self.scheduler.get_jobs()

    def execute_job(self, job_id: str):
        job = self.scheduler.get_job(job_id)
        if job:
            job.func()
        else:
            raise ValueError(f"Job with id '{job_id}' not found.")

    def pause_job(self, job_id: str):
        self.scheduler.pause_job(job_id)

    def resume_job(self, job_id: str):
        self.scheduler.resume_job(job_id)

    def remove_job(self, job_id: str):
        self.scheduler.remove_job(job_id)

    def execute_recurring_jobs(self):
        for job in self.scheduler.get_jobs():
            if job.trigger.interval:
                job.func()

    def pause_recurring_jobs(self):
        for job in self.scheduler.get_jobs():
            if job.trigger.interval:
                self.pause_job(job.id)

    def resume_recurring_jobs(self):
        for job in self.scheduler.get_jobs():
            if job.trigger.interval:
                self.resume_job(job.id)

    def remove_recurring_jobs(self):
        for job in self.scheduler.get_jobs():
            if job.trigger.interval:
                self.remove_job(job.id)

    def clear(self):
        self.__scheduler_is_running = False
        self.scheduler.remove_all_jobs()

    def shutdown(self):
        self.scheduler.shutdown()

cron_manager = CronManager()

# FastAPI Routes
router = APIRouter(prefix="/api/cron", tags=["cron"])

@router.get("/list")
def _list():
    def __format(job):
        return {
            "id": job.id,
            "name": job.name,
            "func": job.func_ref,
            "pending": job.pending,
            "trigger": str(job.trigger),
            "next_run_time": job.next_run_time
        }
    return [__format(job) for job in cron_manager.get_jobs()]

@router.get("/default-jobs")
def _default_jobs():
    def __format(job):
        existing_job = cron_manager.scheduler.get_job(job.name)
        return {
            "name": job.name,
            "status": "exists" if existing_job else "not added"
        }
    return [__format(job) for job in CronManager._list_default]

@router.post("/execute-job/{job_id}")
def _execute_job(job_id: str):
    try:
        cron_manager.execute_job(job_id)
        return {"status": f"Job {job_id} executed"}
    except ValueError as e:
        return {"error": str(e)}

@router.post("/pause-job/{job_id}")
def _pause_job(job_id: str):
    cron_manager.pause_job(job_id)
    return {"status": f"Job {job_id} paused"}

@router.post("/resume-job/{job_id}")
def _resume_job(job_id: str):
    cron_manager.resume_job(job_id)
    return {"status": f"Job {job_id} resumed"}

@router.delete("/remove-job/{job_id}")
def _remove_job(job_id: str):
    cron_manager.remove_job(job_id)
    return {"status": f"Job {job_id} removed"}

@router.post("/execute-recurring")
def _execute_recurring():
    cron_manager.execute_recurring_jobs()
    return {"status": "All recurring jobs executed"}

@router.post("/pause-recurring")
def _pause_recurring():
    cron_manager.pause_recurring_jobs()
    return {"status": "All recurring jobs paused"}

@router.post("/resume-recurring")
def _resume_recurring():
    cron_manager.resume_recurring_jobs()
    return {"status": "All recurring jobs resumed"}

@router.delete("/remove-recurring")
def _remove_recurring():
    cron_manager.remove_recurring_jobs()
    return {"status": "All recurring jobs removed"}

@router.get("/start")
def _start():
    cron_manager.start()
    return {"status": "started"}

@router.delete("/stop")
def _stop():
    cron_manager.clear()
    return {"status": "stopped"}

@router.get("/shutdown")
def _shutdown():
    cron_manager.shutdown()
    return {"status": "shutdown"}
