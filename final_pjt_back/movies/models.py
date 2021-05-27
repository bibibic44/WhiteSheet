from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings

# Create your models here.
class Movie(models.Model):
    movie_key = models.IntegerField()
    title = models.CharField(max_length=150, null=True)
    overview = models.CharField(max_length=300, null=True)
    genre = models.CharField(max_length=100, null=True)
    vote_average = models.FloatField(null=True)
    release_date = models.CharField(max_length=100, null=True)
    poster_path = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.title


class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    movie_title = models.CharField(max_length=100)
    title = models.CharField(max_length=150)
    content = models.CharField(max_length=500)
    rank = models.IntegerField(default=5, validators=[MaxValueValidator(10), MinValueValidator(1)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    username = models.CharField(max_length=50, null=True)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    content = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content


class Recommendation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    interested_genre = models.CharField(max_length=100)

    def __str__(self):
        return self.interested_genre
