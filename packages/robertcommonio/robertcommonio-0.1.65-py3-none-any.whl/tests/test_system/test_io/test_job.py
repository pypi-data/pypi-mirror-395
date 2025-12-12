from robertcommonbasic.basic.dt.utils import get_datetime_str
from robertcommonio.system.io.job import Job

from apscheduler.triggers.cron import CronTrigger


def print_time():
    print(get_datetime_str())


def get_job():
    return Job(func=print_time, name='print_time', trigger=CronTrigger(second="*/1"))


if __name__ == '__main__':
    get_job().run_once()
