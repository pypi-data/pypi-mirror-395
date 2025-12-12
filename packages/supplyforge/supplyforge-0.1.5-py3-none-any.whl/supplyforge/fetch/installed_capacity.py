"""
Module for retrieving installed capacity data from ENTSO-E.
"""

import logging
import os

import pandas as pd
import polars as pl
from dotenv import load_dotenv
from entsoe import EntsoePandasClient
from entsoe.exceptions import NoMatchingDataError

from supplyforge import RESULTS_DIR

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def fetch_and_save_installed_capacity(country_code: str, year: int) -> None:
    """
    Fetches installed generation capacity from ENTSO-E for a given country and year,
    converts it to a Polars DataFrame, and saves it as a Parquet file.

    An ENTSO-E API token must be set in the `ENTSOE_API_TOKEN` environment variable.

    Args:
        country_code: The two-letter country code (e.g., 'DE', 'FR').
        year: The year for which to fetch the data.
    """
    logger.info(f"Starting fetch for installed capacity for country: {country_code}, year: {year}")

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
    output_dir = RESULTS_DIR / "installed_capacities"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"installed_capacities_{country_code}_{year}.parquet"

    logger.info(f"Fetching installed capacity data for {country_code} for the year {year}...")
    try:
        # Fetch data from ENTSO-E (returns a pandas DataFrame)
        installed_capacity_df_pd = client.query_installed_generation_capacity(
            country_code, start=start, end=end, psr_type=None
        )
        logger.info("Successfully fetched data from ENTSO-E.")

        if installed_capacity_df_pd.empty:
            logger.warning(f"No installed capacity data returned for {country_code} for {year}.")
            output_file.touch()
            return

        # Convert to Polars DataFrame and reset index to make timestamp a column
        installed_capacity_df_pl = pl.from_pandas(installed_capacity_df_pd.reset_index())

        # Save the DataFrame
        installed_capacity_df_pl.write_parquet(output_file)
        logger.info(f"Data saved to {output_file}")
    except NoMatchingDataError:
        output_file.touch()
    except Exception as e:
        logger.error(f"An error occurred while fetching data for {country_code} ({year}): {e}", exc_info=True)
        raise

if __name__ == "__main__":
    try:
        fetch_and_save_installed_capacity(
            country_code=snakemake.params.country, year=int(snakemake.params.year)
        )
    except NameError:
        logger.error("This script is intended to be run via Snakemake's 'script' directive.")