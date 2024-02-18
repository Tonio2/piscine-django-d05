from django.http import HttpResponse
from django.db import connection
from django.db.utils import DatabaseError
from django.shortcuts import render


def initialize_database(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS ex06_movies (
                    episode_nb INT PRIMARY KEY,
                    title VARCHAR(64) NOT NULL UNIQUE,
                    opening_crawl TEXT,
                    director VARCHAR(32) NOT NULL,
                    producer VARCHAR(128) NOT NULL,
                    release_date DATE NOT NULL,
                    created TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    updated TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
                );
            """
            )

            cursor.execute(
                """
                  CREATE OR REPLACE FUNCTION update_changetimestamp_column()
                  RETURNS TRIGGER AS $$
                  BEGIN
                  NEW.updated = now();
                  NEW.created = OLD.created;
                  RETURN NEW;
                  END;
                  $$ language 'plpgsql';
                  CREATE TRIGGER update_films_changetimestamp BEFORE UPDATE
                  ON ex06_movies FOR EACH ROW EXECUTE PROCEDURE
                  update_changetimestamp_column();
                """
            )
            # Commit is not necessary with Django's database wrapper
        return HttpResponse("OK", status=200)
    except DatabaseError as e:
        return HttpResponse(f"Error occurred: {e}", status=500)


def populate_database(request):
    responses = []
    try:
        with connection.cursor() as cursor:
            for movie in movies:
                try:
                    cursor.execute(
                        """
                        INSERT INTO ex06_movies
                        (episode_nb, title, director, producer, release_date)
                        VALUES
                        (%s, %s, %s, %s, %s);
                    """,
                        movie,
                    )
                    responses.append(f"OK: {movie[1]}")
                except Exception as e:
                    responses.append(f"Failed: {movie[1]} - {str(e)}")
            # Commit is not necessary with Django's database wrapper
        return HttpResponse("<br>".join(responses))
    except Exception as e:
        return HttpResponse(f"Error occurred: {e}", status=500)


def display(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT * FROM ex06_movies;
            """
            )
            # Commit is not necessary with Django's database wrapper
            rows = cursor.fetchall()
            if not rows:
                return HttpResponse("No data available", status=404)
            html = "<table><tr><th>Episode</th><th>Title</th><th>Opening crawl</th><th>Director</th><th>Producer</th><th>Release Date</th></tr>"
            for movie in rows:
                html += f"<tr><td>{movie[0]}</td><td>{movie[1]}</td><td>{movie[2]}</td><td>{movie[3]}</td><td>{movie[4]}</td><td>{movie[5]}</td></tr>"
            html += "</table>"
            return HttpResponse(html)
    except Exception as e:
        return HttpResponse(f"Error occurred: {e}", status=500)


def update(request):
    try:
        # Connexion à la base de données
        with connection.cursor() as cursor:
            if request.method == "POST":
                # Si le formulaire est soumis, supprimer le film sélectionné
                movie_to_remove = request.POST.get("movie_title")
                opening_crawl = request.POST.get("opening_crawl")
                cursor.execute(
                    "UPDATE ex06_movies SET opening_crawl = %s WHERE title = %s",
                    [opening_crawl, movie_to_remove],
                )

            # Récupérer la liste des films restants
            cursor.execute("SELECT title FROM ex06_movies")
            movies = cursor.fetchall()

        if not movies:
            return HttpResponse("No data available")

        # Préparer les données pour le template
        context = {"movies": movies}
        return render(request, "ex06/update.html", context)

    except Exception as e:
        return HttpResponse(f"Error occurred: {e}", status=500)


movies = [
    (1, "The Phantom Menace", "George Lucas", "Rick McCallum", "1999-05-19"),
    (2, "Attack of the Clones", "George Lucas", "Rick McCallum", "2002-05-16"),
    (3, "Revenge of the Sith", "George Lucas", "Rick McCallum", "2005-05-19"),
    (4, "A New Hope", "George Lucas", "Gary Kurtz, Rick McCallum", "1977-05-25"),
    (
        5,
        "The Empire Strikes Back",
        "Irvin Kershner",
        "Gary Kutz, Rick McCallum",
        "1980-05-17",
    ),
    (
        6,
        "Return of the Jedi",
        "Richard Marquand",
        "Howard G. Kazanjian, George Lucas, Rick McCallum",
        "1983-05-25",
    ),
    (
        7,
        "The Force Awakens",
        "J. J. Abrams",
        "Kathleen Kennedy, J. J. Abrams, Bryan Burk",
        "2015-12-11",
    ),
]
