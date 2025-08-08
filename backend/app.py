# app.py
# Flask backend to verify NGO details using government API (e.g., NGO Darpan).
# Will also handle IPFS file uploads and Supabase integration.

from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "NGO Transparency Backend Running"

if __name__ == "__main__":
    app.run(debug=True)
