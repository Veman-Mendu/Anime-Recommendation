from asyncio.windows_events import NULL
from unittest.util import _MAX_LENGTH
from django.db import models

# Create your models here.
class anime(models.Model):
    epsiodes = models.IntegerField(("Episodes"))
    status = models.CharField(("Status"), max_length=255)
    ratings = models.CharField(("Ratings"), max_length=255)
    scores = models.FloatField(("Scores"))
    rank = models.IntegerField(("Rank"))
    popularity = models.IntegerField(("Popularity"))
    members = models.BigIntegerField(("Members"))
    favorites = models.BigIntegerField(("Favorites"))
    title = models.CharField(("titles"), max_length=255)
    sp = models.CharField(("SP"), max_length=255)
    genre = models.CharField(("Genre"), max_length=255)
    studio = models.CharField(("Studio"), max_length=255)
