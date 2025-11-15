import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

APP_ID = "9dddf785"
APP_KEY = "f843bbbb07cd57d4ec2426d66b918373"

@app.route("/")
def home():
    return "Proxy API de Herno funcionando correctamente."

@app.route("/api/buscar")
def buscar():
    query = request.args.get("query", "").strip()
    pages = int(request.args.get("pages", "1"))

    if not query:
        return jsonify({"error": "missing query"}), 400

    results = []

    for p in range(1, pages + 1):
        url = f"https://api.adzuna.com/v1/api/jobs/ar/search/{p}"
        params = {
            "app_id": APP_ID,
            "app_key": APP_KEY,
            "what": query,
            "results_per_page": 50,
        }

        r = requests.get(url, params=params)
        data = r.json()

        if "results" not in data:
            break

        results.extend(data["results"])

        if len(data["results"]) < 50:
            break

    return jsonify({"query": query, "resultados": results})
