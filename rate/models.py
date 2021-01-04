from django.db import models
from django.contrib.auth.models import User
from Movie.models import Movie
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class Rate(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MaxValueValidator(4),MinValueValidator(1)],default=2)

    class Meta:
        unique_together=('movie','user')

    def __str__(self):
        return str(self.rating)