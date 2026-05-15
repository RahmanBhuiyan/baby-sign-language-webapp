import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

from inference import predict
from model_loader import get_model

DIST_DIR = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "..", "frontend", "dist")
)

app = Flask(__name__, static_folder=None)
CORS(app)


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@app.route("/api/predict", methods=["POST"])
def api_predict():
    data = request.get_json(silent=True) or {}
    image = data.get("image")
    if not image:
        return jsonify({"error": "missing 'image' field"}), 400
    try:
        result = predict(image)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return jsonify(result)


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_frontend(path: str):
    if not os.path.isdir(DIST_DIR):
        return (
            "Frontend not built yet. Run `npm run dev` in webapp/frontend or "
            "`npm run build` to produce the dist/ folder.",
            503,
        )
    target = os.path.join(DIST_DIR, path)
    if path and os.path.isfile(target):
        return send_from_directory(DIST_DIR, path)
    return send_from_directory(DIST_DIR, "index.html")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    print("Loading model...")
    get_model()
    print(f"Model ready. Starting Flask on http://localhost:{port}")
    app.run(host="0.0.0.0", port=port, debug=False, threaded=True)
