from flask import Flask, request, session, jsonify, send_from_directory
from db import Base, engine
from models import Product
from auth import register_user, verify_user
from service import place_order
from repository import get_user_by_id, get_all_products
import os
from flask import render_template
import base64
from flask_mail import Mail, Message

# app.py
# Ensure the necessary directories exist
app = Flask(__name__)
app.secret_key = os.urandom(24)

# Create DB tables
Base.metadata.create_all(bind=engine)

# Seed products if not present
from db import SessionLocal
session = SessionLocal()
if not session.query(Product).first():
    session.add_all([
        Product(name="Laptop", price=1000, stock=10),
        Product(name="Phone", price=500, stock=20)
    ])
    session.commit()
session.close()

@app.route("/")
def index():
    return jsonify({
        "message": "Welcome to the E-commerce API!",
        "endpoints": [
            "/register",
            "/login",
            "/logout",
            "/me",
            "/products",
            "/order"
        ]
    })

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400
    user = register_user(username, password)
    if not user:
        return jsonify({"error": "Username already exists"}), 400
    return jsonify({"message": "User registered successfully"}), 201

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    user = verify_user(username, password)
    if not user:
        return jsonify({"error": "Invalid username or password"}), 401
    session["user_id"] = user.id
    return jsonify({"message": "Logged in successfully"}), 200

@app.route("/logout", methods=["POST"])
def logout():
    session.pop("user_id", None)
    return jsonify({"message": "Logged out"}), 200

@app.route("/me", methods=["GET"])
def me():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401
    from repository import get_user_by_id
    user = get_user_by_id(user_id)
    return jsonify({"user_id": user.id, "username": user.username})

@app.route("/products", methods=["GET"])
def products():
    products = get_all_products()
    out = [
        {
            "id": p.id,
            "name": p.name,
            "price": p.price,
            "stock": p.stock
        } for p in products
    ]
    return jsonify(out)

@app.route("/order", methods=["POST"])
def order():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Authentication required"}), 401
    data = request.get_json()
    product_id = data.get("product_id")
    quantity = data.get("quantity", 1)
    if not product_id or not isinstance(quantity, int) or quantity < 1:
        return jsonify({"error": "product_id and positive integer quantity required"}), 400
    order, error = place_order(user_id, product_id, quantity)
    if error:
        return jsonify({"error": error}), 400
    return jsonify({
        "message": "Order placed successfully",
        "order_id": order.id,
        "product_id": order.product_id,
        "quantity": order.quantity
    }), 201

@app.route("/frontend")
def frontend():
    return send_from_directory(".", "frontend.html")

# --- draw.io integration PATCH START ---

# Ensure diagrams directory exists
DIAGRAMS_FOLDER = os.path.join(os.path.dirname(__file__), 'diagrams')
os.makedirs(DIAGRAMS_FOLDER, exist_ok=True)

@app.route("/diagram")
def diagram():
    return render_template("diagram.html", template_xml="")

@app.route('/diagrams/<filename>')
def get_diagram(filename):
    # Only allow .xml and .pdf files
    if not (filename.endswith('.xml') or filename.endswith('.pdf')):
        return jsonify({"error": "Invalid file type."}), 400
    return send_from_directory(DIAGRAMS_FOLDER, filename, as_attachment=True)

@app.route('/save_diagram', methods=['POST'])
def save_diagram():
    data = request.get_json()
    xml_content = data.get("xml")
    filename = data.get("filename", "diagram.xml")
    if not filename.lower().endswith(".xml"):
        filename += ".xml"
    if not xml_content or not isinstance(xml_content, str) or not xml_content.strip():
        return jsonify({"error": "No XML content provided."}), 400
    filepath = os.path.join(DIAGRAMS_FOLDER, filename)
    # If xml_content is a data URI, decode it
    if xml_content.strip().startswith("data:image/svg+xml;base64,"):
        try:
            b64 = xml_content.split(",", 1)[1]
            xml_content = base64.b64decode(b64).decode("utf-8")
        except Exception as e:
            return jsonify({"error": f"Failed to decode base64 XML: {e}"}), 400
    # Optionally, validate that xml_content looks like XML
    if not xml_content.strip().startswith("<"):
        return jsonify({"error": "Invalid XML content."}), 400
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(xml_content)
    return jsonify({"message": f"Diagram saved as {filename}!"})

