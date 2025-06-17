from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=200)
    year = models.CharField(max_length=10)
    poster = models.URLField()
    plot = models.TextField()

    def __str__(self):
        return self.title
