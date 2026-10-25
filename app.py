database = [
    {
        "route_id": "R101",
        "departure_city": "Karachi",
        "destination_city": "Hyderabad",
        "departure_time": "08:00 AM",
        "ticket_price": 1200,
        "total_seats": 40,
        "available_seats": 40
    },
    {
        "route_id": "R102",
        "departure_city": "Karachi",
        "destination_city": "Sukkur",
        "departure_time": "10:00 AM",
        "ticket_price": 2000,
        "total_seats": 35,
        "available_seats": 35
    },
    {
        "route_id": "R103",
        "departure_city": "Hyderabad",
        "destination_city": "Lahore",
        "departure_time": "09:00 PM",
        "ticket_price": 4500,
        "total_seats": 30,
        "available_seats": 30
    }
]



bookings = []



def view_routes():
    print("\n----------- AVAILABLE BUS ROUTES -----------")

    print("-------------------------------------------")
    print("Route ID:", database["route_id"])
    print("From:", database["departure_city"])
    print("To:", database["destination_city"])
    print("Departure:", database["departure_time"])
    print("Ticket Price: Rs.", database["ticket_price"])
    print("Available Seats:", database["available_seats"])


def route_scheduler():
    print("\n========== BUS ROUTE SCHEDULE ==========")

    cities = []

    for route in database:
        city = route["departure_city"]

        if city not in cities:
            cities.append(city)

    for city in cities:
        print(f"\n{city.upper()}:")

        for route in database:
            if route["departure_city"] == city:
                print(
                    f"    {route['route_id']} -> "
                    f"{route['destination_city'].upper()} | "
                    f"{route['departure_time']}"
                )


def create_booking():
    print("CREATE BOOKING")

    name = input("Enter Your Name: ")
    age = int(input("Enter Your Age: "))
    booked_seats = int(input("How Many Passengers Are Traveliing: "))
    route_id = input("Enter Route ID: ").strip().upper()
    if database["route_id"] == route_id:
            booked_route = database
    else:
        print("Route Id Does Not Exist")

    if booked_route["available_seats"] == 0:
        print("Sorry No seats available.")

        
    # Get number of passengers
    try:
        passengers = int(input("Enter Number of Passengers: "))
    except ValueError:
        print("Please enter a valid whole number!")
        return

    if passengers <= 0:
        print("Number of passengers must be at least 1!")
        return

    if passengers > booked_seats["available_seats"]:
        print("Sorry! Not enough seats available.")
        return

    passenger_names = []

    for i in range(passengers):
        while True:
            name = input(
                f"Enter name of passenger {i + 1}: "
            ).strip()

            if name:
                passenger_names.append(name)
                break

            print("Name cannot be empty. Please try again.")


        bookings.append(booking)

        booked_route["available_seats"] -= booked_seats


        print("\nBooking Successful!")
        print("Booking ID:", booking_counter)
        print("Passenger:", name)
        print(
            "Route:",
            booked_route["departure_city"],
            "to",
            booked_route["destination_city"]
        )
        print("Ticket Price: Rs.", booked_route["ticket_price"])

        booking_counter += 1

    booking = {
        "booking_id": booking_counter,
        "name": name,
        "age": age,
        "route_id": booked_route["route_id"],
        "departure_city": booked_route["departure_city"],
        "destination_city": booked_route["destination_city"],
        "ticket_price": booked_route["ticket_price"],
        "status": "Confirmed"
    }

def cancel_booking():
    print("\n========== CANCEL BOOKING ==========")

    try:
        booking_id = int(input("Enter Booking ID: "))
    except ValueError:
        print("Please enter a valid numeric Booking ID.")
        return

    for booking in bookings:
        if booking["booking_id"] == booking_id:

            if booking["status"] == "Cancelled":
                print("This booking is already cancelled.")
                return

            booking["status"] = "Cancelled"

            # Restore the seat to the correct route
            for route in database:
                if route["route_id"] == booking["route_id"]:
                    route["available_seats"] += 1
                    break

            print("Booking cancelled successfully!")
            print("Booking ID:", booking_id)
            return

    print("Booking ID not found!")




def search_route():
    route_id = input("Enter Route ID: ").strip().upper()

    for route in database:
        if route["route_id"] == route_id:
            print("\n========== ROUTE FOUND ==========")
            print("Route ID:", route["route_id"])
            print("From:", route["departure_city"])
            print("To:", route["destination_city"])
            print("Departure Time:", route["departure_time"])
            print("Ticket Price: Rs.", route["ticket_price"])
            print("Available Seats:", route["available_seats"])
            return route

    print("Route not found!")
    return None



def booking_report():
    print("\n========== BOOKING REPORT ==========")

    if len(bookings) == 0:
        print("No bookings found.")
        return

    total_bookings = len(bookings)
    confirmed_bookings = 0
    cancelled_bookings = 0
    total_revenue = 0

    for booking in bookings:
        print("-------------------------------------------")
        print("Booking ID:", booking["booking_id"])
        print("Passenger:", booking["passenger_name"])
        print("Route ID:", booking["route_id"])
        print(
            "Journey:",
            booking["departure_city"],
            "to",
            booking["destination_city"]
        )
        print("Fare: Rs.", booking["ticket_price"])
        print("Status:", booking["status"])

        if booking["status"] == "Confirmed":
            confirmed_bookings += 1
            total_revenue += booking["ticket_price"]
        else:
            cancelled_bookings += 1

    print("\n========== REPORT SUMMARY ==========")
    print("Total Bookings Created:", total_bookings)
    print("Confirmed Bookings:", confirmed_bookings)
    print("Cancelled Bookings:", cancelled_bookings)
    print("Total Confirmed Fare: Rs.", total_revenue)


def exit_app():
    print("\nThank you for using Smart Bus Tracking System!")
    print("Goodbye!")


def main():
    while True:
        print("\n==========================================")
        print("       SMART BUS TRACKING SYSTEM")
        print("==========================================")
        print("1. View Available Routes")
        print("2. Search Route by ID")
        print("3. Create Booking")
        print("4. Cancel Booking")
        print("5. Generate Booking Report")
        print("6. View Route Scheduler")
        print("7. Exit")
        print("==========================================")

        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            view_routes()

        elif choice == "2":
            search_route()

        elif choice == "3":
            create_booking()

        elif choice == "4":
            cancel_booking()

        elif choice == "5":
            booking_report()

        elif choice == "5":
            route_scheduler()

        elif choice == "6":
            exit_app()
            break

        else:
            print("Invalid choice! Please enter a number from 1 to 6.")


main()