import os
import hashlib
import hmac
import time
from urllib.parse import urlencode
import requests
from dotenv import load_dotenv
from bot.logging_config import logger

load_dotenv()

class BinanceFuturesClient:
    BASE_URL = "https://testnet.binancefuture.com"

    def __init__(self, api_key: str = None, api_secret: str = None):
        self.api_key = api_key or os.getenv("BINANCE_API_KEY")
        self.api_secret = api_secret or os.getenv("BINANCE_API_SECRET")

        if not self.api_key or not self.api_secret:
            logger.error("API credentials not found. Please set BINANCE_API_KEY and BINANCE_API_SECRET.")
            raise ValueError("API credentials are required. Define them in .env or pass them directly.")

        self.session = requests.Session()
        self.session.headers.update({
            "X-MBX-APIKEY": self.api_key,
            "Content-Type": "application/json"
        })

    def _generate_signature(self, query_string: str) -> str:
        """
        Generates HMAC SHA256 signature required by Binance API.
        """
        return hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

    def _dispatch_request(self, method: str, endpoint: str, params: dict = None) -> dict:
        """
        Dispatches request to Binance API with signature and error handling.
        """
        if params is None:
            params = {}

        params["timestamp"] = int(time.time() * 1000)
        query_string = urlencode(params)
        signature = self._generate_signature(query_string)
        
        # Append signature to parameters for urlencode
        params["signature"] = signature

        url = f"{self.BASE_URL}{endpoint}"

        logger.info(f"Sending {method} request to {url} format params")
        
        try:
            # We use params for GET and POST (Binance expects them in query string or data depending on endpoint, 
            # but usually query string is fine for /fapi/v1/order)
            if method.upper() == "GET":
                response = self.session.get(url, params=params, timeout=10)
            elif method.upper() == "POST":
                # For POST requests, parameters can be sent in query string or form data. 
                # Sending in query string works for Binance.
                response = self.session.post(url, params=params, timeout=10)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            response.raise_for_status()
            data = response.json()
            logger.info(f"API Response [{response.status_code}]: {data}")
            return data

        except requests.exceptions.HTTPError as http_err:
            logger.error(f"HTTP error occurred: {http_err} - Response: {response.text}")
            raise Exception(f"Binance API HTTP Error: {response.text}") from http_err
        except requests.exceptions.ConnectionError as conn_err:
            logger.error(f"Network Connection error occurred: {conn_err}")
            raise Exception("Network Error") from conn_err
        except Exception as err:
            logger.error(f"Unexpected error occurred: {err}")
            raise err

    def place_order(self, symbol: str, side: str, order_type: str, quantity: float, price: float = None, stop_price: float = None) -> dict:
        """
        Places an order on Binance Futures Testnet.
        """
        endpoint = "/fapi/v1/order"
        params = {
            "symbol": symbol.upper(),
            "side": side.upper(),
            "type": order_type.upper(),
            "quantity": quantity
        }

        if order_type.upper() in ["LIMIT", "STOP"]:
            params["price"] = price
            params["timeInForce"] = "GTC"
            
        if order_type.upper() in ["STOP_MARKET", "STOP"]:
            params["stopPrice"] = stop_price

        logger.info(f"Placing {order_type} {side} order for {quantity} {symbol}")
        return self._dispatch_request("POST", endpoint, params)
