from django.shortcuts import render
from django.http import HttpResponse
import requests
import json
from base64 import b64encode
import xmltodict

with open("cred.json", "r") as file:
    credentials = json.load(file)
    token = b64encode(f'{credentials["username"]}:{credentials["password"]}'.encode("utf-8")).decode("ascii")
    auth =  f"Basic {token}"

# Create your views here.
def index(request):
    timeframe = request.GET.get('timeframe')
    file_format = request.GET.get('format')
    hostname = request.GET.get('hostname')
    template = request.GET.get('template')
    execute = request.GET.get('execute', False)
    nodes = request.GET.getlist('nodes', '')
    url = f"https://{hostname}:9002/dpa-api/report/" # <16 digit ID>
    pdfs, file_output = [], "nodes.csv"
    headers = {
        "Content-Type": "application/vnd.emc.apollo-v1+xml",
        "Authorization": auth
    }
    for node in nodes:
        if node:
            user = 'lcgjjyoth'
            password = 'Vamshi@3108'
            session = requests.Session()
            session.auth = (user, password)
            response = session.get(f"https://{hostname}:9002/apollo-api/nodes/?query=name%3d" + node, verify=False)
            dict_data = xmltodict.parse(response.content)
            node_id = dict_data['nodes']['node']['id']
            xml = """<runReportParameters>
<report>
<name><template></name> <!-- Report template name -->
</report>
<nodes>
<node>
<!-- scope - node id of the Host -->
<id><node_id></id>
</node>
</nodes>
<timeConstraints type="window">
<window >
<name><timeframe></name> <!-- time period name -->
</window>
</timeConstraints>
<formatParameters>
<!-- format type, could be CSV, HTML, PDF, IMAGE, XML. -->
<formatType><format_type></formatType>
</formatParameters>
</runReportParameters>"""
            xml = xml.replace("<template>", template)
            xml = xml.replace("<timeframe>", timeframe)
            xml = xml.replace("<node_id>", node_id)
            file_format = 'PDF'
            xml = xml.replace("<format_type>", file_format)
            
            response = requests.post(
                f"https://{hostname}:9002/dpa-api/report",
                headers = {
                    "Content-Type": "application/vnd.emc.apollo-v1+xml",
                    "Authorization": auth
                },
                verify=False,
                data=xml
            )
            output_data = xmltodict.parse(response.content)
            output_link = output_data["report"]["link"]
            print(output_link)
            if execute:
                response = requests.request(
                    "GET",
                    output_link,
                    headers = {
                        "Content-Type": "application/vnd.emc.apollo-v1+xml",
                        "Authorization": 'Basic cmVzdHVzZXI6V2VsY29tZUAxMjM='
                    },
                    data = {},
                    verify=False
                )
                pdfs.append(response.text)
    if execute:
        for content in pdfs:
            open(file_output, 'wb').write(content)
        FilePointer = open(file_output,"r")
        response = HttpResponse(FilePointer,content_type='application/csv')
        response['Content-Disposition'] = f'attachment; filename={file_output}'

        return response
    return render(request, "home.html")