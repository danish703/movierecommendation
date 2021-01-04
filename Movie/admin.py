from django.contrib import admin
from.models import Genre, Movie,WatchList
# Register your models here.
admin.site.register(Genre)
admin.site.register([Movie,WatchList])