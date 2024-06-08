from django.shortcuts import render


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ScrapingJob, ScrapingTask
from .serializers import ScrapingJobSerializer
from .tasks import scrape_coin_data

class StartScraping(APIView):
    def post(self, request, format=None):
        coin_list = request.data.get("coins", [])
        job = ScrapingJob.objects.create()
        for coin in coin_list:
            scrape_coin_data.delay(job.id, coin)
        return Response({"job_id": job.job_id}, status=status.HTTP_202_ACCEPTED)

class ScrapingStatus(APIView):
    def get(self, request, job_id, format=None):
        job = ScrapingJob.objects.get(job_id=job_id)
        serializer = ScrapingJobSerializer(job)
        return Response(serializer.data, status=status.HTTP_200_OK)
