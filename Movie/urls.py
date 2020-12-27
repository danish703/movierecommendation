from django.urls import path
from .views import readmore,genereMovieList
urlpatterns= [
    path('<int:id>', readmore, name='readmore'),
    path('genre/<int:cid>',genereMovieList,name='generemovielist')
]