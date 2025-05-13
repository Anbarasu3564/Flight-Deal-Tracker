import time

import flight_data
from notification_manager import NotificationManager
from flight_data import find_cheapest_flight
from data_manager import DataManager
from datetime import datetime,timedelta
from flight_search import FlightSearch


ORIGIN_CITY_CODE = "LON"

data_manager = DataManager()
flight_search = FlightSearch()
notification_manager = NotificationManager()

sheet_data = data_manager.get_destination_data()

#
# print(sheet_data)

if sheet_data[0]["iataCode"] == "":
    for row in sheet_data:
        row["iataCode"] = flight_search.get_destination_codes(row["city"])
        time.sleep(2)
print(f"Sheet data: {sheet_data}")

data_manager.destination_data = sheet_data
data_manager.update_destination_code()



customer_data = data_manager.get_customer_emails()
# print(customer_data)
customer_email_list = [row["whatIsYourEmail?"] for row in customer_data]
# print(customer_email_list)






tomorrow = datetime.now() + timedelta(days=1)
six_months_from_today = datetime.now() + timedelta(days= 6 * 30)


for destination in sheet_data:
    # print(destination)
    print(f"finding flights for {destination["city"]}")
    flights = flight_search.check_flights(
        origin_city_code=ORIGIN_CITY_CODE,
        destination_city_code=destination["iataCode"],
        from_time=tomorrow,
        to_time=six_months_from_today
    )
    # print(f"flight search data : \n\n {flights} \n\n")
    cheapest_flight = flight_data.find_cheapest_flight(flights)
    print(f"{destination['city']}: £{cheapest_flight.price}")

    # ==================== Search for indirect flight if N/A ====================
    if cheapest_flight.price == "N/A":
        stopover_flights = flight_search.check_flights(
            origin_city_code=ORIGIN_CITY_CODE,
            destination_city_code=destination["iataCode"],
            from_time=tomorrow,
            to_time=six_months_from_today,
            is_direct=False,
        )
        # print(f"flight search data : \n\n {stopover_flights} \n\n")
        cheapest_flight = flight_data.find_cheapest_flight(stopover_flights)
        print(f"Cheapest indirect flight price is: £{cheapest_flight.price}")


    if cheapest_flight.price != "N/A" and cheapest_flight.price < destination["lowestPrice"]:
        # Customise the message depending on the number of stops
        if cheapest_flight.stops == 0:
            message = f"Low price alert! Only GBP {cheapest_flight.price} to fly direct "\
                      f"from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, "\
                      f"on {cheapest_flight.out_date} until {cheapest_flight.return_date}."
        else:
            message = f"Low price alert! Only GBP {cheapest_flight.price} to fly "\
                      f"from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, "\
                      f"with {cheapest_flight.stops} stop(s) "\
                      f"departing on {cheapest_flight.out_date} and returning on {cheapest_flight.return_date}."

        #send sms
        """notification_manager.send_sms(message_body=message)"""
        #send whatsup message
        """notification_manager.send_whatsup(message_body=message)"""

        #send email
        notification_manager.send_email(email_body=message,email_list=customer_email_list)



    time.sleep(2)
