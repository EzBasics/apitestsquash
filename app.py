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

# Dynamic endpoints using a user_id parameter

@app.route("/proxy/user/<int:user_id>/schools")
def proxy_user_schools(user_id):
    api_url = f"https://api.ussquash.com/resources/res/user/{user_id}/schools"
    logger.info("Fetching schools from: %s", api_url)
    try:
        response = requests.get(api_url, cookies=COOKIES, timeout=10)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.HTTPError as http_err:
        logger.error("HTTP error occurred: %s", http_err)
        return jsonify({"error": f"HTTP error: {http_err}"}), response.status_code
    except requests.exceptions.RequestException as req_err:
        logger.error("Error fetching API data: %s", req_err)
        return jsonify({"error": "Error fetching API data."}), 500
    except Exception as e:
        logger.error("Unexpected error: %s", e)
        return jsonify({"error": "An unexpected error occurred."}), 500

@app.route("/proxy/user/<int:user_id>/record")
def proxy_user_record(user_id):
    """Fetch the user record for the given user."""
    api_url = f"https://api.ussquash.com/resources/res/user/{user_id}/record"
    logger.info("Fetching user record from: %s", api_url)
    try:
        response = requests.get(api_url, cookies=COOKIES, timeout=10)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.HTTPError as http_err:
        logger.error("HTTP error: %s", http_err)
        return jsonify({"error": f"HTTP error: {http_err}"}), response.status_code
    except requests.exceptions.RequestException as req_err:
        logger.error("Request error: %s", req_err)
        return jsonify({"error": "Error fetching API data."}), 500
    except Exception as e:
        logger.error("Unexpected error: %s", e)
        return jsonify({"error": "An unexpected error occurred while processing your request."}), 500

@app.route("/proxy/liveScoreDetails")
def proxy_live_score_details():
    # The match_id now can be passed dynamically
    match_id = request.args.get("match_id", DEFAULT_MATCH_ID)
    api_url = f"https://api.ussquash.com/resources/res/matches/{match_id}/liveScoreDetails"
    logger.info("Fetching live score details from: %s", api_url)
    try:
        response = requests.get(api_url, cookies=COOKIES, timeout=10)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.HTTPError as http_err:
        logger.error("HTTP error: %s", http_err)
        return jsonify({"error": f"HTTP error: {http_err}"}), response.status_code
    except requests.exceptions.RequestException as req_err:
        logger.error("Request error: %s", req_err)
        return jsonify({"error": "Error fetching API data."}), 500
    except Exception as e:
        logger.error("Unexpected error: %s", e)
        return jsonify({"error": "An unexpected error occurred while processing your request."}), 500

@app.route("/proxy/user/<int:user_id>")
def proxy_user_profile(user_id):
    api_url = f"https://api.ussquash.com/resources/res/user/{user_id}"
    logger.info("Fetching user profile from: %s", api_url)
    try:
        response = requests.get(api_url, cookies=COOKIES, timeout=10)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.HTTPError as http_err:
        logger.error("HTTP error: %s", http_err)
        return jsonify({"error": f"HTTP error: {http_err}"}), response.status_code
    except requests.exceptions.RequestException as req_err:
        logger.error("Request error: %s", req_err)
        return jsonify({"error": "Error fetching API data."}), 500
    except Exception as e:
        logger.error("Unexpected error: %s", e)
        return jsonify({"error": "An unexpected error occurred."}), 500

@app.route("/proxy/user/<int:user_id>/ratings-top")
def proxy_user_ratings_top(user_id):
    api_url = f"https://api.ussquash.com/resources/res/user/{user_id}/ratings-top"
    logger.info("Fetching highest rating from: %s", api_url)
    try:
        response = requests.get(api_url, cookies=COOKIES, timeout=10)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.HTTPError as http_err:
        logger.error("HTTP error: %s", http_err)
        return jsonify({"error": f"HTTP error: {http_err}"}), response.status_code
    except requests.exceptions.RequestException as req_err:
        logger.error("Request error: %s", req_err)
        return jsonify({"error": "Error fetching API data."}), 500
    except Exception as e:
        logger.error("Unexpected error: %s", e)
        return jsonify({"error": "An unexpected error occurred."}), 500

@app.route("/proxy/user/<int:user_id>/ratings")
def proxy_user_ratings(user_id):
    api_url = f"https://api.ussquash.com/resources/res/user/{user_id}/ratings"
    logger.info("Fetching current rating from: %s", api_url)
    try:
        response = requests.get(api_url, cookies=COOKIES, timeout=10)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.HTTPError as http_err:
        logger.error("HTTP error: %s", http_err)
        return jsonify({"error": f"HTTP error: {http_err}"}), response.status_code
    except requests.exceptions.RequestException as req_err:
        logger.error("Request error: %s", req_err)
        return jsonify({"error": "Error fetching API data."}), 500
    except Exception as e:
        logger.error("Unexpected error: %s", e)
        return jsonify({"error": "An unexpected error occurred."}), 500

