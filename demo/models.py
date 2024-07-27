from django.db import models

# Create your models here.
class Movie(models.Model):
    movie_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    release_year = models.IntegerField(null=True)
    language = models.CharField(max_length=45)
    genre_1 = models.CharField(max_length=45)
    watched = models.BooleanField()
    priority = models.IntegerField()
    extra_info = models.CharField(max_length=100)

    def __str__(self):
        return self.name