import logging
import sys

from django.core.management.base import BaseCommand

from geobank.utils import populate_geobank_data


class Command(BaseCommand):
    help = "Populate GeoBank data with translations based on settings.LANGUAGES"

    def add_arguments(self, parser):
        parser.add_argument(
            "--background",
            action="store_true",
            help="Run the population task in the background using Celery",
        )
        parser.add_argument(
            "--population-gte",
            type=int,
            choices=[500, 1000, 5000, 15000],
            help="Choose the minimum population...",
        )

    def handle(self, *args, **options):
        # Configure logging to show info messages on console
        logger = logging.getLogger("geobank")
        if not logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            handler.setLevel(logging.INFO)
            formatter = logging.Formatter("%(message)s")
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)

        population_gte = options.get("population_gte") or 15000

        if options["background"]:
            try:
                from geobank.tasks import populate_geobank_task

                populate_geobank_task.delay(population_gte)
                self.stdout.write(
                    self.style.SUCCESS("GeoBank population task started in background.")
                )
            except ImportError:
                self.stdout.write(
                    self.style.ERROR(
                        "Celery is not installed or configured. Running synchronously."
                    )
                )
                populate_geobank_data(population_gte)
                self.stdout.write(self.style.SUCCESS("GeoBank population completed successfully."))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error starting background task: {e}"))
        else:
            self.stdout.write("Starting GeoBank population...")
            populate_geobank_data(population_gte)
            self.stdout.write(self.style.SUCCESS("GeoBank population completed successfully."))
