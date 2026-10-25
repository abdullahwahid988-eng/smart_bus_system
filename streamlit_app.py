import streamlit as st
import pandas as pd

# -----------------------------
# Smart Bus Tracking System
# Streamlit UI
# -----------------------------
st.set_page_config(
    page_title="Smart Bus Tracking System",
    page_icon="🚌",
    layout="wide",
)

# In-memory demo data (resets when the app process restarts)
if "routes" not in st.session_state:
    st.session_state.routes = [
        {
            "route_id": "R101",
            "departure_city": "Karachi",
            "destination_city": "Hyderabad",
            "departure_time": "08:00 AM",
            "ticket_price": 1200,
            "total_seats": 40,
            "available_seats": 40,
        },
        {
            "route_id": "R102",
            "departure_city": "Karachi",
            "destination_city": "Sukkur",
            "departure_time": "10:00 AM",
            "ticket_price": 2000,
            "total_seats": 35,
            "available_seats": 35,
        },
        {
            "route_id": "R103",
            "departure_city": "Hyderabad",
            "destination_city": "Lahore",
            "departure_time": "09:00 PM",
            "ticket_price": 4500,
            "total_seats": 30,
            "available_seats": 30,
        },
    ]

if "bookings" not in st.session_state:
    st.session_state.bookings = []
if "next_booking_id" not in st.session_state:
    st.session_state.next_booking_id = 1

routes = st.session_state.routes
bookings = st.session_state.bookings


def money(amount):
    return f"Rs. {amount:,.0f}"


def route_by_id(route_id):
    return next((r for r in routes if r["route_id"] == route_id), None)


# Sidebar navigation
st.sidebar.title("🚌 Smart Bus")
st.sidebar.caption("Tracking & Booking System")
page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Available Routes",
        "Search Route",
        "Create Booking",
        "Cancel Booking",
        "Booking Report",
        "Route Scheduler",
    ],
)
st.sidebar.divider()
st.sidebar.info("Demo application. Data is kept in session memory and may reset.")

# Header
st.title("🚌 Smart Bus Tracking System")
st.caption("Manage bus routes, passenger bookings, cancellations, and reports.")
st.divider()

if page == "Dashboard":
    confirmed = sum(b["status"] == "Confirmed" for b in bookings)
    cancelled = sum(b["status"] == "Cancelled" for b in bookings)
    revenue = sum(
        b["ticket_price"] * b["passengers"]
        for b in bookings
        if b["status"] == "Confirmed"
    )
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Available Routes", len(routes))
    c2.metric("Confirmed Bookings", confirmed)
    c3.metric("Cancelled Bookings", cancelled)
    c4.metric("Confirmed Revenue", money(revenue))

    st.subheader("Available routes")
    st.dataframe(
        pd.DataFrame(
            [
                {
                    "Route ID": r["route_id"],
                    "From": r["departure_city"],
                    "To": r["destination_city"],
                    "Departure": r["departure_time"],
                    "Fare": money(r["ticket_price"]),
                    "Seats left": r["available_seats"],
                }
                for r in routes
            ]
        ),
        use_container_width=True,
        hide_index=True,
    )

elif page == "Available Routes":
    st.subheader("🗺️ Available Bus Routes")
    st.write("Check destinations, departure times, ticket prices, and seat availability.")
    st.dataframe(
        pd.DataFrame(
            [
                {
                    "Route ID": r["route_id"],
                    "From": r["departure_city"],
                    "To": r["destination_city"],
                    "Departure": r["departure_time"],
                    "Ticket Price": money(r["ticket_price"]),
                    "Total Seats": r["total_seats"],
                    "Available Seats": r["available_seats"],
                }
                for r in routes
            ]
        ),
        use_container_width=True,
        hide_index=True,
    )

elif page == "Search Route":
    st.subheader("🔎 Search Route by ID")
    with st.form("search_route_form"):
        route_id = st.text_input("Route ID", placeholder="e.g. R101").strip().upper()
        submitted = st.form_submit_button("Search route", use_container_width=True)
    if submitted:
        route = route_by_id(route_id)
        if route:
            st.success("Route found")
            a, b, c = st.columns(3)
            a.metric("Ticket Price", money(route["ticket_price"]))
            b.metric("Available Seats", route["available_seats"])
            c.metric("Departure", route["departure_time"])
            st.write(f"**Route:** {route['route_id']} — {route['departure_city']} to {route['destination_city']}")
        else:
            st.error("Route ID not found. Please check the ID and try again.")

