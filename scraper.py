import urllib
import re
import json
import xml.etree.cElementTree as ET


def get_stations(city):
    url = 'https://%s.bixi.com/data/bikeStations.xml' % city
    response = urllib.urlopen(url)
    content = ET.parse(response)

    # Go through the Javascript, looking for `var station`s
    # Best API ever
    #matches = content.getroot().findall("station")

    stations = {}

    for station in content.getroot().findall("station"):
        # Take everything between the { and the closing } (inclusive)
        # station_json = match[match.index('{'):match.index('}') + 1]

        # Have to double-quote all the keys before loading it
        # If there's extra whitespace before the key, ignore it
        # station_json = re.sub('(?P<prefix>[{,])[ ]?(?P<key>[^:]+):', '\g<prefix>"\g<key>":', station_json)

        # Some stations have unnecessarily escaped single quotes - fix that
        # station_json = station_json.replace("\\'", "'")
        # station = json.loads(station_json)

        # Save it in the stations dictionary
        station_id = int(station.find('id').text)
        stations[station_id] = {
            'docks': int(station.find('nbEmptyDocks').text),
            'bikes': int(station.find('nbBikes').text),
            'name': station.find('name').text,
            'longitude': float(station.find('long').text),
            'latitude': float(station.find('lat').text),
            'installed': bool(station.find('installed').text),
            'locked': bool(station.find('locked').text),
            'temporary': bool(station.find('temporary').text),
        }
    response.close()
    return stations
