from flask import Flask, render_template, jsonify, request, redirect, url_for, send_from_directory
import requests
import logging
import os

app = Flask(__name__)

# Default match id if none is provided
DEFAULT_MATCH_ID = "3499012"

# Session cookie (used to bypass CORS via server-side fetch)
COOKIES = {
    "USSQ-API-SESSION": "s%3AnP8iOvjFv4N5MtnTsq2NikJ0DhzWUQAK.nDc6GCWcX6fO3ek%2FnAlrRf9WXQNfWbWivmwg9bAymqA"
}

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route("/proxy/liveScoreDetails")
def proxy_live_score_details():
    # Get the match_id from the query parameter (or use default)
    match_id = request.args.get("match_id", DEFAULT_MATCH_ID)
    # Build the API URL dynamically based on match_id
    api_url = f"https://api.ussquash.com/resources/res/matches/{match_id}/liveScoreDetails"
    logger.info("Fetching data from API URL: %s", api_url)
    try:
        response = requests.get(api_url, cookies=COOKIES, timeout=10)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        return jsonify(data)
    except requests.exceptions.HTTPError as http_err:
        logger.error("HTTP error occurred: %s", http_err)
        return jsonify({"error": f"HTTP error: {http_err}"}), response.status_code
    except requests.exceptions.RequestException as req_err:
        logger.error("Error fetching API data: %s", req_err)
        return jsonify({"error": "Error fetching API data."}), 500
    except Exception as e:
        logger.error("An unexpected error occurred: %s", e)
        return jsonify({"error": "An unexpected error occurred while processing your request."}), 500

@app.route("/schedule", methods=["GET", "POST"])
def schedule():
    if request.method == "POST":
        match_id = request.form.get("match_id", DEFAULT_MATCH_ID)
        return redirect(url_for("schedule", match_id=match_id))
    else:
        match_id = request.args.get("match_id", DEFAULT_MATCH_ID)
        try:
            return render_template("schedule.html", match_id=match_id)
        except Exception as e:
            logger.error("Template rendering error: %s", e)
            return jsonify({"error": "Template not found or rendering error."}), 500
        
@app.route("/allteamsschedule", methods=["GET", "POST"])
def schedule2():
    if request.method == "POST":
        match_id = request.form.get("match_id", DEFAULT_MATCH_ID)
        return redirect(url_for("schedule2", match_id=match_id))
    else:
        match_id = request.args.get("match_id", DEFAULT_MATCH_ID)
        try:
            return render_template("allteamsschedule.html", match_id=match_id)
        except Exception as e:
            logger.error("Template rendering error: %s", e)
            return jsonify({"error": "Template not found or rendering error."}), 500

@app.route("/compare")
def compare():
    return send_from_directory(os.getcwd(), "compare.html")

@app.route("/")
def roster():
    return send_from_directory(os.getcwd(), "roster.html")

@app.route("/live")
def live():
    return send_from_directory(os.getcwd(), "live.html")

@app.route("/livescores")
def livescores():
    return send_from_directory(os.getcwd(), "livescores.html")

@app.route("/standings")
def standings():
    return send_from_directory(os.getcwd(), "standings.html")

@app.route("/teamtournament")
def teamtournament():
    # This route serves teamtournament.html and will include any query parameters.
    return send_from_directory(os.getcwd(), "teamtournament.html")

@app.route("/tournaments")
def tournaments():
    return send_from_directory(os.getcwd(), "tournaments.html")

@app.route("/singlestournament")
def singlestournament():
    return send_from_directory(os.getcwd(), "singlestournament.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
