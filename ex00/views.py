from django.http import HttpResponse
from django.db import connection
from django.db.utils import DatabaseError


def initialize_database(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS ex00_movies (
                    episode_nb INT PRIMARY KEY,
                    title VARCHAR(64) NOT NULL UNIQUE,
                    opening_crawl TEXT,
                    director VARCHAR(32) NOT NULL,
                    producer VARCHAR(128) NOT NULL,
                    release_date DATE NOT NULL
                );
            """
            )
            # Commit is not necessary with Django's database wrapper
        return HttpResponse("OK", status=200)
    except DatabaseError as e:
        return HttpResponse(f"Error occurred: {e}", status=500)
