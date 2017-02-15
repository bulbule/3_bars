
import json
import os.path
from geopy.distance import great_circle
from geopy.geocoders import Nominatim


def load_data(filepath):
    """ Load a filepath with cyrilic letters """

    if not os.path.exists(filepath):
        return None
    with open(filepath, encoding='cp1251') as data_file:
        data = json.loads(data_file.read())

    return data


def get_biggest_bar(data):
    """ Returns the list of names of the bars
    with the largest number of seats """

    seats = []
    biggest_bars = []

    for element in data:
        seats.append(element['SeatsCount'])

    # indexes of the bars in data with the largest number of seats
    biggest_bars_indexes = [index for index, max_value in enumerate(seats)
                            if max_value == max(seats)]
    for bar in biggest_bars_indexes:
        biggest_bars.append(data[bar]['Name'])

    return(biggest_bars)


def get_smallest_bar(data):
    """ Returns the list of names of the bars
    with the smallest number of seats
    """

    seats = []
    smallest_bars = []

    for element in data:
        seats.append(element['SeatsCount'])

    # indexes of the bars in data with the largest number of seats
    smallest_bars_indexes = [index for index, min_value in enumerate(seats)
                             if min_value == min(seats)]
    for bar in smallest_bars_indexes:
        smallest_bars.append(data[bar]['Name'])

    return(smallest_bars)


def get_closest_bar(data, longitude, latitude):
    """ Returns the list of names of the closest bars """

    my_coordinates = (longitude, latitude)
    distances = []
    closest_bars = []

    for element in data:
        bar_coordinates = tuple(element['geoData']['coordinates'])
        distances.append(great_circle(my_coordinates, bar_coordinates).miles)

    closest_bars_indexes = [index for index, min_dist in enumerate(distances)
                            if min_dist == min(distances)]
    for index in closest_bars_indexes:
        closest_bars.append(data[index]['Name'])

    return(closest_bars)


if __name__ == '__main__':

    data = load_data('data-2897-2016-11-23.json')
    print("Biggest bars:", ";".join(map(str, get_biggest_bar(data))))
    print("Smallest bars:", ", ".join(map(str, get_smallest_bar(data))))
    geolocator = Nominatim()

    try:
        values = input(
            "Enter your longitude and latitude separated by a space:")
        location = [float(number) for number in values.strip().split()]
    except ValueError:
        location = None
    if location is None:
        print("Something different from numbers in your input was detected.")
    else:
        if len(location) != 2:
            raise IndexError("You failed to enter exactly two numbers.")
        else:
            print("Closest bars:", ", ".join(
                map(str, get_closest_bar(data, location[0], location[1]))))
