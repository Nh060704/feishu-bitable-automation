"""
定时任务模块
"""
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TaskScheduler:
    def __init__(self):
        self.scheduler = BlockingScheduler()

    def add_sync_job(self, func, interval_seconds: int):
        """添加定时同步任务"""
        self.scheduler.add_job(
            func,
            "interval",
            seconds=interval_seconds,
            next_run_time=datetime.now(),
            id="sync_job"
        )
        logger.info(f"已添加定时任务，每 {interval_seconds} 秒执行一次")

    def start(self):
        """启动调度器"""
        logger.info("定时任务启动")
        try:
            self.scheduler.start()
        except (KeyboardInterrupt, SystemExit):
            logger.info("定时任务停止")


if __name__ == "__main__":
    def test_job():
        print(f"测试任务执行: {datetime.now()}")

    sched = TaskScheduler()
    sched.add_sync_job(test_job, 10)
    sched.start()
