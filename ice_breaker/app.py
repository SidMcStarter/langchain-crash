from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from ice_breaker.ice_breaker import ice_break_with

load_dotenv()

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/process", methods=["POST"])
def process():
    name = request.form.get("name")
    if name:
        summary, photo_url = ice_break_with(name)
        return jsonify({"summary_and_facts": summary.to_dict(), "photoUrl": photo_url})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")