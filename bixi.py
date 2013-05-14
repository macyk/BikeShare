import sys
import os
import xml.etree.cElementTree as ET
from urllib2 import urlopen
import re

def main():
	for URL in ["https://toronto.bixi.com/data/bikeStations.xml"]:
        feed = urlopen(URL)
        tree = ET.parse(feed)
        for station in tree.getroot().findall("station"):
            nbBikes = station.find("nbBikes").text
            nbEmptyDocks = station.find("nbEmptyDocks").text
            station_lat = re.sub(r"\s", "", station.find("lat").text)
            station_long = re.sub(r"\s", "", station.find("long").text.strip())
            station_installed = station.find("installed").text
            station_locked = station.find("locked").text
            if (station_installed == "true" and station_locked != "true" and (nbBikes != "0" or nbEmptyDocks != "0")):
                print "<Placemark><name>%s bikes avail. - %s empty slots</name><styleUrl>#BixiIconStyle</styleUrl><Point><coordinates>%s,%s,0</coordinates></Point></Placemark>" % (nbBikes, nbEmptyDocks, station_long, station_lat)
        feed.close()