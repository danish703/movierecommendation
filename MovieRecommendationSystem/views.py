from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from Movie.models import Movie,Genre
from recommendation.datapreparation import PrePareData
from rate.forms import RateForm
#from .ratecalc import average
def home(request):
    allmovies = Movie.objects.all()
    genre= Genre.objects.all()
    p = PrePareData(13)
    print(p.calcuatePearsonCoffiecient().items())
    context = {
        'movies' :allmovies,
        'genre':genre

    }
    return render(request,'index.html', context)

def about(request):
    return render(request,'about.html')

def signup(request):
    if request.method == 'GET':
        form = CustomUserCreationForm()
        context = {
            'form': form
        }
        return render(request,'SignUp.html', context)

    else:
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            if request.POST['password1']==request.POST['password2']:
                data = form.save(commit=False)
                password = request.POST['password1']
                data.set_password(password)
                data.save()
                messages.add_message(request,messages.SUCCESS, "User sucessfully added")
                return redirect('signin')
            else:
                messages.add_message(request,messages.ERROR,"password does not match")
                return render(request,'SignUp.html',{'form':form})
        else:
            return render(request, 'Signup.html', {'form' : form})

@login_required(login_url='signin')
def dashboard(request):
    return render(request,'dashboard.html')

def signin(request):
    if request.method=='GET':
        return render(request,'Login.html')
    else:
        inputusername = request.POST['username']
        inputpassword = request.POST['password']

        user = authenticate(username=inputusername, password=inputpassword)
        if user is not None:
            login(request, user=user)
            return redirect('dashboard')
        else:
            messages.add_message(request, messages.ERROR, "Username or Password does not match")
            return redirect('signin')

def signout(request):
    logout(request)
    return redirect('signin')


