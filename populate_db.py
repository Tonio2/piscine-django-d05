import os
import django
import json

# Configuration de l'environnement Django pour le script
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'd05.settings')
django.setup()

from ex09.models import Planets, People

def main():
    with open("ex09_initial_data.json", "r") as file:
        json_data = json.load(file)
        for elm in json_data:
            if elm.model == "ex09.planets":
                Planets.objects.create(id=elm.pk, name=elm.fields["name"], climate=elm.fields["climate"], diameter=elm.fields["diameter"], orbital_period=elm.fields["orbital_period"], population=elm.fields["population"], rotation_period=elm.fields["rotation_period"], surface_water=elm.fields["surface_water"], terrain=elm.fields["terrain"])
            elif elm.model == "ex09.people":
                People.objects.create(id=elm.pk, name=elm.fields["name"], birth_year=elm.fields["birth_year"], gender=elm.fields["gender"], eye_color=elm.fields["eye_color"], hair_color=elm.fields["hair_color"], height=elm.fields["height"], mass=elm.fields["mass"], homeworld=elm.fields["homeworld"], created=elm.fields["created"], updated=elm.fields["updated"])

if __name__ == '__main__':
    main()