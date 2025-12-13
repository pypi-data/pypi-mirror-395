from datetime import date, timedelta

from kpler.sdk import Platform
from kpler.sdk.configuration import Configuration
from kpler.sdk.resources.trades import Trades


config = Configuration(Platform.Liquids, "<your email>", "<your password>")

trades_client = Trades(config)

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
    ],
)
