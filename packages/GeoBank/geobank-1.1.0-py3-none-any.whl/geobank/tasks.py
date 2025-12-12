from celery import shared_task

from .utils import populate_geobank_data


@shared_task
def populate_geobank_task(population_gte: int = 15000):
    populate_geobank_data(population_gte)
