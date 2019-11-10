from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime, date
import logging
from typing import List, Tuple, Dict, Optional
import time
import re
import pymysql
import requests
import json
import pprint

import csv

logging.basicConfig(level=logging.INFO)

appname = 'djangoo_api'

username = "pdtpatrick"
password = "u3!WL2uC0dxu"
# in seconds
start_time = 3600 * 48  # 48 hours
# airport code
# airport = "KSEA" # Frankfurt
airport = "EDDF"  # Frankfurt

# Create your views here.
def read_airport(filename: str) -> Dict[str, str]:
    keys = [
        "id",
        "name",
        "city",
        "country",
        "IATA",
        "ICAO",
        "latitude",
        "longitude",
        "altitude",
        "timezone",
        "dst",
        "tz",
        "type",
        "source",
    ]
    airports = csv.DictReader(open(filename), delimiter=",", quotechar='"', fieldnames=keys)
    d = {airport["ICAO"]: airport for airport in airports}
    return d

def call_api(airport: str = None) -> Dict[str, str]:
    """Call opensky API and return all departures

    begin = now - days ago
    end = now
    """
    current_time = time.time()
    URL = f"https://opensky-network.org/api/flights/departure?airport={airport}&begin={int(current_time) - start_time}&end={int(current_time)}"
    logging.info(f"URL is now: {URL}")
    r = requests.get(URL, auth=(username, password))
    if r.status_code == 404:
        logging.error("Cannot find data")
        return None
    assert len(r.json()) != 0
    return r.json()

def process_coordinates(start_time: int, end_time: int) -> List[Dict[str, str]]:
    """Process Coordinates
    Pull data from opensky api, read the csv and create an output like:

    List[Dict[Dict[str, str]]]

    Meaning, we'll have a List[Airport[Coordinates[longitude, latitude]]]
    """
    
    with open('airports.csv') as csv_file:
        data = csv.reader(csv_file, delimiter=',')
        out_data=[]
        
        for departure in call_api(read_airport):
            arrival_airport = departure["estarrival"]
            departure_airport = departure["estdeparture"]
            
            # departure
            long_departure = departure_airport["longitude"]
            lat_departure = departure_airport["latitude"]
            
            # arrival
            long_arrival = arrival_airport["longitude"]
            lat_arrival = arrival_airport["latitude"]
            
            out_data.append({
                "departure":
              {
                   "longitude":long_departure, 
                   "latitude": lat_departure
                },
              
                "arrival":
              {
                   "longitude":long_arrival, 
                   "latitude": lat_arrival
                } 
            } 
            )        
    return json.dumps(out_data)

def process_flights(start_time: int, end_time: int) -> List[Dict[str, str]]:
    """Process flight information

    Call the opensky api; this will return List[Dict[str, sr]]
    
    Remember our final output, we want to return:
    List[Dict[str, str]]

    In the Dict, we'll have departure, arrival. So something like:
    Dict[departure, arrival]

    The shouldn't be duplicates in your json returned. 
    """
    newcall_api = call_api()
    output_data = []
    for flights in newcall_api:
        arrival_airport = flights["estarrival"]
        departure_airport = flights["estdeparture"]
        
        output_data.append(
        
              {
                   "departure_airport": arrival_airport, 
                   
                }
        )
    return json.dumps(output_data)

def index(*args, **kwargs):
    return HttpResponse("<h1>This is my test home view</h1>")

def flights(*args, **kwargs) -> str:
    """API for flight information

    your API will receive `start_time` and `end_time`
    Your API will return a json in the form of
    [
        {departure_airport: destination_airport},
        {departure_airport: destination_airport}
    ]

    Remember to add some logging so it is easy for you
    to troubleshoot. 

    Once you have your initial version, think about how you can
    scale your API. Also think about how you can speed it up
    """
    start_time = 3600 * 48
    end_time = int(time.time)
return process_flights(start_time, end_time)

    # return HttpResponse("This is my flight plan")

def cordinates(*args, **kwargs) -> str:
     """API for coordinate information

    your API will receive `start_time` and `end_time`
    Your API will return a json in the form of
    [
        {departure_airport: 
            {
                "longitude": long,
                "latitude": lat
            }
        },
        {departure_airport: 
            {
                "longitude": long,
                "latitude": lat
            }
        },
    ]

    Remember to add some logging so it is easy for you
    to troubleshoot. 

    Once you have your initial version, think about how you can
    scale your API. Also think about how you can speed it up
    """
    start_time = 3600 * 48
    end_time = int(time.time)
return process_coordinates(start_time, end_time)



  
    


