import requests
import os
# from pprint import pprint

SHEETY_PRICES_ENDPOINT = os.getenv("SHEETY_PRICES_ENDPOINT")
SHEETY_PRICES_TOKEN = os.getenv("SHEETY_PRICES_TOKEN")
customers_endpoint = f"{(os.getenv('SHEETY_PRICES_ENDPOINT')).replace('prices', 'users')}"
header = {
    "Authorization": f"Bearer {SHEETY_PRICES_TOKEN}"
}


class DataManager:
    #This class is responsible for talking to the Google Sheet.

    def __init__(self):
        self.destination_data = {}
        self.customer_data = {}


    def get_destination_data(self):
        response = requests.get(url=SHEETY_PRICES_ENDPOINT, headers=header)
        data = response.json()
        #pprint(data)
        self.destination_data = data["prices"]
        return self.destination_data

    def update_iata_codes(self):
        for city in self.destination_data:
            query = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(url=f"{SHEETY_PRICES_ENDPOINT}/{city['id']}", headers=header,
                                    json=query)
            print(response.text)

    def add_user(self, first_name, last_name, email):
        query = {
            "user": {
                "firstName": first_name,
                "lastName": last_name,
                "email": email
            }
        }

        response = requests.post(url=customers_endpoint, json=query, headers=header)
        return print(response.text)

    def get_customer_emails(self):
        response = requests.get(url=customers_endpoint, headers=header)
        data = response.json()
        self.customer_data = data["users"]
        return self.customer_data
