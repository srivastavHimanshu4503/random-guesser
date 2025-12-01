from flask import Flask, render_template, request, jsonify, session
import random
import os

app = Flask(__name__, static_folder="static", template_folder="templates")
# set a secret key for session (in production, load from env)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "change-this-in-prod")

# start a new game (or reset)
@app.route("/start", methods=["POST"])
def start_game():
    session["target"] = random.randint(1, 100)
    session["attempts"] = 0
    return jsonify({"status": "ok", "message": "New game started", "range": [1, 100]})

# make a guess
@app.route("/guess", methods=["POST"])
def guess():
    if "target" not in session:
        return jsonify({"status": "error", "message": "No active game. Call /start first."}), 400

    data = request.get_json()
    if not data or "guess" not in data:
        return jsonify({"status": "error", "message": "Missing 'guess' in JSON body."}), 400

    try:
        user_guess = int(data["guess"])
    except (ValueError, TypeError):
        return jsonify({"status": "error", "message": "Guess must be an integer."}), 400

    session["attempts"] = session.get("attempts", 0) + 1
    target = session["target"]

    if user_guess == target:
        attempts = session["attempts"]
        # clear game (optional)
        session.pop("target", None)
        session.pop("attempts", None)
        return jsonify({
            "status": "correct",
            "message": f"Correct! You guessed the number in {attempts} attempts.",
            "attempts": attempts
        })
    elif user_guess > target:
        return jsonify({"status": "lower", "message": "Lower the number.", "attempts": session["attempts"]})
    else:
        return jsonify({"status": "higher", "message": "Increase the number.", "attempts": session["attempts"]})

# main page
@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
