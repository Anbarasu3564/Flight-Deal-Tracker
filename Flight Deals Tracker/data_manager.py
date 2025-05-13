import requests
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth
import os
from pprint import pprint

#loading all the .env data
load_dotenv()



class DataManager:
    def __init__(self):
        self.sheety_endpoint_sheet1 = os.environ["SHEETY_ENDPOINT_SHEET1"]
        self.sheety_endpoint_users = os.environ["SHEETY_ENDPOINT_USERS"]
        self.username = os.environ["SHEETY_USERNAME"]
        self.password = os.environ["SHEETY_PASSWORD"]
        self.authorization = HTTPBasicAuth(self.username, self.password)
        self.destination_data = {}
        self.customer_data = {}

    def get_destination_data(self):
        #getting the all the data from the google sheet

        response = requests.get(self.sheety_endpoint_sheet1, auth=self.authorization)
        # print(response.text)

        data = response.json()

        # pprint(data)

        self.destination_data = data["sheet1"]
        # print(self.destination_data)


        return self.destination_data

    def update_destination_code(self):
        for city in self.destination_data:
            new_data = {
                "sheet1": {
                    "iataCode": city["iataCode"],
                }
            }

            response = requests.put(f"{self.sheety_endpoint_sheet1}/{city['id']}",
                                    json=new_data,
                                    auth=self.authorization)

            print(response.text)

    def get_customer_emails(self):
        response = requests.get(self.sheety_endpoint_users,auth=self.authorization)
        print(response.text)
        self.customer_data = response.json()["users"]
        # print(response.json())
        return self.customer_data
#
# c = DataManager()
# c.get_customer_emails()
