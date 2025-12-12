"""
Module for retrieving physical cross-border flow data from ENTSO-E.
"""

import logging
import os
from typing import List

import pandas as pd
import polars as pl
from dotenv import load_dotenv
from entsoe import EntsoePandasClient, exceptions
from entsoe.mappings import NEIGHBOURS
from supplyforge import RESULTS_DIR

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# For some countries, ENTSO-E requires a specific bidding zone code
# for cross-border flow data, especially for historical queries.
# e.g., Germany was part of DE_LU bidding zone before October 2018.
COUNTRY_BIDDING_ZONE_MAPPING = {
    "DE": "DE_LU",
}


def fetch_and_save_crossborder_flows(country_code: str, year: int) -> None:
    """
    Fetches physical cross-border flows from ENTSO-E for a given country and all its
    neighbors for a specific year, combines them, converts to a Polars DataFrame,
    and saves as a Parquet file.

    An ENTSO-E API token must be set in the `ENTSOE_API_TOKEN` environment variable.

    Args:
        country_code: The two-letter country code (e.g., 'DE', 'FR').
        year: The year for which to fetch the data.
    """
    original_country_code = country_code
    # Use a more specific bidding zone if required by ENTSO-E for the query
    entsoe_country_code = COUNTRY_BIDDING_ZONE_MAPPING.get(original_country_code, original_country_code)

    logger.info(f"Starting fetch for cross-border flows for country: {original_country_code} (using code: {entsoe_country_code}), year: {year}")

    load_dotenv()
    api_token = os.getenv("ENTSOE_API_TOKEN")
    if not api_token:
        logger.error("ENTSOE_API_TOKEN environment variable not set.")
        raise ValueError("ENTSOE_API_TOKEN environment variable not set.")

    client = EntsoePandasClient(api_key=api_token)

    start = pd.Timestamp(f"{year}-01-01", tz="UTC")
    end = pd.Timestamp(f"{year}-12-31 23:59", tz="UTC")


    # Define output path and ensure the directory exists
    # We use the original country code for the output file to maintain consistency.
    output_dir = RESULTS_DIR / "crossborder_flows"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"crossborder_flows_{original_country_code}_{year}.parquet"
    logger.info(f"Fetching cross border flow data for {entsoe_country_code} for the year {year}...")
    try:
        # Fetch data from ENTSO-E (returns a pandas DataFrame)
        flow_df_pd = client.query_physical_crossborder_allborders(entsoe_country_code,
                                                                  start=start,
                                                                  end=end,
                                                                  export=False,
                                                                  per_hour=True)
        logger.info("Successfully fetched data from ENTSO-E.")

        if flow_df_pd.empty:
            logger.warning(f"No cross border flow data returned for {country_code} for {year}.")
            return

        # Convert to Polars DataFrame
        flow_df_pl = pl.from_pandas(flow_df_pd)


        # Save the DataFrame
        flow_df_pl.write_parquet(output_file)
        logger.info(f"Data saved to {output_file}")

    except NoMatchingDataError:
        output_file.touch()
    except Exception as e:
        logger.error(f"An error occurred while fetching data for {original_country_code} ({year}): {e}", exc_info=True)
        raise


if __name__ == "__main__":
    try:
        fetch_and_save_crossborder_flows(
            country_code=snakemake.params.country, year=int(snakemake.params.year)
        )
    except NameError:
        logger.error("This script is intended to be run via Snakemake's 'script' directive.")