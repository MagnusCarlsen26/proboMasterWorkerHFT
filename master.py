import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
import asyncio
load_dotenv()

app = Flask(__name__)

DB_LOCK = asyncio.Lock()

@app.route('/save_data', methods=['GET'])
def save_data():
    payload = request.json
    asyncio.run(save_data_async(payload))
    
    return jsonify({"message": "Data received", "payload": payload})

@app.route('/test', methods=['GET'])
def test():
    return jsonify({"message": "Data received"})

async def save_data_async(payload):
    event_id = payload['eventId']
    timestamp = payload['timestamp']
    
    # Create data directory if it doesn't exist
    os.makedirs("data", exist_ok=True)
    
    # Create directory for event if it doesn't exist
    event_dir = os.path.join("data", f"event_{event_id}")
    os.makedirs(event_dir, exist_ok=True)
    print(payload["available_qty"])
    async with DB_LOCK: 
        # Save data to event-specific files
        yes_file = os.path.join(event_dir, "db_yes.csv")
        no_file = os.path.join(event_dir, "db_no.csv")
        
        with open(yes_file, "a") as f:
            f.write(f"{timestamp},{transform_data(payload['available_qty']['buy'])}\n")
        with open(no_file, "a") as f:
            f.write(f"{timestamp},{transform_data(payload['available_qty']['sell'])}\n")

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