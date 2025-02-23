import argparse
import json

import requests
from setup import BASE_URL, API_KEY


def get_coordinates_by_location(city_and_state, country='US'):
    # Make a request to the api endpoint at https://openweathermap.org/api/geocoding-api#direct_name
    try:
        response = requests.get(BASE_URL+'direct', params = {
            "q": f"{city_and_state},{country}",
            "limit": 1,
            "appid": API_KEY}
                )
        response.raise_for_status()
        if not response.json():
            print("No results found for your desired location, Please try a different location")
        else:
            data = response.json()[0]
            info = {
                "City": data["name"],
                "State": data['state'],
                "Country": data['country'],
                "Latitude": data['lat'],
                "Longitude": data['lon']
            }
            return info

    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def get_coordinates_by_zip(zip_code):
    # Make a request to the api endpoint at https://openweathermap.org/api/geocoding-api#direct_zip
    try:
        response = requests.get(BASE_URL+'zip', params={
            "zip": f"{zip_code},US",
            "appid": API_KEY
        })
        response.raise_for_status()
        if not response.json():
            print("No results found for your desired zip, Please try a different zip")
        else:
            data = response.json()
            zip_based_info = {
                "Zip Code": data["zip"],
                "Location Name": data['name'],
                "Country": data['country'],
                "Latitude": data['lat'],
                "Longitude": data['lon']
            }
            return zip_based_info

    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def parse_by_location_details(args):
    # Code to handle multiple location inputs
    city_state_pairs = [item.split(",") for item in args.city_and_state]

    for pair in city_state_pairs:
        if len(pair) == 2:
            result_by_location = get_coordinates_by_location(pair)
            # Parsing it into json for better readability during testing
            print(json.dumps({"message": "Location Details based on City and State", "data": result_by_location}))
        else:
            print(f"Invalid input format for city and state: {pair},  please refer to the --help option for expected input format")

def parse_by_zip_code(args):
    # Code to handle multiple zip inputs
    zip_pairs = [item.split(",") for item in args.zip_code]

    for pair in zip_pairs[0]:
        if isinstance(pair, str) and len(pair) == 5:
            result_by_zip = get_coordinates_by_zip(pair)
            # Parsing it into json for better readability during testing
            print(json.dumps({"message": "Location Details based on Zip", "data": result_by_zip}))
        else:
            print(f"Invalid input format for zip code: {pair},  please refer to the --help option for expected input format")


def main():
    parser = argparse.ArgumentParser(
        prog='My GeoCoding API CommandLine Program',
        usage='%(prog)s [options]',
        description="An application for displaying location information by using Geocoding API",
        epilog=
        """
            This utility expects Inputs will be given in the following formats: either
            City and State combination: “Madison, WI” \n OR
            Zip Codes: “12345”
            Note: The inputs given should be limited to the U.S only
        """
    )
    parser.add_argument("--city_and_state", nargs="+" ,action="extend",type=str, help="Please Enter the Name of your desired city and state separated by comma, e.g. 'Madison, WI'")
    parser.add_argument("--zip_code", nargs="+", action="extend", type=str, help="Please Enter the 5 digit zip code of your desired place in the U.S.A, e.g. '90034'")
    args = parser.parse_args()
    user_input = vars(args)

    # Conditional logic to determine which API endpoint to request data from depending on user's input
    if 'zip_code' in user_input and user_input['zip_code'] is not None:
        parse_by_zip_code(args)
    elif 'city_and_state' in user_input and user_input['city_and_state'] is not None:
        parse_by_location_details(args)
    else:
        print("Invalid input arguments, please see --help for options")

if __name__ == "__main__":
    main()
