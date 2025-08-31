from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def root():
    return "<h1>Hello from Flask</h1><p>Status: OK</p>", 200

@app.route("/health")
def health():
    return jsonify(status="healthy"), 200