@app.route('/save_pdf_diagram', methods=['POST'])
def save_pdf_diagram():
    import logging
    data = request.get_json()
    pdf_content = data.get("pdf")
    filename = data.get("filename", "diagram.pdf")
    if not filename.lower().endswith(".pdf"):
        filename += ".pdf"
    if not pdf_content or not isinstance(pdf_content, str) or not pdf_content.strip():
        logging.error(f"No PDF content provided for {filename}")
        return jsonify({"error": "No PDF content provided."}), 400
    filepath = os.path.join(DIAGRAMS_FOLDER, filename)
    try:
        if pdf_content.strip().startswith("data:application/pdf;base64,"):
            b64 = pdf_content.split(",", 1)[1]
            pdf_bytes = base64.b64decode(b64)
        else:
            pdf_bytes = base64.b64decode(pdf_content)
    except Exception as e:
        logging.error(f"Failed to decode PDF for {filename}: {e}")
        return jsonify({"error": f"Failed to decode PDF: {e}"}), 400
    if not pdf_bytes or not pdf_bytes.startswith(b'%PDF'):
        logging.error(f"Invalid PDF content for {filename}")
        return jsonify({"error": "Invalid PDF content. The file may be empty or corrupted."}), 400
    try:
        with open(filepath, "wb") as f:
            f.write(pdf_bytes)
    except Exception as e:
        logging.error(f"Failed to save PDF for {filename}: {e}")
        return jsonify({"error": f"Failed to save PDF: {e}"}), 500
    return jsonify({"message": f"Diagram saved as {filename}!"})

@app.route('/load_diagram', methods=['GET'])
def load_diagram():
    filename = request.args.get("filename")
    if not filename or not os.path.exists(os.path.join(DIAGRAMS_FOLDER, filename)):
        return jsonify({"error": "Diagram not found."}), 404
    with open(os.path.join(DIAGRAMS_FOLDER, filename), "r", encoding="utf-8") as f:
        xml_content = f.read()
    return jsonify({"xml": xml_content})

@app.route('/list_diagrams', methods=['GET'])
def list_diagrams():
    files = [f for f in os.listdir(DIAGRAMS_FOLDER) if f.endswith('.xml') or f.endswith('.pdf')]
    return jsonify({"files": files})

import base64

def repair_existing_diagram_file(filename):
    filepath = os.path.join(DIAGRAMS_FOLDER, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    if content.strip().startswith("data:image/svg+xml;base64,"):
        try:
            b64 = content.split(",", 1)[1]
            xml_content = base64.b64decode(b64).decode("utf-8")
            with open(filepath, "w", encoding="utf-8") as f2:
                f2.write(xml_content)
            return True, None
        except Exception as e:
            return False, str(e)
    return False, "File is not a base64 data URI."

@app.route('/repair_diagram/<filename>', methods=['POST'])
def repair_diagram(filename):
    success, error = repair_existing_diagram_file(filename)
    if success:
        return jsonify({"message": f"{filename} repaired!"})
    else:
        return jsonify({"error": error}), 400

@app.route('/send_diagram_email', methods=['POST'])
def send_diagram_email():
    data = request.get_json()
    recipient = data.get('email')
    filename = data.get('filename')
    format = data.get('format', 'pdf')  # 'pdf' or 'xml'

    # Get the file path
    file_path = os.path.join(DIAGRAMS_FOLDER, filename)
    if not os.path.exists(file_path):
        return jsonify({'error': 'Diagram not found.'}), 404

    # Compose and send the message
    msg = Message(subject="Your Requested Diagram",
                  recipients=[recipient],
                  body="Attached is your architectural diagram from our app.")
    with open(file_path, 'rb') as fp:
        ext = filename.split('.')[-1]
        mime_type = 'application/pdf' if ext == 'pdf' else 'text/xml'
        msg.attach(filename, mime_type, fp.read())

    try:
        mail.send(msg)
        return jsonify({'message': 'Diagram sent to email!'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
        # --- draw.io integration PATCH END ---
if __name__ == "__main__":
    app.run(debug=True)
# Add these config lines after you create your app (e.g., after `app = Flask(__name__)`)
app.config.update(
    MAIL_SERVER='smtp.yahoo.com',      # For Gmail, adjust for your provider
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME='raphaeljude@yahoo.com',    # Replace with your email
    MAIL_PASSWORD='xgHeaven24#',     # Replace with your password or app password
    MAIL_DEFAULT_SENDER='raphaeljude@yahoo.com'
)
mail = Mail(app)