@app.route('/rp', methods=['POST'])
def receive_list():
    """Receive a list of websites and send it to the next one"""
    data = request.get_json()
    website_list = data.get("websites", [])
    print("*****************RECIEVED DATA FROM PIN*******************************\n",website_list)
    if not website_list:  # If list is empty, return to ping website
        return jsonify({"message": "Ping cycle complete"}), 200

    next_website = website_list[0]  # Get next website
    remaining_list = website_list[1:]  # Remove first entry

    try:
        response = requests.post(f"{next_website}/rp", json={"websites": remaining_list})
        return jsonify({"message": f"List forwarded to {next_website}", "response": response.json()}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
