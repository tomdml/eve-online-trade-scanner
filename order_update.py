import pandas as pd
from pynput import keyboard
import pyperclip

import order_import
from price_differences import get_prices_from_station

def update_all(settings, session):

    orders = pd.read_csv(order_import.get_player_orders_file())
    orders.index = orders['typeID']
    orders.index = orders.index.rename('type_id')

    min_prices = get_prices_from_station(settings.dest_hub, settings.dest_order_type, settings.cache_all)
    # orders = orders[min_prices < orders['price']]
    orders['min_price'] = min_prices * 0.999

    def prepare():
        for typeID, price in orders['min_price'].iteritems():
            yield typeID, price

    p = prepare()

    def handle_paste():
        try:
            typeID, price = next(p)
        except StopIteration:
            return False

        print(f"got {typeID}")

        pyperclip.copy(str(price))

        params = {'type_id': typeID}
        res = session.post('https://esi.evetech.net/latest/ui/openwindow/marketdetails/', params=params)

        print(res.status_code)
    with keyboard.GlobalHotKeys({'<ctrl>+<space>': handle_paste}) as listener:
        listener.join()


if __name__ == '__main__':
    from settings import settings
    orders = pd.read_csv(order_import.get_player_orders_file())
    orders.index = orders['typeID']
    orders.index = orders.index.rename('type_id')

    min_prices = get_prices_from_station(settings.dest_hub, settings.dest_order_type, settings.cache_all)

    print(orders['price'].head(), min_prices.head())