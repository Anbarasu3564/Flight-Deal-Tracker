import os
from pprint import pprint
from datetime import datetime
import requests
from dotenv import load_dotenv

load_dotenv()
# print(os.environ["AMADEUS_API_KEY"])

TOKEN_ENDPOINT = "https://test.api.amadeus.com/v1/security/oauth2/token"
IATA_ENDPOINT = "https://test.api.amadeus.com/v1/reference-data/locations"
FLIGHT_ENDPOINT = "https://test.api.amadeus.com/v2/shopping/flight-offers"


class FlightSearch:
    def __init__(self):
        self.api_key = os.environ["AMADEUS_API_KEY"]
        self.api_secret = os.environ["AMADEUS_SECRET"]
        self.token = self.get_new_token()

    def get_new_token(self):

        header = {
            "content-type": "application/x-www-form-urlencoded",
        }
        body = {
            "grant_type": "client_credentials",
            "client_id": self.api_key,
            "client_secret": self.api_secret,
        }
        response = requests.post(TOKEN_ENDPOINT, headers=header, data=body)
        # print(response.text)
        print(f"Your token is {response.json()['access_token']}")
        print(f"Your token expires in {response.json()['expires_in']} seconds")

        return response.json()["access_token"]

    def get_destination_codes(self, city_name):
        print(f"Using this token to get destination {self.token}")

        header = {"Authorization": f"Bearer {self.token}"}
        query = {
            "keyword": city_name,
            "subType": "CITY",
            # "max":2,
            # "include":"AIRPORTS",
        }

        response = requests.get(
            IATA_ENDPOINT,
            headers=header,
            params=query
        )
        print(f"Status code {response.status_code}. Airport IATA: {response.text}")
        try:
            code = response.json()["data"][0]['iataCode']
        except IndexError:
            print(f"IndexError: No airport code found for {city_name}.")
            return "N/A"
        except KeyError:
            print(f"KeyError: No airport code found for {city_name}.")
            return "Not Found"

        return code

    def check_flights(self, origin_city_code, destination_city_code, from_time, to_time,is_direct = True):
        # print(f"flight_search.check_flights() is using this token {self.token}")
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

        response = requests.get(FLIGHT_ENDPOINT,params=query,headers=header)
        # print(response.text)
        print(response.json())

        if response.status_code != 200:
            print(f"check_flights() response code: {response.status_code}")
            print("There was a problem with the flight search.\n"
                  "For details on status codes, check the API documentation:\n"
                  "https://developers.amadeus.com/self-service/category/flights/api-doc/flight-offers-search/api"
                  "-reference")
            print("Response body:", response.text)
            return None

        return response.json()










# f = FlightSearch()
# f.get_destination_codes("LONDON")
# f.check_flights("PAR","LON",from_time="2025-02-20",to_time="2025-03-20")