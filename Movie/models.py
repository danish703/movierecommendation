from django.db import models
# Create your models here.
from django.db.models import Sum,Count
from django.contrib.auth.models import User
class Genre(models.Model):
    title = models.CharField(max_length=100)
    def __str__(self):
        return self.title

class Movie(models.Model):
    movie_name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='movieimg/')
    release_year = models.CharField(max_length=4)
    Genre = models.ForeignKey(Genre,on_delete=models.CASCADE)

    def __str__(self):
        return self.movie_name


    @property
    def averageRate(self):
        from rate.models import Rate
        sum = Rate.objects.filter(movie=self).aggregate(Sum('rating'))
        c = Rate.objects.filter(movie=self).aggregate(Count('rating'))
        if sum['rating__sum'] == None:
            avg = 0;
        else:
            avg = int(sum['rating__sum'] / c['rating__count'])
        return avg

class  WatchList(models.Model):
    movie = models.ForeignKey(Movie,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.movie)

    class Meta:
        unique_together = ('movie','user')