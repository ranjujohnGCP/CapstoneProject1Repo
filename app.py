from flask import Flask, jsonify, request, render_template_string
import time
import random
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

# -----------------------------
# In-Memory DB
# -----------------------------
products = [
    {"id": 1, "name": "Laptop", "price": 80000, "img": "https://cdn-icons-png.flaticon.com/512/2920/2920277.png"},
    {"id": 2, "name": "Phone", "price": 30000, "img": "https://cdn-icons-png.flaticon.com/512/15/15874.png"},
    {"id": 3, "name": "Headphones", "price": 2000, "img": "https://cdn-icons-png.flaticon.com/512/727/727245.png"}
]

cart = []

# -----------------------------
# UI Home Page
# -----------------------------
@app.route("/")
def home():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>E-Commerce App</title>
        <style>
            body {
                font-family: Arial;
                background: linear-gradient(to right, #1e3c72, #2a5298);
                color: white;
                text-align: center;
            }
            h1 {
                margin-top: 20px;
            }
            .container {
                display: flex;
                justify-content: center;
                gap: 20px;
                margin-top: 30px;
            }
            .card {
                background: white;
                color: black;
                padding: 15px;
                border-radius: 10px;
                width: 200px;
                box-shadow: 0px 4px 10px rgba(0,0,0,0.3);
            }
            .card img {
                width: 80px;
            }
            button {
                background: #2a5298;
                color: white;
                border: none;
                padding: 8px 12px;
                margin-top: 10px;
                cursor: pointer;
                border-radius: 5px;
            }
            button:hover {
                background: #1e3c72;
            }
            .checkout-btn {
                background: green;
                margin-top: 20px;
                padding: 10px 20px;
                font-size: 16px;
            }
        </style>
    </head>
    <body>

        <h1>🛒 E-Commerce Microservice</h1>
        <p>Modernized App (Flask + Kubernetes Ready)</p>

        <div class="container">
            {% for p in products %}
            <div class="card">
                <img src="{{p.img}}" />
                <h3>{{p.name}}</h3>
                <p>₹{{p.price}}</p>
                <button onclick="addToCart({{p.id}})">Add to Cart</button>
            </div>
            {% endfor %}
        </div>

        <h2 style="margin-top:40px;">
            🛍️ Cart Items: <span id="cartCount">0</span>
        </h2>

        <button class="checkout-btn" onclick="checkout()">
            ✅ Checkout
        </button>

        <h3 id="statusMsg" style="margin-top:20px;"></h3>

        <script>
            async function addToCart(id) {
                await fetch('/cart', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({product_id: id})
                });
                loadCart();
            }

            async function loadCart() {
                let res = await fetch('/cart');
                let data = await res.json();
                document.getElementById('cartCount').innerText = data.length;
            }

            async function checkout() {
                document.getElementById("statusMsg").innerText = "⏳ Processing...";

                let res = await fetch('/checkout', {
                    method: 'POST'
                });

                let data = await res.json();

                if (res.status === 200) {
                    document.getElementById("statusMsg").innerText =
                        "✅ Order Placed Successfully!";
                } else {
                    document.getElementById("statusMsg").innerText =
                        "❌ Failed: " + (data.reason || data.error || "Try again");
                }

                loadCart();
            }

            loadCart();
        </script>

    </body>
    </html>
    """
    return render_template_string(html, products=products)


# -----------------------------
# APIs
# -----------------------------
@app.route("/health")
def health():
    return jsonify({"status": "UP"})


@app.route("/ready")
def ready():
    return jsonify({"status": "READY"})


@app.route("/products")
def get_products():
    return jsonify(products)


@app.route("/cart", methods=["GET"])
def get_cart():
    return jsonify(cart)


@app.route("/cart", methods=["POST"])
def add_to_cart():
    data = request.get_json()
    pid = data.get("product_id")

    for p in products:
        if p["id"] == pid:
            cart.append(p)
            return jsonify({"message": "Added"}), 201

    return jsonify({"error": "Not found"}), 404


@app.route("/checkout", methods=["POST"])
def checkout():
    if not cart:
        return jsonify({"error": "Cart empty"}), 400

    logging.info("Processing checkout...")

    time.sleep(random.randint(1, 3))

    if random.random() < 0.3:
        logging.error("Payment failed")
        return jsonify({"status": "FAILED", "reason": "Payment gateway error"}), 500

    cart.clear()
    return jsonify({"status": "SUCCESS"})


@app.route("/metrics")
def metrics():
    return jsonify({
        "total_products": len(products),
        "cart_items": len(cart)
    })


# -----------------------------
# Run
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
