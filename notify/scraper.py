import urllib
import re
import json
import math
import logging
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

def get_bikes(city, location):
    logging.info("get_bikes")
    url = 'https://%s.bixi.com/data/bikeStations.xml' % city
    response = urllib.urlopen(url)
    content = ET.parse(response)

    """ create a stations dictionary """
    stations = {}
    stations_distance = []
    for station in content.getroot().findall("station"):
        # Save it in the stations dictionary
        station_id = int(station.find('id').text)
        lon = float(station.find('long').text)
        lat = float(station.find('lat').text)
        distance = float(distance_on_unit_sphere(location.get('latitude'), location.get('longitude'),lat,lon))
        """logging.info('the distance is %s.' % distance)"""
        stations[station_id] = {
            'distance' : distance,
            'docks': int(station.find('nbEmptyDocks').text),
            'bikes': int(station.find('nbBikes').text),
            'name': station.find('name').text,
            'longitude': lon,
            'latitude': lat,
            'installed': bool(station.find('installed').text),
            'locked': bool(station.find('locked').text),
            'temporary': bool(station.find('temporary').text),
        }
        stations_distance.append(stations[station_id])
    response.close()
    """logging.info("station list %s" %stations_distance)"""
    newlist = sorted(stations_distance, key=lambda k: k['distance']) 
    """logging.info("station list %s" %newlist)"""
    for station_data in newlist:
        if station_data['bikes'] > 0:
            message = str(station_data['name'])
            return station_data

def get_stops(city, location):
    logging.info("get_bikes")
    url = 'https://%s.bixi.com/data/bikeStations.xml' % city
    response = urllib.urlopen(url)
    content = ET.parse(response)

    """ create a stations dictionary """
    stations = {}
    stations_distance = []
    for station in content.getroot().findall("station"):
        # Save it in the stations dictionary
        station_id = int(station.find('id').text)
        lon = float(station.find('long').text)
        lat = float(station.find('lat').text)
        distance = float(distance_on_unit_sphere(location.get('latitude'), location.get('longitude'),lat,lon))
        """logging.info('the distance is %s.' % distance)"""
        stations[station_id] = {
            'distance' : distance,
            'docks': int(station.find('nbEmptyDocks').text),
            'bikes': int(station.find('nbBikes').text),
            'name': station.find('name').text,
            'longitude': lon,
            'latitude': lat,
            'installed': bool(station.find('installed').text),
            'locked': bool(station.find('locked').text),
            'temporary': bool(station.find('temporary').text),
        }
        stations_distance.append(stations[station_id])
    response.close()
    logging.info("station list %s" %stations_distance)
    newlist = sorted(stations_distance, key=lambda k: k['distance']) 
    logging.info("station list %s" %newlist)
    for station_data in newlist:
        if station_data['docks'] > 0:
            message = str(station_data['name'])
            return station_data

def distance_on_unit_sphere(lat1, long1, lat2, long2):

    # Convert latitude and longitude to 
    # spherical coordinates in radians.
    degrees_to_radians = math.pi/180.0
        
    # phi = 90 - latitude
    phi1 = (90.0 - lat1)*degrees_to_radians
    phi2 = (90.0 - lat2)*degrees_to_radians
        
    # theta = longitude
    theta1 = long1*degrees_to_radians
    theta2 = long2*degrees_to_radians
        
    # Compute spherical distance from spherical coordinates.
        
    # For two locations in spherical coordinates 
    # (1, theta, phi) and (1, theta, phi)
    # cosine( arc length ) = 
    #    sin phi sin phi' cos(theta-theta') + cos phi cos phi'
    # distance = rho * arc length
    
    cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) + 
           math.cos(phi1)*math.cos(phi2))
    arc = math.acos( cos )

    # Remember to multiply arc by the radius of the earth 
    # in your favorite set of units to get length.
    return arc

