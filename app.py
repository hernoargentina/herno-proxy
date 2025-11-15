from flask import Flask, render_template, request
import requests
import json

app = Flask(__name__, template_folder="templates", static_folder="static")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/buscar", methods=["POST"])
def buscar():
    query = request.form.get("query")
    paginas = int(request.form.get("paginas", 1))

    # CORRECCIÓN: usar endpoint REAL de tu proxy
    PROXY_URL = "https://flask-hello-world-7ck3.onrender.com/api/buscar"

    try:
        # Ahora enviamos GET como espera tu proxy
        r = requests.get(
            PROXY_URL,
            params={"query": query, "pages": paginas},
            timeout=30
        )

        raw = r.json()

    except Exception as e:
        return f"<h2>Error llamando al proxy:</h2><pre>{e}</pre>"

    resultados = raw.get("resultados", [])

    # --- Limpieza ---
    limpios = []
    for item in resultados:
        if isinstance(item, dict):
            limpios.append(item)
        else:
            try:
                limpios.append(json.loads(item))
            except:
                continue

    return render_template(
        "resultado.html",
        query=query,
        resultados=limpios,
        total=len(limpios)
    )

if __name__ == "__main__":
    app.run(debug=True)
