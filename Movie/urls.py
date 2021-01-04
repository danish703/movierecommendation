from django.urls import path
from .views import readmore,genereMovieList,addToWatchList,myWatchList,rateHistory
urlpatterns= [
    path('<int:id>', readmore, name='readmore'),
    path('genre/<int:cid>',genereMovieList,name='generemovielist'),
    path('addwatchlist/<int:movieid>',addToWatchList,name='addtowatchlist'),
    path('mywatchlist/',myWatchList,name='mywatchlist'),
    path('history/',rateHistory,name='ratehistory'),
]