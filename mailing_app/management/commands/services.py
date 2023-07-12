import time

import schedule
from django.core.management import BaseCommand
from mailing_app.services import run_scheduler


class Command(BaseCommand):

    def handle(self, *args, **options):
        run_scheduler()
        while True:
            schedule.run_pending()
            time.sleep(1)
