The Kpler Python SDK provides access to Kpler data.

It can be easily integrated into notebooks, scripts, and applications.

It is available to all Kpler API clients (credentials required)

Documentation : https://python-sdk.dev.kpler.com

````python
from kpler.sdk import Platform
from kpler.sdk.configuration import Configuration
from kpler.sdk.resources.trades import Trades
from datetime import date, timedelta

# Create configuration object
configuration = Configuration(Platform.Liquids, "<your email>", "<your password>")

# To change the platform use _change_platform method of Configuration class
configuration._change_platform(Platform.Liquids)

# Connect to one of the Kpler's client using your configuration object, ie: Trades
trades_client = Trades(configuration)

# Get all possible columns returned by the get_trades query
trades_columns = trades_client.get_columns()

# Do a get trades with default columns and with a maximum size of 5 for the dataframe
trades_df = trades_client.get(size=5)

# Get US imports over last week
us_imports = trades_client.get(
    to_zones=["United States"],
    products=["crude"],
    with_forecast=False,
    with_intra_country=True,
    start_date=date.today() - timedelta(days=7),
    columns=[
        "vessel_name",
        "closest_ancestor_product",
        "closest_ancestor_grade",
        "start",
        "end",
        "origin_location_name",
        "destination_location_name",
    ]
)

````
