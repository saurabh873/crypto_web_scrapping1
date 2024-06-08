# api/tasks.py

from celery import shared_task
from .models import ScrapingJob, ScrapingTask
from .scraper import CoinMarketCapScraper

@shared_task
def scrape_coin_data(job_id, coin):
    scraper = CoinMarketCapScraper()
    data = scraper.scrape_coin_data(coin)
    job = ScrapingJob.objects.get(id=job_id)
    ScrapingTask.objects.create(job=job, coin=coin, output=data)
    scraper.close()
