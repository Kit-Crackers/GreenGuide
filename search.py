from flask import Blueprint, jsonify, request, render_template, abort
from data_loader import load_plants
import os

search_bp = Blueprint("search", __name__)

plants_data = load_plants()

# function to fetch plant image
def get_plant_image(plant_name):

    folder = os.path.join("static", "img", "plants")

    clean_name = plant_name.split("(")[0].strip().lower()

    for file in os.listdir(folder):

        if clean_name in file.lower():
            return f"/static/img/plants/{file}"

    return "/static/img/default.jpg"


# Search page
@search_bp.route("/search")
def search_page():
    return render_template("search.html")


# API for live suggestions
@search_bp.route("/api/search")
def api_search():
    q = request.args.get("q", "").lower()

    return jsonify([
        p["name"] for p in plants_data
        if q and q in p["name"].lower()
    ])


# Plant detail page
@search_bp.route("/plant/<plant_name>")
def plant_detail(plant_name):

    plant = next(
        (p for p in plants_data if p["name"].lower() == plant_name.lower()),
        None
    )

    if not plant:
        abort(404)

    plant_image = get_plant_image(plant["name"])

    return render_template(
        "plant_detail.html",
        plant=plant,
        plant_image=plant_image
    )