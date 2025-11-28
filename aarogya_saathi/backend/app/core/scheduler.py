from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.services.twilio_service import TwilioService
from app.core.config import settings
import datetime

scheduler = AsyncIOScheduler()
twilio_service = TwilioService()


async def morning_health_check():
    """
    The actual job that runs every morning.
    It pulls patients from the DB (simulated here) and calls them.
    """
    target_phone = settings.NEIGHBOR_PHONE_NUMBER

    print(f"SCHEDULER: Triggering Check-in for {target_phone}...")

    twilio_service.make_call(target_phone)


def start_scheduler():
    run_date = datetime.datetime.now() + datetime.timedelta(seconds=20)
    scheduler.add_job(morning_health_check, "date", run_date=run_date)

    # scheduler.add_job(morning_health_check, 'cron', hour=9, minute=0)

    scheduler.start()
    print("Autonomous Scheduler Started")
