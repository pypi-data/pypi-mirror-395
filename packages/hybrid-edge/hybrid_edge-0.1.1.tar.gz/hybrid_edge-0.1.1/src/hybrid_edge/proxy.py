from flask import Flask, request, jsonify, Response
import requests
import os

app = Flask(__name__)

def run_proxy():
    OLLAMA_PORT = os.getenv("OLLAMA_PORT", "11434")
    SECRET_KEY = os.getenv("SECRET_KEY")
    FLASK_PORT = int(os.getenv("FLASK_PORT", "5000"))

    if not SECRET_KEY:
        print("❌ ERROR: SECRET_KEY not found in .env file!")
        return

    OLLAMA_URL = f"http://localhost:{OLLAMA_PORT}/api/generate"

    @app.route('/api/generate', methods=['POST'])
    def secure_gateway():
        auth_header = request.headers.get('Authorization')
        if auth_header != f"Bearer {SECRET_KEY}":
            return jsonify({"error": "Unauthorized"}), 403

        try:
            ollama_response = requests.post(OLLAMA_URL, json=request.json)
            return Response(ollama_response.content, status=ollama_response.status_code, content_type='application/json')
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    print(f"🛡️ Security Guard running on Port {FLASK_PORT}")
    # Disable reloader so it runs nicely in a thread
    app.run(port=FLASK_PORT, use_reloader=False)