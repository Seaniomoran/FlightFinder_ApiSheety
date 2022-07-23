from notification_manager import NotificationManager
from data_manager import DataManager
from flight_search import FlightSearch
from datetime import datetime, timedelta

# This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager
# classes to achieve the program requirement
#
data_manager = DataManager()
flight_search = FlightSearch()
notification_manager = NotificationManager()

ORIGIN_CITY = ["London"]
ORIGIN_CITY_IATA = flight_search.get_destination_info(ORIGIN_CITY)

sheet_data = data_manager.get_destination_data()

if sheet_data[0]["iataCode"] == "":
    city_names = [row["city"] for row in sheet_data]
    data_manager.city_codes = flight_search.get_destination_info(city_names)
    data_manager.update_iata_codes()
    sheet_data = data_manager.get_destination_data()

destinations = {
    data["iataCode"]: {
        "id": data["id"],
        "city": data["city"],
        "price": data["lowestPrice"]
    } for data in sheet_data}
# #
start_date = (datetime.now() + timedelta(1))
end_date = (datetime.now() + timedelta(days=6 * 30))

for location in destinations:
    flight = flight_search.check_flights(from_city_iata=ORIGIN_CITY_IATA,
                                         to_city_iata=location,
                                         from_date=start_date,
                                         to_date=end_date)

    if flight is None:
        continue

    if flight.price < destinations[location]["price"]:

        users = data_manager.get_customer_emails()
        emails = [row["email"] for row in users]
        names = [row["firstName"] for row in users]

        message = f"Low price alert! Only £{flight.price} to fly from {flight.origin_city}-{flight.origin_airport} to {flight.destination_city}-{flight.destination_airport}, from {flight.out_date} to {flight.return_date}."
        if flight.stop_overs > 0:
            message += f"\nFlight has {flight.stop_overs} stop over, via {flight.via_city}."

        link = f"https://www.google.co.uk/flights?hl=en#flt={flight.origin_airport}.{flight.destination_airport}.{flight.out_date}*{flight.destination_airport}.{flight.origin_airport}.{flight.return_date}"
        notification_manager.send_emails(emails, message, link)