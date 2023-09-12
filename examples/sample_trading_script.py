from time import sleep

from strategies.previous_day_trend_strategy import PreviousDayTrendStrategy
from utils import init_mt5

from art_trader.mt5.common import MT5Strategy, MT5Symbol
from art_trader.mt5.trading import MT5Account, MT5Trader


class DemoTrader(MT5Trader):
    """
    This trader executes its strategy whenever there isn't an existing
    order (pending or open) for that asset. So whenever a trade is closed,
    a new one is executed.

    By defining your own methods, such as self.do(), you can design your own
    trade execution logic whithout worrying about compatibility issues with
    the broker.

    Attributes:
        strategy (MT5Strategy): The trading strategy to be used.
        tickers (list[str]): List of tickers to trade.
    """

    def __init__(self, strategy: MT5Strategy, tickers: list[str]):
        self.strategy = strategy
        self.symbols = [MT5Symbol(x) for x in tickers]

    def do(self):
        for symbol in self.symbols:
            # Get open and pending orders for the current symbol
            open_orders = self.get_open_orders(symbol)
            pending_orders = self.get_pending_orders(symbol)

            # If there are no open or pending orders, place a new order
            if not pending_orders and not open_orders:
                self.send(self.trade(symbol))


def main():

    # Initialize MT5 connection
    init_mt5(login=None, password=None, server="AdmiralMarkets-Demo")

    # Create the Trader instance
    demo_trader = DemoTrader(PreviousDayTrendStrategy(), ["EURUSD-Z"])

    # Create an MT5Account object if you'd like to monitor your account.
    # You could also pass this object to your trader or strategy if live
    # account data is required for your trading logic or strategy.
    demo_account = MT5Account()

    # Start trading; execute the trading logic every 60 seconds
    while True:
        demo_trader.do()
        print(demo_account)
        sleep(60)


if __name__ == '__main__':
    main()
