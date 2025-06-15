# E-commerce Flask Project (Terraform-ready)

This is a layered architecture example for an e-commerce API and frontend, built with Python, Flask, and SQLAlchemy. The project is designed for easy deployment (e.g., with Terraform) and includes user registration, login, product listing, order placement, and a web frontend for API interaction. It also integrates draw.io for architecture diagrams.

## Structure

- `app.py` - Flask API (Presentation Layer)
- `auth.py` - Authentication logic
- `service.py` - Business logic (orders)
- `models.py` - SQLAlchemy ORM models (Domain)
- `repository.py` - Data access helpers
- `db.py` - DB setup
- `requirements.txt` - Dependencies
- `frontend.html` - Web UI for API
- `templates/diagram.html` - draw.io integration
- `diagrams/` - Saved diagrams (XML, PDF)

## Setup

1. **Install dependencies:**

    pip install -r requirements.txt

2. **Run the app:**

    python app.py

3. **Demo via curl:**

    # Register a user
    curl -X POST http://localhost:5000/register -H "Content-Type: application/json" -d '{"username":"user1","password":"test"}'

    # Login
    curl -X POST http://localhost:5000/login -H "Content-Type: application/json" -d '{"username":"user1","password":"test"}'

    # Get products
    curl http://localhost:5000/products

    # Place an order (after logging in, send cookie for session)
    curl -X POST http://localhost:5000/order -H "Content-Type: application/json" -d '{"product_id":1,"quantity":1}' --cookie-jar cookies.txt --cookie cookies.txt

## Security
- Passwords are hashed, never stored in plaintext.
- All endpoints validate input.
- Orders require authentication (session-based).
- SQLAlchemy ORM prevents SQL injection by default.

## Deployment
- Project is structured for easy deployment, including with Terraform or other IaC tools.
