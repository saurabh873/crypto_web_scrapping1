

from django.db import models
import uuid

class ScrapingJob(models.Model):
    job_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

class ScrapingTask(models.Model):
    job = models.ForeignKey(ScrapingJob, related_name='tasks', on_delete=models.CASCADE)
    coin = models.CharField(max_length=10)
    output = models.JSONField()
