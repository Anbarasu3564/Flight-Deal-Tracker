class FlightData:
    def __init__(self,price,origin_airport,destination_airport,out_date,return_date,stops):
        self.price =price
        self.origin_airport = origin_airport
        self.destination_airport = destination_airport
        self.out_date = out_date
        self.return_date = return_date
        self.stops = stops


def find_cheapest_flight(data):

    if data is None or not data["data"]:
        return FlightData("N/A","N/A","N/A","N/A","N/A","N/A")

    flight = data["data"][0]
    lowest_price = float(flight["price"]["grandTotal"])
    # lowest_price = 2.1 #test code

    origin = flight["itineraries"][0]["segments"][0]["departure"]["iataCode"]
    # A flight with 2 segments will have 1 stop
    nr_stops = len(flight["itineraries"][0]["segments"]) - 1
    destination = flight["itineraries"][0]["segments"][0]["arrival"]["iataCode"]

    out_date = flight["itineraries"][0]["segments"][0]["departure"]["at"].split("T")[0]
    return_date = flight["itineraries"][1]["segments"][0]["departure"]["at"].split("T")[0]

    cheapest_flight = FlightData(lowest_price,origin,destination,out_date,return_date,nr_stops)

    for flight in data["data"]:
        price = float(flight["price"]["grandTotal"])
        if price < lowest_price:
            origin = flight["itineraries"][0]["segments"][0]["departure"]["iataCode"]
            destination = flight["itineraries"][0]["segments"][0]["arrival"]["iataCode"]
            out_date = flight["itineraries"][0]["segments"][0]["departure"]["at"].split("T")[0]
            return_date = flight["itineraries"][1]["segments"][0]["departure"]["at"].split("T")[0]
            cheapest_flight = FlightData(lowest_price, origin, destination, out_date, return_date,nr_stops)
            print(f"Lowest price to {destination} is £{lowest_price}")

    return cheapest_flight