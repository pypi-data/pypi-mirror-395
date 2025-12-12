import logging

from apscheduler.schedulers.blocking import BlockingScheduler


from aiq.churn.analytics.file_dataloader import FileDataLoader
from aiq.churn.analytics.subscriberprofile_loader import SubscriberProfileLoader
from aiq.churn.utils.logging_config import setup_logging

config = {
    "aiq_analytics": {
        "jobs": [
            {
                "name": "file_dataloader",
                "active": True,
                "cron": {"minutes": "*", "hours": "*"}
            },
            {
                "name": "subscriber_profile_loader",
                "active": True,
                "cron": {"minutes": "*", "hours": "*"}
            },
            {
                "name": "subscriber_profile_update_churned",
                "active": True,
                "cron": {"minutes": "*", "hours": "*"}
            }
        ],
        "mysql": {
            "host": "localhost",
            "user": "root",
            "password": "root",
            "database": "dataloader",
            "charset": "utf8",
            "pool_name": "dataloaderpool",
            "pool_size": 5
        },
        "opensearch": {
            "host": "10.150.1.22",
            "port": 19200,
            "user": "admin",
            "password": "ev0lv1ng@dm1n",
            "index": "aiq_subscriberprofile",
            "batch_size": 1000
        },
        "dirs": {
            "file_dir": r"D:\working\evol-aiq\data-in",
            "processed_dir": r"D:\working\evol-aiq\data-out"
        }
    }
}


class AIQAnalyticsJobScheduler:
    logger = logging.getLogger(__name__)
    file_dataloader: FileDataLoader = None
    subscription_profile_loader: SubscriberProfileLoader = None
    scheduler: BlockingScheduler = None
    aiq_analytics_config: dict

    def __init__(self, config: dict):

        # 1. Load Configuration
        self.config = config

        log_config = self.config['logging']['aiq_analytics']
        setup_logging(
            log_file=log_config.get('log_file'),
            log_level=log_config.get('log_level'),
            max_bytes=log_config.get('max_bytes'),
            backup_count=log_config.get('backup_count')
        )

        self.logger.info('AIQAnalyticsJobScheduler init')
        self.aiq_analytics_config = config['aiq_analytics']
        self.file_data_loader = FileDataLoader(self.aiq_analytics_config)
        self.subscription_profile_loader = SubscriberProfileLoader(self.aiq_analytics_config)
        self.scheduler = BlockingScheduler(timezone="Asia/Kolkata")

        self.schedule_jobs()

    def schedule_jobs(self):

        jobs = self.aiq_analytics_config.get("jobs", [])
        for job in jobs:
            if job.get("name") == "file_dataloader" and job.get("active"):
                cron = job.get("cron", {})
                minutes = cron.get("minutes", "*")
                hours = cron.get("hours", "*")
                day_of_week = cron.get("day_of_week", "*")
                self.scheduler.add_job(self.file_data_loader.run_loader, "cron", minute=minutes, hour=hours, day_of_week=day_of_week)
                self.logger.info('scheduled --> file dataloader job')

            if job.get("name") == "subscriber_profile_loader" and job.get("active"):
                cron = job.get("cron", {})
                minutes = cron.get("minutes", "*")
                hours = cron.get("hours", "*")
                day_of_week = cron.get("day_of_week", "*")
                self.scheduler.add_job(self.subscription_profile_loader.sync_es_to_db, "cron", minute=minutes, hour=hours, day_of_week=day_of_week)
                self.logger.info('scheduled --> subscription profile loader job')

            if job.get("name") == "subscriber_profile_update_churned" and job.get("active"):
                cron = job.get("cron", {})
                minutes = cron.get("minutes", "*")
                hours = cron.get("hours", "*")
                day_of_week = cron.get("day_of_week", "*")
                self.scheduler.add_job(self.subscription_profile_loader.update_churned, "cron", minute=minutes, hour=hours, day_of_week=day_of_week)
                self.logger.info('scheduled --> subscription profile update churned job')

        self.logger.info('all jobs scheduled')


    def run(self):
        self.logger.info('starting scheduler')
        try:
            self.scheduler.start()
        except (KeyboardInterrupt, SystemExit):
            print("Scheduler stopped manually.")


if __name__ == "__main__":
    analytics_job_scheduler = AIQAnalyticsJobScheduler(config)
    analytics_job_scheduler.run()

