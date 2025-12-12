"""
Module for retrieving unavailability of generation units data from ENTSO-E.
"""

import logging
import os

import pandas as pd
import polars as pl
import requests
from dotenv import load_dotenv
load_dotenv()
from entsoe import EntsoePandasClient
from entsoe.exceptions import NoMatchingDataError

from supplyforge import RESULTS_DIR

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# For some countries, ENTSO-E requires a specific bidding zone code
# for unavailability data, especially for historical queries.
# e.g., Germany was part of DE_LU bidding zone before October 2018.
COUNTRY_BIDDING_ZONE_MAPPING = {
    "DE": "DE_LU",
}


def fetch_and_save_unavailability(country_code: str, year: int) -> None:
    """
    Fetches unavailability of generation units from ENTSO-E for a given country and year,
    converts it to a Polars DataFrame, and saves it as a Parquet file.

    An ENTSO-E API token must be set in the `ENTSOE_API_TOKEN` environment variable.

    Args:
        country_code: The two-letter country code (e.g., 'DE', 'FR').
        year: The year for which to fetch the data.
    """
    original_country_code = country_code
    # Use a more specific bidding zone if required by ENTSO-E for the query
    entsoe_country_code = COUNTRY_BIDDING_ZONE_MAPPING.get(country_code, country_code)

    logger.info(f"Starting fetch for unavailability for country: {original_country_code} (using code: {entsoe_country_code}), year: {year}")

    # Load environment variables from .env file
    load_dotenv()
    api_token = os.getenv("ENTSOE_API_TOKEN")
    if not api_token:
        logger.error("ENTSOE_API_TOKEN environment variable not set.")
        raise ValueError("ENTSOE_API_TOKEN environment variable not set.")

    client = EntsoePandasClient(api_key=api_token)

    # Define the time range for the entire year in UTC
    start = pd.Timestamp(f"{year}-01-01", tz="UTC")
    end = pd.Timestamp(f"{year}-12-31 23:59", tz="UTC")

    # Define output path and ensure the directory exists
    # We use the original country code for the output file to maintain consistency.
    output_dir = RESULTS_DIR / "unavailability"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"unavailability_{original_country_code}_{year}.parquet"

    logger.info(f"Fetching unavailability data for {entsoe_country_code} for the year {year}...")
    try:
        # Fetch data from ENTSO-E (returns a pandas DataFrame)
        unavailability_df_pd = client.query_unavailability_of_generation_units(
            entsoe_country_code, start=start, end=end
        )
        logger.info("Successfully fetched data from ENTSO-E.")

        if unavailability_df_pd.empty:
            logger.warning(f"No unavailability data returned for {country_code} for {year}.")
            return

        # Convert to Polars DataFrame
        unavailability_df_pl = pl.from_pandas(unavailability_df_pd)


        # Save the DataFrame
        unavailability_df_pl.write_parquet(output_file)
        logger.info(f"Data saved to {output_file}")
    except requests.exceptions.HTTPError as e:
        output_file.touch()
    except NoMatchingDataError:
        output_file.touch()
    except Exception as e:
        logger.error(f"An error occurred while fetching data for {original_country_code} ({year}): {e}", exc_info=True)
        raise

if __name__ == "__main__":
    try:
        fetch_and_save_unavailability(
            country_code=snakemake.params.country, year=int(snakemake.params.year)
        )
    except NameError:
        logger.error("This script is intended to be run via Snakemake's 'script' directive.")