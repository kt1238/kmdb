from django.shortcuts import render
from django.http import HttpResponse
from load import loadcsvfile
from demo.models import Movie
import random

# Create your views here.
def home(request):
    loadcsvfile()
    return render(request, 'home.html')

def all(request):
    records = Movie.objects.all()
    context = {
        'records':records
    }
    return render(request,'all.html',context)

def details(request,movie_id):
    movie = Movie.objects.get(pk=movie_id)
    context = {
        'movie': movie
    }
    return render(request,'details.html',context)

def search(request):
    if request.method == 'POST':
        search_term = request.POST['search_term']
    # Creates an empty QuerySet
    year_query = Movie.objects.none()
    if search_term.isnumeric():
        year_query = Movie.objects.filter(release_year=search_term)

    result = Movie.objects.filter(name__contains=search_term) | Movie.objects.filter(genre_1__contains=search_term) | year_query

    context = {
        'search_term': search_term,
        'result': result
    }
    return render(request,'search.html',context)

def random_movie(request):
    id = random.randint(1,1253)
    return details(request,id)
