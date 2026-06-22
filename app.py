from flask import Flask, render_template, abort, request, redirect, session, flash, jsonify
from search import search_bp, get_plant_image
from data_loader import load_plants
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from predict import predict_disease
import os, uuid
import requests
import urllib.parse


app = Flask(__name__)
app.secret_key = "your_secret_key"
app.register_blueprint(search_bp)

def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

# Load plant data once
plants_data = load_plants()


@app.context_processor
def inject_user():
    return dict(user=session.get("user_email"))

@app.route("/")
def home():
    return render_template("index.html", user=session.get("user_email"))

@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/register", methods=["POST"])
def register():
    email = request.form["email"]
    password = request.form["password"]

    hashed_password = generate_password_hash(password)

    conn = get_db()
    cur = conn.cursor()

    try:
        cur.execute("INSERT INTO users (email, password) VALUES (?, ?)", 
                    (email, hashed_password))
        conn.commit()
    except:
        flash("User already exists!", "error")
        return redirect("/")

    conn.close()

    return redirect("/")

@app.route("/login", methods=["POST"])
def login():
    email = request.form["email"]
    password = request.form["password"]

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cur.fetchone()

    conn.close()

    if user and check_password_hash(user["password"], password):
        session["user_id"] = user["id"]
        session["user_email"] = user["email"]
        return redirect("/")
    else:
       flash("Invalid email or password!", "error")
       return redirect("/")
    
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/account")
def account():
    if "user_id" not in session:
        return redirect("/")

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM user_plants WHERE user_id = ?", (session["user_id"],))
    plants = cur.fetchall()

    conn.close()

    return render_template(
    "account.html",
    plants=plants,
    user=session.get("user_email")
)

@app.route("/add_plant", methods=["POST"])
def add_plant():
    if "user_id" not in session:
        return redirect("/")

    plant_name = request.form["plant_name"]
    plant_id = request.form["plant_id"]

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO user_plants (user_id, plant_name, plant_id) VALUES (?, ?, ?)",
        (session["user_id"], plant_name, plant_id)
    )

    conn.commit()
    conn.close()

    return redirect("/account")

@app.route("/remove_plant", methods=["POST"])
def remove_plant():

    if "user_id" not in session:
        return jsonify({"success": False})

    data = request.get_json()

    plant_id = data.get("plant_id")

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM user_plants WHERE user_id = ? AND plant_id = ?",
        (session["user_id"], plant_id)
    )

    conn.commit()
    conn.close()

    return jsonify({"success": True})

@app.route("/predict", methods=["POST"])
def predict():

    if "image" not in request.files:
        return "No image uploaded"

    file = request.files["image"]

    if file.filename == "":
        return "No file selected"

    filename = str(uuid.uuid4()) + file.filename
    filepath = os.path.join("static/img", filename)
    file.save(filepath)

    disease, confidence, care = predict_disease(filepath)

    plant_name = request.form.get("plant_name")

    plant = next(
        (p for p in plants_data if p["name"].lower() == plant_name.lower()),
        None
    )

    plant_image = get_plant_image(plant["name"])

    return render_template(
        "plant_detail.html",
        plant=plant,
        plant_image=plant_image,
        disease=disease,
        confidence=round(confidence * 100, 2),
        care=care
    )
    



if __name__ == "__main__":
    app.run(debug=True)
