import random
from django.shortcuts import render
from django.http import HttpResponse
from .models import Movie
from django.views import generic


# Create your views here.
def home(request):
    return render(request, 'home.html')


class MovieView(generic.list.ListView):
    model = Movie
    template_name = 'all.html'
    context_object_name = 'movies'


def details(request, id):
    movie = Movie.objects.get(id=id)
    context = {
        'movie': movie
    }
    return render(request, 'details.html', context)


def search(request):
    if request.method == 'POST':
        search_term = request.POST['search_term']
    # Creates an empty QuerySet
    year_query = Movie.objects.none()
    if search_term.isnumeric():
        year_query = Movie.objects.filter(release_year=search_term)

    result = Movie.objects.filter(name__contains=search_term) | Movie.objects.filter(
        genre_1__contains=search_term) | year_query

    context = {
        'search_term': search_term,
        'result': result
    }
    return render(request, 'search.html', context)


def random_movie(request):
    id = random.randint(1, Movie.objects.count())
    return details(request, id)
