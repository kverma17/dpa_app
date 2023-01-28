from django.shortcuts import render
from django.http import HttpResponse
import requests

# Create your views here.
def index(request):
    timeframe = request.GET.get('timeframe')
    print(timeframe)
    nodes = request.GET.getlist('nodes', '')
    print(nodes)
    url = "https://rs01sv01.bnl.cos.lan:9002/dpa-api/report/"
    for node in nodes:
        if node:
            response = requests.get("https://reqres.in/api/users/" + node)
            print(response.json())
    return render(request, "home.html")