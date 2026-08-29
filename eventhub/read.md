# EventHub

EventHub is a Django REST Framework backend API for a simplified event ticketing platform.

The application allows users to browse events, reserve seats, cancel reservations, and filter event or reservation data through REST API endpoints.

The project demonstrates Django ORM, Django REST Framework serializers, ModelViewSets, routers, validation, custom actions, middleware, and relational database design.

---

## Features

- Create and retrieve events
- Filter events by status
- Filter events by venue
- Create seat reservations
- Automatically deduct available seats after reservation
- Prevent overbooking
- Cancel reservations
- Restore seats after cancellation
- Filter reservations by event
- Count confirmed reservations for each event
- Log API request method, path, response status, and duration using custom middleware

---

## Technologies Used

- Python
- Django
- Django REST Framework
- SQLite
- Postman
- Git
- GitHub

---

## Project Structure

```text
eventhub/
├── manage.py
├── db.sqlite3
├── requirements.txt
├── README.md
├── screenshots/
│   ├── api_events_201.png
│   ├── api_events_status_upcoming_200.png
│   ├── events_1_200.png
│   ├── events_1_check_200.png
│   ├── reservations_confirmed_201.png
│   ├── reservations_exceeded_400.png
│   ├── reservations_1_cancel_200.png
│   └── reservations_event_id_1_200.png
│
├── eventhub/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
└── events/
    ├── migrations/
    │   ├── __init__.py
    │   └── 0001_initial.py
    ├── models.py
    ├── serializers.py
    ├── views.py
    ├── urls.py
    ├── middleware.py
    └── admin.py


Setup and Installation
1. Clone the repository
git clone <your-repository-url>
cd eventhub
2. Create a virtual environment
python -m venv venv
3. Activate the virtual environment
Windows
venv\Scripts\activate
4. Install dependencies
pip install -r requirements.txt
5. Apply migrations
python manage.py migrate
6. Run the development server
python manage.py runserver

The API will be available at:

http://127.0.0.1:8000/
Data Models
Event

An Event contains:

title
venue
date
total seats
available seats
status
creation timestamp

Supported event statuses:

upcoming
ongoing
completed
cancelled
Reservation

A Reservation belongs to one Event.

It contains:

event
attendee name
attendee email
seats reserved
reservation status
creation timestamp

Supported reservation statuses:

confirmed
cancelled

The relationship is:

Event 1 -------- Many Reservations
API Endpoints
Event Endpoints
Method	Endpoint	Description
GET	/api/events/	Get all events
POST	/api/events/	Create an event
GET	/api/events/{id}/	Get a specific event
PUT	/api/events/{id}/	Replace an event
PATCH	/api/events/{id}/	Partially update an event
DELETE	/api/events/{id}/	Delete an event
GET	/api/events/?status=upcoming	Filter events by status
GET	/api/events/?venue=Bangalore	Filter events by venue
Reservation Endpoints
Method	Endpoint	Description
GET	/api/reservations/	Get all reservations
POST	/api/reservations/	Create a reservation
GET	/api/reservations/{id}/	Get a specific reservation
GET	/api/reservations/?event_id=1	Filter reservations by event
POST	/api/reservations/{id}/cancel/	Cancel a reservation
Reservation Logic

When a reservation is created, EventHub checks:

At least one seat is being reserved.
The event is either upcoming or ongoing.
The requested number of seats does not exceed the available seats.

When validation succeeds:

available_seats
      ↓
subtract seats_reserved
      ↓
create Reservation

For example:

Available seats before reservation: 500
Seats reserved: 2
Available seats after reservation: 498

When the reservation is cancelled:

498 + 2 = 500

The reservation remains in the system for historical information, but its status changes to:

cancelled
Design Decision

One design decision in this project was to maintain available_seats directly on the Event model.

When a reservation is created, the reserved seats are deducted from available_seats. When that reservation is cancelled, the same seats are restored.

This makes seat availability easy to query and avoids calculating remaining seats from all reservations every time an event is requested.

Reservation creation and seat deduction are handled together inside the ReservationSerializer.create() method so that reservation-related business logic remains centralized.

For a production system with heavy concurrent booking traffic, database transactions and row-level locking could be introduced to provide stronger protection against race conditions.

Request Logging Middleware

The project includes custom middleware that logs every request.

The middleware records:

HTTP method
Request path
Response status
Request duration

Example:

GET /api/events/ - 200 - 0.02s
POST /api/reservations/ - 201 - 0.03s
POST /api/reservations/ - 400 - 0.02s
Postman API Testing
Event Creation — 201 Created

A new event was successfully created.

Event Status Filtering — 200 OK

Events were successfully filtered using:

GET /api/events/?status=upcoming

Event Retrieval — 200 OK

A specific event was retrieved using:

GET /api/events/1/

Required Reservation Tests
Successful Reservation — 201 Created

A reservation was successfully created and the event's available seats were reduced.

POST /api/reservations/

Overbooking Failure — 400 Bad Request

The API prevents users from reserving more seats than are currently available.

POST /api/reservations/

Expected status:

400 Bad Request

Successful Cancellation — 200 OK

A confirmed reservation was cancelled successfully.

POST /api/reservations/1/cancel/

The reservation status becomes:

cancelled

and its seats are restored to the Event.

Seat Restoration Verification — 200 OK

After cancellation, the Event endpoint was checked again to confirm that the reserved seats were restored.

Reservation Filtering — 200 OK

Reservations can be filtered using the event ID:

GET /api/reservations/?event_id=1

HTTP Status Codes Tested
Status	Meaning
200 OK	Request completed successfully
201 Created	Event or reservation successfully created
400 Bad Request	Validation failed, such as overbooking
404 Not Found	Requested resource does not exist