elif page == "Create Booking":
    st.subheader("🎫 Create a Booking")
    available_routes = [r for r in routes if r["available_seats"] > 0]
    if not available_routes:
        st.warning("No routes currently have available seats.")
    else:
        route_options = {
            f'{r["route_id"]} | {r["departure_city"]} → {r["destination_city"]} | {r["departure_time"]} | {money(r["ticket_price"])}': r["route_id"]
            for r in available_routes
        }
        with st.form("create_booking_form"):
            passenger_name = st.text_input("Lead passenger name")
            age = st.number_input("Lead passenger age", min_value=1, max_value=120, value=18, step=1)
            selected_label = st.selectbox("Select route", list(route_options.keys()))
            passengers = st.number_input(
                "Number of passengers",
                min_value=1,
                max_value=max(1, route_by_id(route_options[selected_label])["available_seats"]),
                value=1,
                step=1,
            )
            submitted = st.form_submit_button("Confirm booking", use_container_width=True)

        if submitted:
            route = route_by_id(route_options[selected_label])
            passenger_name = passenger_name.strip()
            if not passenger_name:
                st.error("Please enter the lead passenger's name.")
            elif passengers > route["available_seats"]:
                st.error("Not enough seats available for this route.")
            else:
                booking_id = st.session_state.next_booking_id
                booking = {
                    "booking_id": booking_id,
                    "name": passenger_name,
                    "age": int(age),
                    "route_id": route["route_id"],
                    "departure_city": route["departure_city"],
                    "destination_city": route["destination_city"],
                    "ticket_price": route["ticket_price"],
                    "passengers": int(passengers),
                    "status": "Confirmed",
                }
                bookings.append(booking)
                route["available_seats"] -= int(passengers)
                st.session_state.next_booking_id += 1
                st.success(f"Booking confirmed! Your booking ID is **{booking_id}**.")
                st.write(f"**Journey:** {route['departure_city']} → {route['destination_city']}")
                st.write(f"**Passengers:** {int(passengers)}")
                st.write(f"**Total fare:** {money(route['ticket_price'] * int(passengers))}")

elif page == "Cancel Booking":
    st.subheader("❌ Cancel a Booking")
    active_bookings = [b for b in bookings if b["status"] == "Confirmed"]
    if not active_bookings:
        st.info("There are no confirmed bookings to cancel.")
    else:
        booking_options = {
            f'Booking #{b["booking_id"]} — {b["name"]} ({b["route_id"]})': b["booking_id"]
            for b in active_bookings
        }
        with st.form("cancel_booking_form"):
            selected_booking = st.selectbox("Select booking", list(booking_options.keys()))
            submitted = st.form_submit_button("Cancel booking", use_container_width=True)
        if submitted:
            booking_id = booking_options[selected_booking]
            booking = next(b for b in bookings if b["booking_id"] == booking_id)
            booking["status"] = "Cancelled"
            route = route_by_id(booking["route_id"])
            if route:
                route["available_seats"] = min(
                    route["total_seats"],
                    route["available_seats"] + booking["passengers"],
                )
            st.success(f"Booking #{booking_id} has been cancelled and its seats restored.")

elif page == "Booking Report":
    st.subheader("📊 Booking Report")
    if not bookings:
        st.info("No bookings have been created yet.")
    else:
        confirmed = [b for b in bookings if b["status"] == "Confirmed"]
        cancelled = [b for b in bookings if b["status"] == "Cancelled"]
        revenue = sum(b["ticket_price"] * b["passengers"] for b in confirmed)
        c1, c2, c3 = st.columns(3)
        c1.metric("Total bookings", len(bookings))
        c2.metric("Confirmed", len(confirmed))
        c3.metric("Cancelled", len(cancelled))
        st.metric("Total confirmed fare", money(revenue))
        st.dataframe(
            pd.DataFrame(
                [
                    {
                        "Booking ID": b["booking_id"],
                        "Passenger": b["name"],
                        "Age": b["age"],
                        "Route ID": b["route_id"],
                        "Journey": f'{b["departure_city"]} → {b["destination_city"]}',
                        "Passengers": b["passengers"],
                        "Fare per passenger": money(b["ticket_price"]),
                        "Total fare": money(b["ticket_price"] * b["passengers"]),
                        "Status": b["status"],
                    }
                    for b in bookings
                ]
            ),
            use_container_width=True,
            hide_index=True,
        )
        csv = pd.DataFrame(bookings).to_csv(index=False).encode("utf-8")
        st.download_button("Download report as CSV", data=csv, file_name="booking_report.csv", mime="text/csv")

elif page == "Route Scheduler":
    st.subheader("🕒 Bus Route Scheduler")
    cities = list(dict.fromkeys(r["departure_city"] for r in routes))
    for city in cities:
        city_routes = [r for r in routes if r["departure_city"] == city]
        with st.expander(f"📍 {city}", expanded=True):
            for route in city_routes:
                st.write(
                    f'**{route["route_id"]}** → {route["destination_city"]}  |  '
                    f'{route["departure_time"]}  |  {money(route["ticket_price"])}'
                )
