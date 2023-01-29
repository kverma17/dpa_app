from django.shortcuts import render
from django.http import HttpResponse
import requests
import xmltodict

# Create your views here.
def index(request):
    timeframe = request.GET.get('timeframe')
    print(timeframe)
    file_format = request.GET.get('format')
    print(file_format)
    template = request.GET.get('template')
    print(template)
    nodes = request.GET.getlist('nodes', '')
    print(nodes)
    url = "https://rs01sv01.bnl.cos.lan:9002/dpa-api/report/" # <16 digit ID>
    for node in nodes:
        if node:
            user = ''
            password = ''
            session = requests.Session()
            session.auth = (user, password)
            response = session.get("https://rs01sv01.bnl.cos.lan:9002/dpa-api/report/")
            dict_data = xmltodict.parse(response.content)
            print(dict_data)
            # print(f"ID for node {node} : {dict_data['licenses']['license']['id']}")
    return render(request, "home.html")