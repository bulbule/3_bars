
import json
import sys
import os.path
from geopy.distance import great_circle
from geopy.geocoders import Nominatim


def load_data(filepath):
    """ Load a filepath with cyrilic letters """

    if not os.path.exists(filepath):
        return None
    with open(filepath, encoding='cp1251') as data_file:
        return json.loads(data_file.read())


def get_biggest_bars(bars):

    max_seats_bar = max(bars, key=lambda bar: bar['SeatsCount'])
    biggest_bars = [bar for bar in bars if bar[
        'SeatsCount'] == max_seats_bar['SeatsCount']]

    return biggest_bars


def get_smallest_bars(bars):

    min_seats_bar = min(bars, key=lambda bar: bar['SeatsCount'])
    smallest_bars = [bar for bar in bars if bar[
        'SeatsCount'] == min_seats_bar['SeatsCount']]

    return smallest_bars


def get_closest_bars(bars, longitude, latitude):

    my_coordinates = (longitude, latitude)

    distances = [
        great_circle(
            my_coordinates,
            (element['geoData']['coordinates'])).miles for element in bars]
        
    min_distance = min(distances)

    closest_bars = [bars[index] for index, dist in enumerate(distances)
                            if dist == min_distance]

    #closest_bars = [bars[index] for index in closest_bars_indexes]

    return closest_bars


if __name__ == '__main__':

    bars = load_data(sys.argv[1])
    print("Biggest bars:", *[bar['Name']
                             for bar in get_biggest_bars(bars)], sep='\n')
    print("Smallest bars:", *[bar['Name']
                              for bar in get_smallest_bars(bars)], sep='\n')
    geolocator = Nominatim()

    try:
        values = input(
            "Enter your longitude and latitude separated by a space:")
        location = [float(number) for number in values.strip().split()]
    except ValueError:
        print("Something different from numbers in your input was detected.")
    else:
        if len(location) != 2:
            raise IndexError("You failed to enter exactly two numbers.")
        else:
            print("Closest bars:",
                  *[bar['Name'] for bar in get_closest_bars(bars,
                                                           location[0],
                                                           location[1])],
                  sep='\n')
