import abc
from datetime import datetime, timedelta
from typing import Callable, Dict, Sequence, Tuple, List, Optional
from threading import RLock, currentThread

from robertcommonbasic.basic.data.utils import generate_object_id
from apscheduler.triggers.base import BaseTrigger
from apscheduler.schedulers.base import BaseScheduler
from apscheduler.schedulers.blocking import BlockingScheduler


class JobInfo():

    def __init__(self, name: str, heart_beat_interval: int) -> None:
        self.thread_id = currentThread().ident
        self.heart_beat_interval = heart_beat_interval
        self.name = name
        self.update_time = datetime.now()
        self.start_time = datetime.now()

    def __str__(self) -> str:
        return f'name: {self.name}, heartbeat: {self.heart_beat_interval}, update_time: {self.update_time.strftime("%Y-%m-%d %H:%M:%S")}'


class JobTracker(object):

    __all_jobs: Dict[str, JobInfo] = {}
    __runtime_lock = RLock()

    @classmethod
    def on_job_start(cls, job_id: str, heart_beat_interval: int = 30, name: str = None):
        """启动"""
        with cls.__runtime_lock:
            cls.__all_jobs[job_id] = JobInfo(name, heart_beat_interval)

    @classmethod
    def on_job_update(cls, job_id):
        """更新"""
        with cls.__runtime_lock:
            job = cls.__all_jobs.get(job_id)
            if job:
                job.update_time = datetime.now()

    @classmethod
    def on_job_complete(cls, job_id: str):
        """结束"""
        with cls.__runtime_lock:
            cls.__all_jobs.pop(job_id, None)

    @classmethod
    def check_jobs(cls) -> Tuple[Sequence[JobInfo], Sequence[JobInfo]]:
        """检查任务"""
        timeout_jobs = []
        running_jobs = []
        with cls.__runtime_lock:
            for job_info in JobTracker.__all_jobs.values():
                update_time = job_info.update_time
                heart_beat_interval = job_info.heart_beat_interval

                elapsed = 0
                if update_time and heart_beat_interval:
                    elapsed = (datetime.now() - update_time).total_seconds()
                if elapsed > heart_beat_interval * 2:
                    timeout_jobs.append(job_info)
                else:
                    running_jobs.append(job_info)
        return timeout_jobs, running_jobs


class BaseJob(abc.ABC):

    def __init__(self, name: str, trigger: BaseTrigger, enabled: bool = True, heartbeat: int = 150) -> None:
        super().__init__()
        self.name = name
        self.trigger = trigger
        self.heartbeat = heartbeat
        self.enabled = enabled
        self._breath_time = None
        self.job_id = generate_object_id()

    def run_once(self):
        JobTracker.on_job_start(self.job_id, self.heartbeat, name=self.name)
        self._breath_time = datetime.now()
        try:
            if self.enabled:
                self.job_func()
        except Exception as e:
            raise Exception(f"Job failed: {str(e)}")
        finally:
            JobTracker.on_job_complete(self.job_id)

    def _breath(self, min_interval: float = 0):
        min_interval = min_interval or (self.heartbeat / 10.0)
        next_breath_time = self._breath_time + timedelta(seconds=min_interval)
        now_time = datetime.now()
        if now_time > next_breath_time:
            JobTracker.on_job_update(self.job_id)
            self._breath_time = now_time

    @abc.abstractmethod
    def job_func(self):
        """主函数"""
        pass


class Job(BaseJob):

    def __init__(self, func: Callable, name: str, trigger: BaseTrigger, enabled: bool = True, heartbeat: int = 300) -> None:
        super().__init__(name, trigger, enabled, heartbeat)
        self._job_func = func

    def job_func(self):
        self._job_func()


class ScheduleJobs:

    def __init__(self, jobs: List[Job], scheduler: Optional[BaseScheduler] = None):
        self.scheduler = scheduler if scheduler else BlockingScheduler(misfire_grace_time=30)
        self.jobs = jobs

    def run(self):
        for job in self.jobs:
            self.scheduler.add_job(func=job.run_once, id=job.name, name=job.name, trigger=job.trigger, max_instances=2)
        self.scheduler.start()
