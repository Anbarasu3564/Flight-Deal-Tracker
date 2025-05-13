import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

TOKEN_ENDPOINT = "https://test.api.amadeus.com/v1/security/oauth2/token"
IATA_ENDPOINT = "https://test.api.amadeus.com/v1/reference-data/locations"
FLIGHT_ENDPOINT = "https://test.api.amadeus.com/v2/shopping/flight-offers"

class FlightSearch:
    """
    This class interacts with the Amadeus API to search for flights and
    retrieve destination codes for cities.
    """

    def __init__(self):
        self.api_key = os.environ["AMADEUS_API_KEY"]
        self.api_secret = os.environ["AMADEUS_SECRET"]
        self.token = self.get_new_token()

    def get_new_token(self):
        """
        Retrieves a new token from the Amadeus API.
        """
        header = {"content-type": "application/x-www-form-urlencoded"}
        body = {
            "grant_type": "client_credentials",
            "client_id": self.api_key,
            "client_secret": self.api_secret,
        }
        response = requests.post(TOKEN_ENDPOINT, headers=header, data=body)
        print(f"Your token is {response.json()['access_token']}")
        return response.json()["access_token"]

    def get_destination_codes(self, city_name):
        """
        Retrieves the IATA code for a given city from the Amadeus API.
        """
        header = {"Authorization": f"Bearer {self.token}"}
        query = {
            "keyword": city_name,
            "subType": "CITY",
        }
        response = requests.get(IATA_ENDPOINT, headers=header, params=query)

        try:
            code = response.json()["data"][0]['iataCode']
        except IndexError:
            print(f"Error: No airport code found for {city_name}.")
            return "N/A"
        except KeyError:
            print(f"Error: No airport code found for {city_name}.")
            return "Not Found"

        return code

    def check_flights(self, origin_city_code, destination_city_code, from_time, to_time, is_direct=True):
        """
        Checks available flights between origin and destination with the given dates.
        """
        header = {"Authorization": f"Bearer {self.token}"}
        query = {
            "originLocationCode": origin_city_code,
            "destinationLocationCode": destination_city_code,
            "departureDate": from_time.strftime("%Y-%m-%d"),
            "returnDate": to_time.strftime("%Y-%m-%d"),
            "adults": 1,
            "nonStop": "true" if is_direct else "false",
            "currencyCode": "GBP",
            "max": "1",
        }

        response = requests.get(FLIGHT_ENDPOINT, params=query, headers=header)

        if response.status_code != 200:
            print(f"Error: {response.status_code} - {response.text}")
            return None

        return response.json()
