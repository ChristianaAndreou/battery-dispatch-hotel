from django.core.management.base import BaseCommand

from reports.services.data_generation import generate_week_data
from reports.services.dispatch import run_dispatch


class Command(BaseCommand):
    help = "Generate weekly time series data and run battery dispatch"

    def handle(self, *args, **options):
        generate_week_data()
        run_dispatch()
        self.stdout.write(self.style.SUCCESS("Generated data and dispatch results"))