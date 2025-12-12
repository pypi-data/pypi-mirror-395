"""
Module for retrieving data from various sources.

This module provides functions to download, cache, and load data from various public sources,
primarily the ENTSO-E Transparency Platform.
"""

import logging
import os

import pandas as pd
import polars as pl
from entsoe import EntsoePandasClient
from entsoe.exceptions import NoMatchingDataError

from supplyforge import RESULTS_DIR
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)



def fetch_and_save_generation(country_code: str, year: int) -> None:
    """
    Fetches actual generation per production type from ENTSO-E for a given country and year,
    converts it to a Polars DataFrame, and saves it as a Parquet file.

    An ENTSO-E API token must be set in the `ENTSOE_API_TOKEN` environment variable.

    Args:
        country_code: The two-letter country code (e.g., 'DE', 'FR').
        year: The year for which to fetch the data.
    """
    logger.info(f"Starting fetch for country: {country_code}, year: {year}")

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
    output_dir = RESULTS_DIR / "generation"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"generation_{country_code}_{year}.parquet"

    logger.info(f"Fetching generation data for {country_code} for the year {year}...")
    try:
        # Fetch data from ENTSO-E (returns a pandas DataFrame)
        generation_df_pd = client.query_generation(country_code, start=start, end=end)
        logger.info("Successfully fetched data from ENTSO-E.")

        if generation_df_pd.empty:
            logger.warning(f"No generation data returned for {country_code} for {year}.")
            return

        # Convert to Polars DataFrame and reset index to make timestamp a column
        generation_df_pl = pl.from_pandas(generation_df_pd.reset_index())


        # Save the DataFrame
        generation_df_pl.write_parquet(output_file)
        logger.info(f"Data saved to {output_file}")

    except NoMatchingDataError:
        output_file.touch()
    except Exception as e:

        logger.error(f"An error occurred while fetching data for {country_code} ({year}): {e}", exc_info=True)
        raise

# This block is executed when the script is called directly by Snakemake's `script` directive.
# It accesses the 'snakemake' object that Snakemake automatically injects.
if __name__ == "__main__":
    try:
        # The 'snakemake' object is globally available in scripts run via the script directive
        fetch_and_save_generation(
            country_code=snakemake.params.country, year=int(snakemake.params.year)
        )
    except NameError:
        logger.error("This script is intended to be run via Snakemake's 'script' directive.")
