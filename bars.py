# -*- coding: utf-8 -*-
"""
Created on Tue Feb 14 11:58:21 2017

@author: anyya
"""

import json
from geopy.distance import great_circle
from geopy.geocoders import Nominatim


def load_data(filepath):

    """ Load a filepath with cyrilic letters """
    
    with open(filepath, encoding='cp1251') as data_file:
        data = json.loads(data_file.read())
        
    return data


def get_biggest_bar(data):

    """ Returns the list of names of the bars 
    with the largest number of seats """
    
    seats = []
    biggest_bars = []
    
    for el in data:
        seats.append(el['SeatsCount'])

    # indexes of the bars in data with the largest number of seats
    biggest_bars_indexes = [i for i, j in enumerate(seats) if j == max(seats)]
    for bar in biggest_bars_indexes:
        biggest_bars.append(data[bar]['Name'])
    
    return(biggest_bars)
    
        
def get_smallest_bar(data):
    
    """ Returns the list of names of the bars
    with the smallest number of seats
    """
    
    seats = []
    smallest_bars = []
    
    for el in data:
        seats.append(el['SeatsCount'])
    
    # indexes of the bars in data with the largest number of seats
    smallest_bars_indexes = [i for i, j in enumerate(seats) if j == min(seats)]
    for bar in smallest_bars_indexes:
        smallest_bars.append(data[bar]['Name'])
        
    return(smallest_bars)


def get_closest_bar(data, longitude, latitude):
    
    """ Returns the list of names of the closest bars """
    
    my_coordinates = (longitude, latitude)
    distances = []
    closest_bars = []
    
    for el in data:
        bar_coordinates = tuple(el['geoData']['coordinates'])
        distances.append(great_circle(my_coordinates, bar_coordinates).miles)
        
    closest_bars_indexes = [i for i, j in enumerate(distances)
                            if j == min(distances)]
    for index in closest_bars_indexes:
        closest_bars.append(data[index]['Name'])
    
    return(closest_bars)


if __name__ == '__main__':
    
    data = load_data('data-2897-2016-11-23.json')
    print("Biggest bars:", ";".join(map(str, get_biggest_bar(data))))
    print("Smallest bars:", ", ".join(map(str, get_smallest_bar(data))))
    geolocator = Nominatim()
    value = input("Enter your gps coordinates:")
    if not value:   # if nothing is entered the location of MIPT is chosen
        location = (geolocator.geocode("MIPT").longitude,
                    geolocator.geocode("MIPT").latitude)
    else:
        location = [float(i) for i in value.strip().split()]
    print("Closest bars:",
          ", ".join(map(str, get_closest_bar(data, location[0], location[1]))))
