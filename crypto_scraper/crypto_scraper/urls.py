# crypto_scraper/urls.py

from django.contrib import admin
from django.urls import path
from api.views import StartScraping, ScrapingStatus

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/taskmanager/start_scraping', StartScraping.as_view(), name='start-scraping'),
    path('api/taskmanager/scraping_status/<uuid:job_id>', ScrapingStatus.as_view(), name='scraping-status'),
]
