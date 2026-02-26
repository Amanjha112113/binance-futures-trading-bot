# Binance Futures Testnet Trading Bot

This is a Python application that can place orders on the Binance Futures Testnet (USDT-M). It provides a clean, reusable structure with proper logging and exception handling.

## Features
- Place Market, Limit, Stop Market, and Stop (Stop-Limit) orders (Bonus)
- Support for BUY and SELL
- Input validation
- Structured project layout separating API client, validation, and CLI logic
- Logging of all requests, responses, and errors to `trading_bot.log`
- Enhanced Interactive CLI UX using `Typer` and `Rich` to show nice formatted output, menus, and prompts (Bonus)

## Project Structure
```text
trading_bot/
  bot/
    __init__.py
    client.py        # Binance API REST client wrapper
    orders.py        # Order execution/handling logic
    validators.py    # Input validation logic
    logging_config.py# Logger setup
  cli.py             # Command-line entry point
  requirements.txt
  .env               # API credentials (Create this file)
  README.md
```

## Setup Steps

1. **Clone the repository or extract the zip folder:**
   ```bash
   cd trading_bot
   ```

2. **Create a virtual environment (Optional but Recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API Credentials:**
   Create a `.env` file in the root directory (where `cli.py` is located) and add your Binance Futures Testnet API Key and Secret:
   ```env
   BINANCE_API_KEY=your_api_key_here
   BINANCE_API_SECRET=your_api_secret_here
   ```
   > You can register and generate these on [Binance Futures Testnet](https://testnet.binancefuture.com/).

## How to Run Examples

Use the `cli.py` script to interact with the bot.

**1. Run Interactive Mode (Bonus Requirement):**
Simply run the CLI without arguments to start the interactive prompt:
```bash
python cli.py
```

**2. View Help and Options:**
```bash
python cli.py --help
```

**2. Place a MARKET order:**
```bash
python cli.py BTCUSDT BUY MARKET 0.01 
```

**3. Place a LIMIT order:**
```bash
python cli.py BTCUSDT SELL LIMIT 0.05 --price 95000.0
```

**5. Place a STOP_MARKET order (Bonus Requirement):**
```bash
python cli.py BTCUSDT BUY STOP_MARKET 0.02 --stop-price 92000.0
```

**6. Place a STOP (Stop-Limit) order (Bonus Requirement):**
```bash
python cli.py BTCUSDT SELL STOP 0.05 --price 95000.0 --stop-price 92000.0
```

## Assumptions
- The user will have valid Testnet balances to fulfill the requested orders.
- The minimum order sizes and nominal value requirements of Binance Futures apply. If an order fails, check the `trading_bot.log` file for `API Response`.

## Error Handling
If you provide invalid input (e.g., negative quantity, missing price for Limit orders), the input validation block will catch it before making the API call. If Binance rejects the order or a network error occurs, the bot gracefully logs it and prints a summary.
