import typer
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, FloatPrompt
from rich import print as rprint
from bot.orders import execute_order

app = typer.Typer(help="Binance Futures Testnet Trading Bot CLI")
console = Console()

@app.command()
def place_order(
    symbol: str = typer.Argument(None, help="Trading symbol (e.g., BTCUSDT). If empty, starts interactive mode."),
    side: str = typer.Argument(None, help="Order side (BUY or SELL)"),
    order_type: str = typer.Argument(None, help="Order type (MARKET, LIMIT, STOP_MARKET, STOP)"),
    quantity: float = typer.Argument(None, help="Quantity to trade"),
    price: float = typer.Option(None, "--price", "-p", help="Price (Required for LIMIT and STOP orders)"),
    stop_price: float = typer.Option(None, "--stop-price", "-s", help="Stop Price (Required for STOP_MARKET and STOP orders)")
):
    """
    Places an order on the Binance Futures Testnet.
    Run without arguments to start interactive mode.
    """
    if symbol is None:
        console.print("[bold cyan]Welcome to the Binance Futures Interactive Trading Bot![/bold cyan]")
        console.print("Let's place an order interactively.\n")
        
        symbol = Prompt.ask("Enter Trading Symbol", default="BTCUSDT").upper()
        side = Prompt.ask("Order Side", choices=["BUY", "SELL"], default="BUY")
        order_type = Prompt.ask("Order Type", choices=["MARKET", "LIMIT", "STOP_MARKET", "STOP"], default="MARKET")
        quantity = FloatPrompt.ask("Enter Quantity (e.g., 0.01)")
        
        if order_type in ["LIMIT", "STOP"]:
            price = FloatPrompt.ask("Enter Price")
            
        if order_type in ["STOP_MARKET", "STOP"]:
            stop_price = FloatPrompt.ask("Enter Stop Price")
            
        console.print("\n")
    elif not all([side, order_type, quantity]):
        console.print("[bold red]Error: If you provide a symbol, you must also provide SIDE, ORDER_TYPE, and QUANTITY as arguments.[/bold red]")
        console.print("Example: python cli.py BTCUSDT BUY MARKET 0.01")
        raise typer.Exit(code=1)
    console.print(f"[bold blue]Submitting Request...[/bold blue]")

    # Print Order Request Summary Table
    table = Table(title="Order Request Summary")
    table.add_column("Field", style="cyan")
    table.add_column("Value", style="magenta")

    table.add_row("Symbol", symbol.upper())
    table.add_row("Side", side.upper())
    table.add_row("Type", order_type.upper())
    table.add_row("Quantity", str(quantity))
    
    if price:
        table.add_row("Price", str(price))
    if stop_price:
        table.add_row("Stop Price", str(stop_price))

    console.print(table)

    # Execute Order
    result = execute_order(
        symbol=symbol,
        side=side,
        order_type=order_type,
        quantity=quantity,
        price=price,
        stop_price=stop_price
    )

    if result["success"]:
        console.print("\n[bold green]✅ Order Placed Successfully![/bold green]")
        
        data = result["data"]
        res_table = Table(title="Order Response Details")
        res_table.add_column("Field", style="cyan")
        res_table.add_column("Value", style="magenta")

        # Essential fields returned by Binance API for confirmation
        res_table.add_row("Order ID", str(data.get("orderId", "N/A")))
        res_table.add_row("Status", str(data.get("status", "N/A")))
        res_table.add_row("Executed Qty", str(data.get("executedQty", "N/A")))
        res_table.add_row("Average Price", str(data.get("avgPrice", "N/A")))

        console.print(res_table)
        console.print("[dim]Note: Check trading_bot.log for full API response details.[/dim]")

    else:
        # Print Failure
        console.print(f"\n[bold red]❌ Failed to Place Order:[/bold red] {result['message']}")
        console.print("[dim]Please check trading_bot.log for more detailed error logs.[/dim]")


if __name__ == "__main__":
    app()