@app.route("/proxy/user/<int:user_id>/ratings_history")
def proxy_user_ratings_history(user_id):
    api_url = f"https://api.ussquash.com/resources/res/user/{user_id}/ratings_history"
    logger.info("Fetching ratings history from: %s", api_url)
    try:
        response = requests.get(api_url, cookies=COOKIES, timeout=10)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.HTTPError as http_err:
        logger.error("HTTP error: %s", http_err)
        return jsonify({"error": f"HTTP error: {http_err}"}), response.status_code
    except requests.exceptions.RequestException as req_err:
        logger.error("Request error: %s", req_err)
        return jsonify({"error": "Error fetching API data."}), 500
    except Exception as e:
        logger.error("Unexpected error: %s", e)
        return jsonify({"error": "An unexpected error occurred."}), 500

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

@app.route("/users", methods=["GET", "POST"])
def users():
    if request.method == "POST":
        match_id = request.form.get("match_id", DEFAULT_MATCH_ID)
        return redirect(url_for("schedule", match_id=match_id))
    else:
        match_id = request.args.get("match_id", DEFAULT_MATCH_ID)
        try:
            return render_template("users.html", match_id=match_id)
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

@app.route("/proxy/user/<int:user_id>/rankings")
def proxy_user_rankings(user_id):
    api_url = f"https://api.ussquash.com/resources/res/user/{user_id}/rankings?history=yes"
    logger.info("Fetching user rankings from: %s", api_url)
    try:
        response = requests.get(api_url, cookies=COOKIES, timeout=10)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.HTTPError as http_err:
        logger.error("HTTP error: %s", http_err)
        return jsonify({"error": f"HTTP error: {http_err}"}), response.status_code
    except requests.exceptions.RequestException as req_err:
        logger.error("Request error: %s", req_err)
        return jsonify({"error": "Error fetching API data."}), 500
    except Exception as e:
        logger.error("Unexpected error: %s", e)
        return jsonify({"error": "An unexpected error occurred."}), 500

@app.route("/proxy/players/<int:user_id>/leagues")
def proxy_player_leagues(user_id):
    api_url = f"https://api.ussquash.com/resources/res/players/{user_id}/leagues"
    logger.info("Fetching player leagues from: %s", api_url)
    try:
        response = requests.get(api_url, cookies=COOKIES, timeout=10)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.HTTPError as http_err:
        logger.error("HTTP error: %s", http_err)
        return jsonify({"error": f"HTTP error: {http_err}"}), response.status_code
    except requests.exceptions.RequestException as req_err:
        logger.error("Request error: %s", req_err)
        return jsonify({"error": "Error fetching API data."}), 500
    except Exception as e:
        logger.error("Unexpected error: %s", e)
        return jsonify({"error": "An unexpected error occurred."}), 500

@app.route("/proxy/user/<int:user_id>/affiliations")
def proxy_user_affiliations(user_id):
    api_url = f"https://api.ussquash.com/resources/res/user/{user_id}/affiliations"
    logger.info("Fetching user affiliations from: %s", api_url)
    try:
        response = requests.get(api_url, cookies=COOKIES, timeout=10)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.HTTPError as http_err:
        logger.error("HTTP error: %s", http_err)
        return jsonify({"error": f"HTTP error: {http_err}"}), response.status_code
    except requests.exceptions.RequestException as req_err:
        logger.error("Request error: %s", req_err)
        return jsonify({"error": "Error fetching API data."}), 500
    except Exception as e:
        logger.error("Unexpected error: %s", e)
        return jsonify({"error": "An unexpected error occurred."}), 500

@app.route("/proxy/search")
def proxy_search():
    query = request.args.get("q")
    if not query:
        return jsonify({"error": "Missing query parameter"}), 400
    encoded_query = query.replace(" ", "%20")
    api_url = f"https://api.ussquash.com/resources/res/search/{encoded_query}"
    logger.info("Fetching search results from: %s", api_url)
    try:
        response = requests.get(api_url, cookies=COOKIES, timeout=10)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.HTTPError as http_err:
        logger.error("HTTP error: %s", http_err)
        return jsonify({"error": f"HTTP error: {http_err}"}), response.status_code
    except requests.exceptions.RequestException as req_err:
        logger.error("Request error: %s", req_err)
        return jsonify({"error": "Error fetching API data."}), 500
    except Exception as e:
        logger.error("Unexpected error: %s", e)
        return jsonify({"error": "An unexpected error occurred."}), 500

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
