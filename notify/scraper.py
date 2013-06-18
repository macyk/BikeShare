import urllib
import re
import json
import xml.etree.cElementTree as ET


def get_stations(city, station_start, station_end):
    url = 'https://%s.bixi.com/data/bikeStations.xml' % city
    response = urllib.urlopen(url)
    content = ET.parse(response)

    stations = {}

    for station in content.getroot().findall("station"):
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
    message = ''
    start_full = False
    start_empty = False
    end_full = False
    end_empty = False
    for station_id, station_data in stations.iteritems():
        if station_data['name'] == station_start:
            if station_data['docks'] == 0:
                start_full = True
                message += str('%s is Full.' % station_data['name'])
            if station_data['bikes'] == 0:
                start_empty = True
                message += str('%s is Empty.' % station_data['name'])
        if station_data['name'] == station_end:
            if station_data['docks'] == 0:
                end_full = True
                message += str('%s is Full.' % station_data['name'])
            if station_data['bikes'] == 0:
                end_empty = True 
                message += str('%s is Empty.' % station_data['name'])
    if(start_full == False & start_empty == False & end_empty == False & end_full== False):
        message = 'Good To Go :)'
    return message
