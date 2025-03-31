import requests
from flask import Flask, jsonify

app = Flask(__name__)

# List of websites in the cycle
website_list = [
    "https://thrivemun.com",
]
website_list.append("")
@app.route('/start-ping', methods=['GET'])
def start_ping():
    """Start the ping loop by sending the list to the main website"""
    try:
        response = requests.post(f"{website_list[0]}/rp", json={"websites": website_list[1:]})
        return jsonify({"message": "Ping cycle started", "response": response.json()}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def home():
    return "Ping Website is running!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

# # FOR REMAINING WEBSITES
# @app.route('/', methods=['POST'])
# def receive_list():
#     """Receive a list of websites and send it to the next one"""
#     data = request.get_json()
#     website_list = data.get("websites", [])

#     if not website_list or len(website_list) < 2:
#         return jsonify({"message": "No further websites to ping"}), 200

#     next_website = website_list[1]  # Get the next website in the list
#     remaining_list = website_list[1:]  # Remove the first entry

#     try:
#         response = requests.post(f"{website_list[0]}/rp", json={"websites": website_list[1:]})
#         return jsonify({"message": f"List forwarded to {next_website}", "response": response.json()}), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

