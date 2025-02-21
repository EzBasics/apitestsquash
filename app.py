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

@app.route("/", methods=["GET", "POST"])
def schedule():
    if request.method == "POST":
        match_id = request.form.get("match_id", DEFAULT_MATCH_ID)
        return redirect(url_for("schedule", match_id=match_id))
    else:
        match_id = request.args.get("match_id", DEFAULT_MATCH_ID)
        try:
            return render_template("index.html", match_id=match_id)
        except Exception as e:
            logger.error("Template rendering error: %s", e)
            return jsonify({"error": "Template not found or rendering error."}), 500

# New route to serve compare.html (static file)
@app.route("/compare")
def compare():
    # This assumes compare.html is in the same folder as app.py.
    # If you move compare.html to a "static" folder, update the folder name accordingly.
    return send_from_directory(os.getcwd(), "compare.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
