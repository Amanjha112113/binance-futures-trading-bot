from bot.logging_config import logger

def validate_order_input(symbol: str, side: str, order_type: str, quantity: float, price: float = None, stop_price: float = None):
    """
    Validates user input for placing an order.
    """
    side = side.upper()
    order_type = order_type.upper()
    symbol = symbol.upper()

    if side not in ["BUY", "SELL"]:
        raise ValueError("Side must be 'BUY' or 'SELL'.")

    # Add STOP_MARKET and STOP for bonus requirements
    if order_type not in ["MARKET", "LIMIT", "STOP_MARKET", "STOP"]:
        raise ValueError("Order type must be 'MARKET', 'LIMIT', 'STOP_MARKET', or 'STOP'.")

    if quantity <= 0:
        raise ValueError("Quantity must be greater than 0.")

    if order_type in ["LIMIT", "STOP"]:
        if price is None or price <= 0:
            raise ValueError("Price is required and must be > 0 for LIMIT and STOP orders.")
            
    if order_type in ["STOP_MARKET", "STOP"]:
        if stop_price is None or stop_price <= 0:
            raise ValueError("Stop price is required and must be > 0 for STOP_MARKET and STOP (Stop-Limit) orders.")

    return True
