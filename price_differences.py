import pandas as pd

import order_data
import historical_data
import order_import
import render
from sde_utils import get_item_names, get_item_sizes


def get_prices_from_station(station_name, order_type, cached) -> pd.Series:
    # Get orders as JSON
    print(f'Loading {order_type} orders from {station_name} using {"cached data" if cached else "ESI"}...')
    orders_json = order_data.get_all_orders(station_name, order_type, cached)
    print(f'Got {len(orders_json)} orders!')

    # Convert to DF and find minimum price per typeID
    df = pd.DataFrame.from_records(orders_json)
    return df.groupby('type_id')['price'].min()  # pd.Series


def get_volume_price_history(station_name, typeIDs, days, cached) -> tuple[pd.Series]:
    """Get historical data for each given typeID"""

    idx = pd.IndexSlice

    print(f'Loading market history in {station_name} for {len(typeIDs)} items...')
    history_json = historical_data.get_all_history(station_name, typeIDs, cached=cached)
    print('Success!')

    print(f'Processing history content into database...')
    typeID_history_dict = {
        typeID: pd.DataFrame.from_records(data, index=['date'])
        for typeID, data
        in history_json.items()
    }

    historical_df = pd.concat(typeID_history_dict, axis=1).T
    historical_df = historical_df.drop('date', axis='columns')
    historical_df.columns = pd.to_datetime(historical_df.columns, yearfirst=True)
    print('Done!')

    print(f'Pulling out historical volume data for {days} days:')
    v = historical_df.loc[idx[:, 'volume'], historical_df.columns > (pd.Timestamp('today').floor('D') - pd.offsets.Day(days))]
    v = v.fillna(0).mean(axis=1)
    v = v.droplevel(1, axis=0)

    print(f'Pulling out historical price data for {days} days:')
    p = historical_df.loc[idx[:, 'average'], historical_df.columns > (pd.Timestamp('today').floor('D') - pd.offsets.Day(days))]
    p = p.mean(axis=1)
    p = p.droplevel(1, axis=0)

    print('Done!')
    return v, p


def price_differences(settings):

    print('Loading Static Data Export mappings...', end=' ')
    typeIDs_to_names = get_item_names()
    typeIDs_to_sizes = get_item_sizes()
    print('Done!')

    # Results DataFrame
    summary = pd.DataFrame()

    # Order Series
    source_prices = get_prices_from_station(settings.source_hub, settings.source_order_type, settings.cache_all)
    dest_prices = get_prices_from_station(settings.dest_hub, settings.dest_order_type, settings.cache_all)

    # Sell-side costs: Broker fees (~3.5%), Sales tax (~2.25%), Hauling fees (~2%).
    dest_prices_taxed = dest_prices * ((1 - 0.035 - 0.0225) * (1 - 0.02))

    # Series back into output DF columns
    summary['Product Cost'] = source_prices
    summary['Product Revenue'] = dest_prices_taxed
    summary['Profit'] = summary['Product Revenue'] - summary['Product Cost']
    summary['Margin'] = summary['Profit'] / summary['Product Cost']

    # Get historical volume and price for order refinement
    volume, price = get_volume_price_history(settings.dest_hub, summary.index, settings.days_history, settings.cache_all)

    summary['Mean Volume'] = volume

    # Remove orders where the ratio of current price to historic price is too high
    summary = summary[(summary['Product Revenue'] / price) < settings.bogus_threshold]

    # Finally, calculate expected profit per item by multiplying trade profit by mean volume
    summary['Total Profit'] = summary['Profit'] * summary['Mean Volume']

    # Clean up by dropping NAN rows - Usually this means no volume data or no sell-side orders.
    summary = summary.dropna()

    # Find out which items are already being traded by the player
    player_orders_df = pd.read_csv(order_import.get_player_orders_file())
    player_orders_set = set(player_orders_df['typeID'])
    summary['Already Selling'] = summary.index.isin(player_orders_set)

    if settings.hide_existing:
        summary = summary[~summary['Already Selling']]
        summary = summary.drop('Already Selling', axis=1)

    # Calculate item volume required to fulfil daily sale volume
    summary['Haul Size'] = summary['Mean Volume'] * summary.index.map(typeIDs_to_sizes)

    # Sort by profit descending for output
    summary = summary.sort_values(by='Total Profit', ascending=False)

    # Use item names instead of typeIDs
    summary['typeID'] = summary.index
    summary = summary.rename(typeIDs_to_names)

    # Output to a pretty table and return URL for further use
    url = render.render_to_html(summary)
    return url
