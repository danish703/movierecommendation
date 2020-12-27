from django.shortcuts import render,redirect
from .models import Movie,Genre
from rate.forms import RateForm
from django.contrib import messages

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
            data = form.save(commit=False)
            data.user = request.user
            data.movie_id = id
            data.save()
            messages.add_message(request,messages.SUCCESS,"Your rating has been successfully added.")
            return redirect('readmore', id)
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
