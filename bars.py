
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


def get_biggest_bar(bars):
    """ Returns the list of names of the bars
    with the largest number of seats """

    seats = max(bar["SeatsCount"] for bar in bars)
    biggest_bars = [bar['Name']
                    for bar in bars if bar['SeatsCount'] == seats]

    return biggest_bars


def get_smallest_bar(bars):
    """ Returns the list of names of the bars
    with the smallest number of seats
    """

    seats = min(bar["SeatsCount"] for bar in bars)
    smallest_bars = [bar['Name']
                     for bar in bars if bar['SeatsCount'] == seats]

    return smallest_bars


def get_closest_bar(bars, longitude, latitude):
    """ Returns the list of names of the closest bars """

    my_coordinates = (longitude, latitude)

    distances = [
        great_circle(
            my_coordinates,
            (element['geoData']['coordinates'])).miles for element in bars]

    closest_bars_indexes = [index for index, min_dist in enumerate(distances)
                            if min_dist == min(distances)]

    closest_bars = [bars[index]['Name'] for index in closest_bars_indexes]

    return closest_bars


if __name__ == '__main__':

    bars = load_data(sys.argv[1])
    print("Biggest bars:", ";".join(map(str, get_biggest_bar(bars))))
    print("Smallest bars:", ", ".join(map(str, get_smallest_bar(bars))))
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
            print("Closest bars:", ", ".join(
                map(str, get_closest_bar(bars,
                                         location[0], location[1]))))
