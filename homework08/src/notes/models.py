from django.utils import timezone
from django.contrib.auth.models import User

from django.db import models
from config.settings import base

class Note(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    owner = models.ForeignKey(base.AUTH_USER_MODEL, related_name='notes', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def was_published_recently(self):
        now = timezone.now()
        return now - timezone.timedelta(days=1) <= self.pub_date <= now
