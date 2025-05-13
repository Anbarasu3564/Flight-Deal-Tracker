import os
from data_manager import DataManager
from flight_data import FlightData, find_cheapest_flight
from flight_search import FlightSearch
from notification_manager import NotificationManager
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()


def main():
    """
    This function runs the flight deal tracker system. It fetches destination data from the Google Sheet,
    checks for cheap flights for those destinations, and sends notifications to users if there's a deal.
    """

    # Initialize all the classes needed for the process
    data_manager = DataManager()
    flight_search = FlightSearch()
    notification_manager = NotificationManager()

    # Step 1: Get destination data (city names and IATA codes) from the Google Sheet
    destinations = data_manager.get_destination_data()

    # Step 2: Check for available flight deals for each destination
    for destination in destinations:
        city_name = destination["city"]
        destination_code = destination["iataCode"]

        # If IATA code is not present, fetch it using the flight search API
        if destination_code == "":
            destination_code = flight_search.get_destination_codes(city_name)
            destination["iataCode"] = destination_code
            data_manager.update_destination_code()  # Update IATA code in the Google Sheet

        # Step 3: Get flight details for the destination
        flight_data = flight_search.check_flights(
            "LON", destination_code, "2025-06-01", "2025-06-30", is_direct=True
        )

        # Step 4: Process flight data to find the cheapest option
        cheapest_flight = find_cheapest_flight(flight_data)

        # If a valid flight is found and it's cheaper than the set price, send notifications
        if cheapest_flight.price != "N/A" and float(cheapest_flight.price) < 200:
            message_body = f"Low price alert! Only £{cheapest_flight.price} to {city_name} from London. " \
                           f"Departure: {cheapest_flight.out_date}, Return: {cheapest_flight.return_date}. " \
                           f"Stops: {cheapest_flight.stops}."

            # Get customer emails to send notifications
            customers = data_manager.get_customer_emails()
            emails = [customer["email"] for customer in customers]

            # Send the email notifications
            notification_manager.send_email(message_body, emails)

            # Optionally, send SMS or WhatsApp alerts too (depending on your setup)
            notification_manager.send_sms(message_body)
            notification_manager.send_whatsup(message_body)


if __name__ == "__main__":
    main()
