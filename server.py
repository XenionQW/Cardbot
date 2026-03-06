from flask import Flask, render_template, jsonify, request, abort
from database.db import get_user_collection, get_user, get_top_users
from config import WEBAPP_HOST, WEBAPP_PORT
import os

app = Flask(__name__, template_folder="templates", static_folder="static")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/collection")
def collection():
    user_id = request.args.get("user_id", type=int)
    if not user_id:
        abort(400, "user_id required")
    return render_template("collection.html", user_id=user_id)


@app.route("/api/collection/<int:user_id>")
def api_collection(user_id: int):
    user = get_user(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    cards = get_user_collection(user_id)
    return jsonify({
        "user": {
            "first_name": user["first_name"],
            "username": user["username"],
            "total_cards": user["total_cards"],
            "black_holes": user["black_holes"],
        },
        "cards": cards,
        "total_power": sum(c["power"] * c["count"] for c in cards),
    })


@app.route("/api/top")
def api_top():
    top = get_top_users(10)
    return jsonify(top)


def start_webapp():
    app.run(host=WEBAPP_HOST, port=WEBAPP_PORT, debug=False, use_reloader=False)
