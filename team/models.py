from django.db import models
from django.utils import timezone

class Reply(models.Model):
    POSITIVE = 1
    NEUTRAL = 2
    NEGATIVE = 3

    user_name = models.CharField(max_length=100)
    user_id = models.CharField(max_length=100)
    response = models.IntegerField(default=NEUTRAL)

class Translatelog(models.Model):
    user_name = models.CharField(max_length=100)
    user_id = models.CharField(max_length=100)
    origin_text = models.TextField()
    deepl_text = models.TextField()
    source_lang = models.CharField(max_length=20)
    target_lang = models.CharField(max_length=20)
    date = models.DateTimeField(default=timezone.now)