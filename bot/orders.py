from bot.client import BinanceFuturesClient
from bot.validators import validate_order_input
from bot.logging_config import logger

def execute_order(symbol: str, side: str, order_type: str, quantity: float, price: float = None, stop_price: float = None):
    """
    Validates input and executes an order using BinanceFuturesClient.
    """
    try:
        # Validate User Input
        validate_order_input(
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price,
            stop_price=stop_price
        )
        
        # Initialize Client
        # Expects BINANCE_API_KEY and BINANCE_API_SECRET in the environment
        client = BinanceFuturesClient()

        logger.info(f"Client Initialized. Attempting to place order: {symbol} | {side} | {order_type}")
        
        # Place Order
        response = client.place_order(
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price,
            stop_price=stop_price
        )

        return {
            "success": True,
            "message": "Order placed successfully!",
            "data": response
        }

    except ValueError as ve:
        logger.error(f"Validation Error: {str(ve)}")
        return {"success": False, "message": f"Validation Error: {str(ve)}", "data": None}
    except Exception as e:
        logger.error(f"Order Execution Failed: {str(e)}")
        return {"success": False, "message": f"Order Failed: {str(e)}", "data": None}
