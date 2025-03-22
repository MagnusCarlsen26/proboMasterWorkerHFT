import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
import threading
load_dotenv()

app = Flask(__name__)

DB_LOCK = threading.Lock()

@app.route('/save_data', methods=['GET'])
def save_data():
    payload = request.json
    save_data_sync(payload)
    
    return jsonify({"message": "Data received", "payload": payload})

@app.route('/test', methods=['GET'])
def test():
    return jsonify({"message": "Data received"})

def save_data_sync(payload):
    event_id = payload['eventId']
    timestamp = payload['timestamp']
    
    os.makedirs("data", exist_ok=True)
    
    event_dir = os.path.join("data", f"event_{event_id}")
    os.makedirs(event_dir, exist_ok=True)
    print(payload["available_qty"])

    try:
        with DB_LOCK: 
            yes_file = os.path.join(event_dir, "db_yes.csv")
            no_file = os.path.join(event_dir, "db_no.csv")
            
            with open(yes_file, "a") as f:
                f.write(f"{timestamp},{transform_data(payload['available_qty']['buy'])}\n")
            with open(no_file, "a") as f:
                f.write(f"{timestamp},{transform_data(payload['available_qty']['sell'])}\n")

    except Exception as e:
        print(e)

def transform_data(book):
    keys = [i/2 for i in range(1,20)]
    transformed_book = ""
    for key in keys:
        if str(key) in book:
            transformed_book += f"{book[str(key)]},"
    print(transformed_book)
    return transformed_book

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)