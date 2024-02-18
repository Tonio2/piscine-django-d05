from django.http import HttpResponse
from django.shortcuts import render
from .models import Planets, People

# Create your views here.
def display(request):
    try:
        people = People.objects.filter(homeworld__climate__icontains="windy").order_by("name").values("name", "homeworld__name", "homeworld__climate")
        
        if not people:
            return HttpResponse("No data available, please use the following command line before use: python populate_db.py")
        
        html = "<table><tr><th>Name</th><th>Homeworld</th><th>Climate</th></tr>"
        for p in people:
            html += "<tr><td>{}</td><td>{}</td><td>{}</td></tr>".format(p["name"], p["homeworld__name"], p["homeworld__climate"])
        html += "</table>"
        return HttpResponse(html)
    except Exception as e:
        return HttpResponse(str(e))
    


