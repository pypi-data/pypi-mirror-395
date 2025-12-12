"""
Module for retrieving day-ahead price data from ENTSO-E.
"""

import logging
import os

import pandas as pd
import polars as pl
from dotenv import load_dotenv
from entsoe import EntsoePandasClient, exceptions
from supplyforge import RESULTS_DIR

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# For some countries, ENTSO-E requires a specific bidding zone code
# for day-ahead prices, especially for historical queries.
# e.g., Germany was part of DE_LU bidding zone before October 2018.
# For countries with multiple bidding zones, provide a list of codes.
# The script will fetch data for all zones and average the prices.
# Example for Italy (not exhaustive): IT: ["IT_NORD", "IT_CNOR", "IT_CSUD", "IT_SUD"]
COUNTRY_BIDDING_ZONE_MAPPING = {
    "DE": ["DE_LU"],
    "IT": [
        "IT_NORD", "IT_CNOR", "IT_CSUD", "IT_SUD",
        "IT_SICI", "IT_SARD", "IT_CALA"
    ],
}


def fetch_and_save_day_ahead_prices(country_code: str, year: int) -> None:
    """
    Fetches day-ahead prices from ENTSO-E for a given country and year,
    converts it to a Polars DataFrame, and saves it as a Parquet file.

    An ENTSO-E API token must be set in the `ENTSOE_API_TOKEN` environment variable.

    Args:
        country_code: The two-letter country code (e.g., 'DE', 'FR').
        year: The year for which to fetch the data.
    """
    original_country_code = country_code
    # Use a more specific bidding zone if required by ENTSO-E for the query
    # If no mapping exists, use the country code itself in a list.
    entsoe_bidding_zones = COUNTRY_BIDDING_ZONE_MAPPING.get(country_code, [country_code])

    logger.info(
        f"Starting fetch for day-ahead prices for country: {original_country_code} (using zones: {entsoe_bidding_zones}), year: {year}"
    )

    # Load environment variables from .env file
    load_dotenv()
    api_token = os.getenv("ENTSOE_API_TOKEN")
    if not api_token:
        logger.error("ENTSOE_API_TOKEN environment variable not set.")
        raise ValueError("ENTSOE_API_TOKEN environment variable not set.")

    client = EntsoePandasClient(api_key=api_token, retry_delay=60, retry_count=10, timeout=360)

    # Define the time range for the entire year in UTC
    start = pd.Timestamp(f"{year}-01-01", tz="UTC")
    end = pd.Timestamp(f"{year}-12-31 23:59", tz="UTC")

    logger.info(f"Fetching day-ahead prices for {original_country_code} for the year {year}...")
    prices_df_pl = None
    try:
        all_prices_series = []
        for zone in entsoe_bidding_zones:
            try:
                logger.info(f"Querying bidding zone: {zone}")
                # Fetch data from ENTSO-E (returns a pandas Series)
                prices_pd = client.query_day_ahead_prices(zone, start=start, end=end)
                prices_pd = prices_pd.to_frame()
                prices_pd["bidding_zone"] = zone
                if prices_pd is not None and not prices_pd.empty:
                    all_prices_series.append(prices_pd)
            except exceptions.NoMatchingDataError:
                logger.warning(f"No day-ahead price data found on ENTSO-E for bidding zone {zone} for {year}.")

        if all_prices_series:
            logger.info("Successfully fetched data from ENTSO-E.")
            if len(all_prices_series) > 1:
                logger.info(f"Averaging prices across {len(all_prices_series)} bidding zones.")
                # Concatenate into a DataFrame and calculate the mean price across zones for each timestamp
                prices_pd = pd.concat(all_prices_series, axis=0)
            else:
                prices_pd = all_prices_series[0]

            # Convert pandas Series to a DataFrame and reset the index
            prices_df_pd = prices_pd.reset_index()
            # Convert to Polars DataFrame and rename columns
            prices_df_pl = pl.from_pandas(prices_df_pd).rename({"index": "timestamp", "0": "price_eur_per_mwh"})

    except exceptions.NoMatchingDataError:
        logger.warning(f"No day-ahead price data found on ENTSO-E for any specified zone in {original_country_code} for {year}.")
    except Exception as e:
        logger.error(f"An error occurred while fetching data for {original_country_code} ({year}): {e}", exc_info=True)
        raise

    if prices_df_pl is None:
        logger.info(f"Creating an empty parquet file for {original_country_code} for {year}.")
        prices_df_pl = pl.DataFrame(
            schema={"timestamp": pl.Datetime(time_unit="us", time_zone="UTC"), "price_eur_per_mwh": pl.Float64}
        )

    # Define output path and ensure the directory exists
    # We use the original country code for the output file to maintain consistency.
    output_dir = RESULTS_DIR / "day_ahead_prices"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"day_ahead_prices_{original_country_code}_{year}.parquet"

    # Save the DataFrame (either with data or empty)
    prices_df_pl.write_parquet(output_file)
    logger.info(f"Data saved to {output_file}")

if __name__ == "__main__":
    try:
        fetch_and_save_day_ahead_prices(
            country_code=snakemake.params.country, year=int(snakemake.params.year)
        )
    except NameError:
        logger.info("This script is intended to be run via Snakemake's 'script' directive. Here it is a standalone"
                    "for testing purposes.")

        fetch_and_save_day_ahead_prices(
            country_code="ES", year=2021
        )