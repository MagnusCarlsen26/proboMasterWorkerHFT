import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()

HEADERS = {
    "accept": "*/*",
    "accept-language": "en",
    "appid": "in.probo.pro",
    "authorization": f"Bearer {os.getenv('PROBO_BEARER_TOKEN')}",
    "content-type": "application/json"
}

PROBO_URL = "https://prod.api.probo.in/api/v3/tms/trade/bestAvailablePrice?eventId={eventId}"
MASTER_URL = os.getenv("MASTER_URL")

def get_available_qty( eventId: int ):
    
    response = requests.get( PROBO_URL.format( eventId = eventId ), headers = HEADERS )
    
    response.raise_for_status()
    
    data = response.json()
    
    return data["data"]["available_qty"]

def send_data( available_qty: int, eventId: int ):

    response = requests.get( 
        MASTER_URL, 
        headers = HEADERS, 
        json = { 
            "available_qty": available_qty,
            "eventId": eventId,
            "timestamp": time.time()
        } 
    )
    response.raise_for_status()

if __name__ == "__main__":
    
    EVENT_ID = 3824790

    available_qty = get_available_qty( eventId = EVENT_ID )
    send_data( available_qty, eventId = EVENT_ID )