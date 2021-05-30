from lxml import html
import requests
import itertools
import json

header = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'}

with open('site_info.json') as json_file:
    site_info = json.load(json_file)


def get_incident_dict(incident, site):
    xpaths = site_info[site]['xpaths']

    if str(type(incident)) == "<class 'lxml.etree._ElementUnicodeResult'>":
        url = site_info[site]['main_url'] + incident if incident.startswith('/') else incident
        incident_dom = html.fromstring(requests.get(url).text)
    else:
        incident_dom = incident
        incident = incident_dom.xpath(xpaths['link'])

    print(incident_dom.xpath(xpaths['name']))
    return {
        'name': incident_dom.xpath(xpaths['name']),
        'datetime': incident_dom.xpath(xpaths['datetime']),
        'source': incident_dom.xpath(xpaths['source']),
        'link': incident,
        'site': site
    }


def get_incidents_list(site):
    response = requests.get(site_info[site]['main_url'])
    dom = html.fromstring(response.text)

    incidents = []
    for incidents_group in site_info[site]['incidents_groups']:
        incidents += dom.xpath(incidents_group)

    return [get_incident_dict(incident, site) for incident in incidents[:5]]


incidents_list = [get_incidents_list(site) for site in site_info]
incidents_list = list(itertools.chain(*incidents_list))
print(len(incidents_list))

for x in incidents_list:
    print(x)
