from django.shortcuts import render,redirect
from .models import Movie,Genre
from rate.forms import RateForm
from django.contrib import messages
from .models import WatchList
from rate.models import Rate
from django.contrib.auth.decorators import login_required
def readmore(request, id):
    if request.method=='GET':
        a = Movie.objects.get(pk=id)
        rateform = RateForm()
        context = {
            'movies': a,
            'rateform': RateForm
        }
        return render(request, 'readmore.html', context)
    else:
        form = RateForm(request.POST)
        if form.is_valid():
            try:
                data = form.save(commit=False)
                data.user = request.user
                data.movie_id = id
                data.save()
                messages.add_message(request,messages.SUCCESS,"Your rating has been successfully added.")
                return redirect('readmore', id)
            except:
                messages.add_message(request,messages.ERROR,"You already rate this movie")
                return redirect('readmore',id)
        else:
            messages.add_message(request, messages.ERROR, "An error occurred.")
            return render(request, 'readmore.html', {'rateform':form})


def genereMovieList(request,cid):
    genre = Genre.objects.get(pk=cid)
    context= {
        'title': genre.title,
         'movies':Movie.objects.filter(Genre=genre)
    }
    return render(request,'genremovies.html',context)

@login_required(login_url='signin')
def addToWatchList(request,movieid):
    try:
        a = WatchList(movie_id=movieid,user_id=request.user.id)
        a.save()
        messages.add_message(request,messages.SUCCESS,"successfully added to watchlist")
        return redirect('dashboard')
    except:
        messages.add_message(request,messages.ERROR,"already added to watchlist")
        return redirect('dashboard')



@login_required(login_url='signin')
def myWatchList(request):
    a = WatchList.objects.filter(user=request.user)
    watchlist_movie_id = []
    for x in a:
        watchlist_movie_id.append(x.movie_id)
    context = {
        'movies':Movie.objects.filter(id__in=watchlist_movie_id)
    }
    return render(request,'watchlist.html',context)

def rateHistory(request):
    x = Rate.objects.filter(user = request.user)
    context = {
        'rate':x
    }
    return render(request,'history.html',context)