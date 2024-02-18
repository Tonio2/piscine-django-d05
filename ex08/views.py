from django.http import HttpResponse
from django.db import connection
from django.db.utils import DatabaseError
from django.shortcuts import render


def initialize_database(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS ex08_planets (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(64) UNIQUE NOT NULL,
                    climate VARCHAR,
                    diameter INTEGER,
                    orbital_period INTEGER,
                    population BIGINT,
                    rotation_period INTEGER,
                    surface_water REAL,
                    terrain VARCHAR(128)
                );
            """
            )

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS ex08_people (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(64) UNIQUE NOT NULL,
                    birth_year VARCHAR(32),
                    gender VARCHAR(32),
                    eye_color VARCHAR(32),
                    hair_color VARCHAR(32),
                    height INTEGER,
                    mass REAL,
                    homeworld VARCHAR(64),
                    FOREIGN KEY (homeworld) REFERENCES ex08_planets(name)
                );
            """
            )

            # Commit is not necessary with Django's database wrapper
        return HttpResponse("OK", status=200)
    except DatabaseError as e:
        return HttpResponse(f"Error occurred: {e}", status=500)


def populate_database(request):
    response = ""
    try:
        with connection.cursor() as cursor:
            with open("ex08/planets.csv", "r") as file:
                cursor.copy_from(
                    file,
                    "ex08_planets",
                    sep="\t",
                    null="NULL",
                    columns=(
                        "name",
                        "climate",
                        "diameter",
                        "orbital_period",
                        "population",
                        "rotation_period",
                        "surface_water",
                        "terrain",
                    ),
                )
            response += "Planets: OK\n"

            with open("ex08/people.csv", "r") as file:
                cursor.copy_from(
                    file,
                    "ex08_people",
                    sep="\t",
                    null="NULL",
                    columns=(
                        "name",
                        "birth_year",
                        "gender",
                        "eye_color",
                        "hair_color",
                        "height",
                        "mass",
                        "homeworld",
                    ),
                )
            response += "People: OK"

        connection.commit()

    except Exception as e:
        response = str(e)

    return HttpResponse(response)


def display(request):
    try:
        with connection.cursor() as cursor:
            # Exécuter la requête SQL
            cursor.execute(
                """
                SELECT p.name, p.homeworld, pl.climate
                FROM ex08_people p
                JOIN ex08_planets pl ON p.homeworld = pl.name
                WHERE pl.climate LIKE '%windy%'
                ORDER BY p.name;
            """
            )

            rows = cursor.fetchall()

            if not rows:
                return HttpResponse("No data available")

            # Construire la réponse
            response = "<ul>"
            for row in rows:
                response += f"<li>{row[0]} - {row[1]} - {row[2]}</li>"
            response += "</ul>"

            return HttpResponse(response)

    except Exception:
        return HttpResponse("No data available")
