
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import time
# 计时器


async def perform_startup_tasks():
    """ 1 """
    print("Performing startup tasks...")
    scheduler.start()
    print("APScheduler 启动")

async def perform_shutdown_tasks():
    """ 1 """
    print("Performing shutdown tasks...")
    scheduler.shutdown()
    print("APScheduler 关闭")


def task_daily_midnight():
    """
    每天凌晨 0:00 执行的任务
    """
    print(f"任务：每天凌晨 0:00 执行。当前时间：{time.ctime()}")

def task_weekday_3am():
    """
    工作日 3:00 执行的任务
    """
    print(f"任务：工作日 3:00 执行。当前时间：{time.ctime()}")

def task_weekday_850am():
    """
    工作日 8:50 执行的任务
    """
    print(f"任务：工作日 9:30 执行。当前时间：{time.ctime()}")

def task_weekday_6pm():
    """
    工作日 18:00 执行的任务
    """
    print(f"任务：工作日 18:00 执行。当前时间：{time.ctime()}")

def task_weekday_7pm():
    """
    工作日 19:00 执行的任务
    """
    print(f"任务：工作日 19:00 执行。当前时间：{time.ctime()}")

def task_weekend_8am():
    """
    休息日 5:00 执行的任务
    """
    print(f"任务：休息日 5:00 执行。当前时间：{time.ctime()}")

scheduler = BackgroundScheduler()
# TODO 修改自动日程执行
# 每天的凌晨 0:00
scheduler.add_job(task_daily_midnight, CronTrigger(hour=0, minute=0))

# 每日 的 3:00
scheduler.add_job(task_weekday_3am, CronTrigger(hour=3, minute=0, 
                                                # day_of_week='mon-fri'
                                                ))

# 工作日 (周一到周五) 的 8:50
scheduler.add_job(task_weekday_850am, CronTrigger(hour=8, minute=50, day_of_week='mon-fri'))

# 工作日 (周一到周五) 的 18:00
scheduler.add_job(task_weekday_6pm, CronTrigger(hour=18, minute=0, day_of_week='mon-fri'))

# 每日 的 19:00
scheduler.add_job(task_weekday_7pm, CronTrigger(hour=19, minute=0, 
                                                # day_of_week='mon-fri'
                                                ))

# 休息日 (周六和周日) 的 8:00
scheduler.add_job(task_weekend_8am, CronTrigger(hour=8, minute=0, day_of_week='sat,sun'))
