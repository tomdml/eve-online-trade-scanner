import glob
import os


def get_player_orders_file():
    path = glob.glob(os.path.expanduser(os.path.join('~', 'Documents', 'EVE', 'logs', 'Marketlogs', '*')))

    latest_log = max(path, key=os.path.getctime)
    return latest_log
