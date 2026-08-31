# Mechanic Shop API

A Flask REST API for managing a mechanic shop's customers, mechanics, service tickets, and parts inventory — built using the Application Factory pattern, SQLAlchemy ORM, Marshmallow schemas, token authentication, rate limiting, and caching.

## Tech Stack

- Python / Flask
- Flask-SQLAlchemy (MySQL)
- Flask-Marshmallow
- Flask-Limiter
- Flask-Caching
- python-jose (JWT authentication)
- python-dotenv
- flask-swagger / flask-swagger-ui (API documentation)

## Project Structure

mechanic-shop-api/
├── application/
│ ├── blueprints/
│ │ ├── customers/
│ │ ├── mechanics/
│ │ ├── service_ticket/
│ │ └── inventory/
│ ├── utils/
│ │ └── util.py
│ ├── static/
│ │ └── swagger.yaml
│ ├── extensions.py
│ ├── models.py
│ └── init.py
├── tests/
│ ├── test_customers.py
│ ├── test_mechanics.py
│ ├── test_service_tickets.py
│ └── test_inventory.py
├── app.py
├── config.py
├── .env
└── Mechanic Shop API.postman_collection.json

## Setup Instructions

1. Clone the repository:
   git clone <your-repo-url>
   cd mechanic-shop-api

2. Create and activate a virtual environment:
   python -m venv venv
   source venv/bin/activate

3. Install dependencies:
   pip install flask flask-sqlalchemy flask-marshmallow marshmallow-sqlalchemy mysql-connector-python flask-limiter flask-caching python-jose python-dotenv flask-swagger flask-swagger-ui

4. Create a MySQL database:

```sql
   CREATE DATABASE mechanic_shop_db;
```

5. Create a `.env` file in the project root with your own values:
   DB_PASSWORD=your_mysql_password
   SECRET_KEY=your_jwt_secret_key

6. Run the app:
   python app.py

The API will be available at `http://127.0.0.1:5000`.

## API Endpoints

### Customers (`/customers`)

- `POST /login` — log in with email/password, returns a JWT
- `POST /` — create a customer (rate limited to 3 per hour)
- `GET /` — get all customers (paginated: `?page=1&per_page=10`)
- `GET /<id>` — get a single customer
- `PUT /` — update the logged-in customer (requires token)
- `DELETE /` — delete the logged-in customer (requires token)
- `GET /my-tickets` — get service tickets for the logged-in customer (requires token)

### Mechanics (`/mechanics`)

- `POST /` — create a mechanic
- `GET /` — get all mechanics (cached for 60s)
- `PUT /<id>` — update a mechanic
- `DELETE /<id>` — delete a mechanic
- `GET /most-active` — get mechanics sorted by number of tickets worked, most active first

### Service Tickets (`/service-tickets`)

- `POST /` — create a service ticket
- `GET /` — get all service tickets
- `PUT /<ticket_id>/assign-mechanic/<mechanic_id>` — assign a mechanic to a ticket
- `PUT /<ticket_id>/remove-mechanic/<mechanic_id>` — remove a mechanic from a ticket
- `PUT /<ticket_id>/edit` — bulk add/remove mechanics via `add_ids`/`remove_ids`
- `PUT /<ticket_id>/add-part/<part_id>` — attach an inventory part to a ticket

### Inventory (`/inventory`)

- `POST /` — create a part
- `GET /` — get all parts
- `GET /<id>` — get a single part
- `PUT /<id>` — update a part
- `DELETE /<id>` — delete a part

## Authentication

Customers log in via `POST /customers/login` with `email` and `password`, receiving a JWT `auth_token` valid for 1 hour. Protected routes require the header:
Authorization: Bearer <token>

## API Documentation

Interactive API documentation is available at `http://127.0.0.1:5000/api/docs` once the app is running, powered by Swagger UI. It covers every endpoint's request/response shape, and includes an "Authorize" button for testing token-protected routes directly from the docs. The underlying spec lives at `application/static/swagger.yaml`.

## Testing

A full unit test suite covers every endpoint in the API, including negative test cases (validation errors, not-found responses, unauthorized access). Tests use Python's built-in `unittest` module against an isolated SQLite database, so they never touch production data.

To run the full suite:
python -m unittest discover tests

A Postman collection (`Mechanic Shop API.postman_collection.json`) is also included in this repo with example requests for every endpoint, organized by resource.
