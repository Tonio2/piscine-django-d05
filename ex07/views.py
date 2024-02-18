import datetime
from django.http import HttpResponse
from django.db import connection
from django.shortcuts import render
from .models import Movies
from .forms import MovieForm


def populate_database(request):
    responses = []
    for movie in movies:
        try:
            Movies.objects.create(
                episode_nb=movie[0],
                title=movie[1],
                director=movie[2],
                producer=movie[3],
                release_date=datetime.datetime.strptime(movie[4], "%Y-%m-%d"),
            )
            responses.append(f"OK: {movie[1]}")
        except Exception as e:
            responses.append(f"Failed: {movie[1]} - {str(e)}")

    return HttpResponse("<br>".join(responses))


def display(request):
    try:
        movies = Movies.objects.all()
        if not movies:
            return HttpResponse("No data available", status=404)
        html = "<table><tr><th>Episode</th><th>Title</th><th>Opening crawl</th><th>Director</th><th>Producer</th><th>Release Date</th></tr>"
        for movie in movies:
            html += f"<tr><td>{movie.episode_nb}</td><td>{movie.title}</td><td>{movie.opening_crawl}</td><td>{movie.director}</td><td>{movie.producer}</td><td>{movie.release_date}</td></tr>"
        html += "</table>"
        return HttpResponse(html)
    except Exception as e:
        return HttpResponse(f"Error occurred: {e}", status=500)


def update(request):
    try:
        if request.method == "POST":
            form = MovieForm(request.POST)
            if form.is_valid():
                movie = form.cleaned_data["movie"]
                movie.opening_crawl = form.cleaned_data["opening_crawl"]
                movie.save()

        form = MovieForm()  # Refresh form to update movie list
        movies = Movies.objects.all()

    except Exception as e:
        return HttpResponse(f"Error occurred: {e}", status=500)

    context = {"form": form, "movies": movies}
    return render(request, "ex07/update.html", context)


movies = [
    [1, "The Phantom Menace", "George Lucas", "Rick McCallum", "1999-05-19"],
    [2, "Attack of the Clones", "George Lucas", "Rick McCallum", "2002-05-16"],
    [3, "Revenge of the Sith", "George Lucas", "Rick McCallum", "2005-05-19"],
    [4, "A New Hope", "George Lucas", "Gary Kurtz, Rick McCallum", "1977-05-25"],
    [
        5,
        "The Empire Strikes Back",
        "Irvin Kershner",
        "Gary Kutz, Rick McCallum",
        "1980-05-17",
    ],
    [
        6,
        "Return of the Jedi",
        "Richard Marquand",
        "Howard G. Kazanjian, George Lucas, Rick McCallum",
        "1983-05-25",
    ],
    [
        7,
        "The Force Awakens",
        "J. J. Abrams",
        "Kathleen Kennedy, J. J. Abrams, Bryan Burk",
        "2015-12-11",
    ],
]
