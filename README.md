# Piscine Django - Day 05

## Description des Exercices

Cette série d'exercices avancés en Django se concentre sur l'utilisation approfondie de Django ORM, les manipulations de bases de données via SQL et ORM, la gestion des relations entre les modèles, ainsi que l'implémentation de fonctionnalités avancées telles que la mise à jour de données et l'utilisation de clés étrangères. Les exercices couvrent la création de tables et de modèles, l'insertion et la mise à jour de données, ainsi que des opérations plus complexes impliquant des relations Many-to-Many.

## Installation

### Install Postgresql
```bash
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
```

### Configure postgresql
```bash
sudo -u postgres psql
CREATE DATABASE formationdjango;
CREATE ROLE djangouser WITH LOGIN PASSWORD 'secret';
GRANT ALL PRIVILEGES ON DATABASE formationdjango TO djangouser;
ALTER ROLE djangouser CREATEDB CREATEROLE;
\q
```

### Start Django server
```bash
python -m venv venv
source venv/bin/activate
pip install -r reauirements.txt
python manage.py makemigrations ex01 ex03 ex05 ex07 ex09
python manage.py migrate
```