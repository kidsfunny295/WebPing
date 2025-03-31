import requests
import threading
from flask import Flask, request, jsonify

app = Flask(__name__)

# List of websites in the cycle
website_list = [
    "https://thrivemun.com",
]
website_list.append("https://webping.onrender.com")

# Global flag to track if a ping is scheduled
ping_scheduled = False
ping_lock = threading.Lock()  # Ensures thread-safe access to the flag

def delayed_ping():
    """Wait 10 minutes and restart the ping cycle if no other ping is running"""
    global ping_scheduled
    with ping_lock:
        if ping_scheduled:  # Avoid scheduling if already running
            return
        ping_scheduled = True

    threading.Timer(600, start_ping).start()  # Schedule next ping in 10 minutes

@app.route('/start-ping', methods=['GET'])
def start_ping():
    """Start the ping loop by sending the list to the main website"""
    global ping_scheduled
    with ping_lock:
        if ping_scheduled:  # Avoid duplicate pings
            return jsonify({"message": "Ping already scheduled"}), 200

        ping_scheduled = True

    try:
        response = requests.post(f"{website_list[0]}/rp", json={"websites": website_list[1:]})
        return jsonify({"message": "Ping cycle started", "response": response.json()}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        with ping_lock:
            ping_scheduled = False  # Reset flag after request is complete

@app.route('/rp', methods=['POST'])
def receive_list():
    """Receive ping, print debug message, and restart after 10 mins"""
    global ping_scheduled
    with ping_lock:
        if ping_scheduled:  # Avoid duplicate pings
            return jsonify({"message": "Ping already scheduled"}), 200

        ping_scheduled = True

    print("*****************************GOT PINGED*******************************")
    delayed_ping()  # Schedule next ping after 10 minutes
    return "Ping Received", 200

@app.route('/')
def home():
    return "Ping Website is running!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
