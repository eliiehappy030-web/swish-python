from flask import Flask, jsonify, send_from_directory
import os

app = Flask(__name__, static_folder=".", static_url_path="")

@app.route("/")
def home():
    return send_from_directory(".", "index.html")

@app.route("/api/test-library")
def test_library():
    try:
        import swish

        return jsonify({
            "status": "ok",
            "message": "Biblioteket laddades och körs ✅",
            "library": "swish-python",
            "has_SwishClient": hasattr(swish, "SwishClient"),
            "has_Environment": hasattr(swish, "Environment")
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": "Biblioteket kunde inte laddas",
            "error": str(e)
        }), 500

@app.route("/api/app-action")
def app_action():
    try:
        import swish

        return jsonify({
            "status": "ok",
            "message": "Knappen körde Python och biblioteket ✅",
            "has_SwishClient": hasattr(swish, "SwishClient")
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": "Något gick fel när biblioteket skulle köras",
            "error": str(e)
        }), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
