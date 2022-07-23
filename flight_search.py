import os
import requests
from flight_data import FlightData
from pprint import pprint

TEQUILA_PRICES_ID = os.getenv("TEQUILA_PRICES_ID")
TEQUILA_PRICES_KEY = os.getenv("TEQUILA_PRICES_KEY")
TEQUILA_ENDPOINT = "http://tequila-api.kiwi.com"
headers = {"apikey": TEQUILA_PRICES_KEY}


class FlightSearch:
    #This class is responsible for talking to the Flight Search API.

    def __init__(self):
        self.city_codes = []

    def get_destination_info(self, city_names):

        location_endpoint = f"{TEQUILA_ENDPOINT}/locations/query"
        for city in city_names:
            query = {
                "term": city,
                "location_types": "city"
            }
            response = requests.get(url=location_endpoint, headers=headers, params=query)
            data = response.json()["locations"]
            code = data[0]["code"]
            self.city_codes.append(code)

        return self.city_codes

    def check_flights(self, from_city_iata, to_city_iata, from_date, to_date):
        query = {
            "fly_from": from_city_iata,
            "fly_to": to_city_iata,
            "date_from": from_date.strftime('%d/%m/%Y'),
            "date_to": to_date.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 30,
            "flight_type": "",
            "one_for_city": 1,
            "max_stopovers": 0,
            "curr": "USD"
        }

        response = requests.get(url=f"{TEQUILA_ENDPOINT}/v2/search",
                                headers=headers,
                                params=query)
        pprint(response.json())

        try:
            data = response.json()["data"][0]
        except IndexError:
            query["max_stopovers"] = 1
            response = requests.get(url=f"{TEQUILA_ENDPOINT}/v2/search", headers=headers, params=query)
            dict = response.json()
            try:
                data = dict["data"][0]
            except IndexError:
                return None
            else:
                flight_data = FlightData(
                    price=data["price"],
                    origin_city=data["route"][0]["cityFrom"],
                    origin_airport=data["route"][0]["flyFrom"],
                    destination_city=data["route"][1]["cityTo"],
                    destination_airport=data["route"][1]["flyTo"],
                    out_date=data["route"][0]["local_departure"].split("T")[0],
                    return_date=data["route"][1]["local_departure"].split("T")[0],
                    stop_overs=1,
                    via_city=data["route"][0]["cityTo"]
                )
                return flight_data
        else:
            flight_data = FlightData(
                price=data["price"],
                origin_city=data["route"][0]["cityFrom"],
                origin_airport=data["route"][0]["flyFrom"],
                destination_city=data["route"][0]["cityTo"],
                destination_airport=data["route"][0]["flyTo"],
                out_date=data["route"][0]["local_departure"].split("T")[0],
                return_date=data["route"][1]["local_departure"].split("T")[0]
            )
            print(f"{flight_data.destination_city}: £{flight_data.price}")
            return flight_data
