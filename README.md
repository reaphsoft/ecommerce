# E-commerce Flask Project (Terraform-ready)

This project is a full-stack e-commerce API and frontend built with Python, Flask, and SQLAlchemy, designed for modern cloud deployment using Terraform. It demonstrates a layered architecture and includes user registration, login, product listing, order placement, and a web frontend for API interaction. The project also integrates draw.io for architecture diagrams and is ready for infrastructure-as-code workflows.

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
- `terraform/` - Infrastructure as Code (Terraform configs, state, and scripts)

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

## Deployment & Terraform Notes
- The `terraform/` directory contains all Infrastructure as Code (IaC) files for AWS deployment.
- **State files and provider binaries are excluded from version control** via `.gitignore` to avoid large files and sensitive data in the repository.
- To deploy infrastructure:
    1. `cd terraform`
    2. `terraform init` (downloads providers)
    3. `terraform plan` (review changes)
    4. `terraform apply` (provision resources)
- **Never commit `.terraform/` or `*.tfstate` files.**
- Collaborators should always run `terraform init` after cloning or pulling changes.

## Diagrams
- Architecture and use-case diagrams are stored in `diagrams/` and `diagram_templates/`.
- Edit or view diagrams using draw.io or the integrated web UI.

---

**This repository is now clean and ready for collaboration and cloud deployment.**
