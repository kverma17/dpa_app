from django.shortcuts import render
from django.http import HttpResponse
import requests
import xmltodict

# Create your views here.
def index(request):
    timeframe = request.GET.get('timeframe')
    file_format = request.GET.get('format')
    template = request.GET.get('template')
    nodes = request.GET.getlist('nodes', '')
    url = "https://rs01sv01.bnl.cos.lan:9002/dpa-api/report/" # <16 digit ID>
    pdfs, file_output = [], "nodes.pdf"
    headers = {'Content-Type': 'application/xml'} 
    for node in nodes:
        if node:
            user = 'lcgjjyoth'
            password = 'Vamshi@3108'
            session = requests.Session()
            session.auth = (user, password)
            response = session.get("https://rs01sv01.bnl.cos.lan:9002/apollo-api/nodes/?query=name%3d" + node, verify=False)
            dict_data = xmltodict.parse(response.content)
            node_id = dict_data['nodes']['node'][0]['id']
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
<name>Last Month</name> <!-- time period name -->
</window>
</timeConstraints>
<formatParameters>
<!-- format type, could be CSV, HTML, PDF, IMAGE, XML. -->
<formatType><format_type></formatType>
</formatParameters>
</runReportParameters>"""
            xml.replace("<template>", template)
            xml.replace("<node_id>", node_id)
            xml.replace("<format_type>", file_format)
            r = requests.post(url + node_id, data=xml, headers=headers)
            pdfs.append(r.content)
    if nodes:
        for content in pdfs:
            open(file_output, 'wb').write(content)
        FilePointer = open(file_output,"r")
        response = HttpResponse(FilePointer,content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename={file_output}'

        return response
    return render(request, "home.html")