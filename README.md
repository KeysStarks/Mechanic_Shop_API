# Mechanic Shop API

A Flask REST API for managing a mechanic shop's customers, mechanics, and service tickets — built using the Application Factory pattern, SQLAlchemy ORM, and Marshmallow schemas.

## Tech Stack

- Python / Flask
- Flask-SQLAlchemy (MySQL)
- Flask-Marshmallow
- MySQL

## Project Structure

mechanic-shop-api/
├── application/
│ ├── blueprints/
│ │ ├── customers/
│ │ ├── mechanics/
│ │ └── service_ticket/
│ ├── extensions.py
│ ├── models.py
│ └── init.py
├── app.py
├── config.py
└── Mechanic Shop API.postman_collection.json

## Setup Instructions

1. Clone the repository:
   git clone <your-repo-url>
   cd mechanic-shop-api

2. Create and activate a virtual environment:
   python -m venv venv
   source venv/bin/activate

3. Install dependencies:
   pip install flask flask-sqlalchemy flask-marshmallow marshmallow-sqlalchemy mysql-connector-python

4. Create a MySQL database:

```sql
   CREATE DATABASE mechanic_shop_db;
```

5. Update `config.py` with your own MySQL username and password.

6. Run the app:
   python app.py

The API will be available at `http://127.0.0.1:5000`.

## API Endpoints

### Customers (`/customers`)

- `POST /` — create a customer
- `GET /` — get all customers
- `GET /<id>` — get a single customer
- `PUT /<id>` — update a customer
- `DELETE /<id>` — delete a customer

### Mechanics (`/mechanics`)

- `POST /` — create a mechanic
- `GET /` — get all mechanics
- `PUT /<id>` — update a mechanic
- `DELETE /<id>` — delete a mechanic

### Service Tickets (`/service-tickets`)

- `POST /` — create a service ticket
- `GET /` — get all service tickets
- `PUT /<ticket_id>/assign-mechanic/<mechanic_id>` — assign a mechanic to a ticket
- `PUT /<ticket_id>/remove-mechanic/<mechanic_id>` — remove a mechanic from a ticket

## Testing

A Postman collection (`Mechanic Shop API.postman_collection.json`) is included in this repo with example requests for every endpoint above.
