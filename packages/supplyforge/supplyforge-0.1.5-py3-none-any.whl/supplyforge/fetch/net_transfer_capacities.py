"""
Module for retrieving physical cross-border flow data from ENTSO-E.
"""

import logging
import os
from typing import List

import pandas as pd
import polars as pl
from dotenv import load_dotenv
load_dotenv()
from entsoe import EntsoePandasClient, exceptions
from entsoe.exceptions import NoMatchingDataError
from entsoe.mappings import NEIGHBOURS, lookup_area
from supplyforge import RESULTS_DIR

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# For some countries, ENTSO-E requires a specific bidding zone code
# for cross-border flow data, especially for historical queries.
# e.g., Germany was part of DE_LU bidding zone before October 2018.
COUNTRY_BIDDING_ZONE_MAPPING = {
    "DE": "DE_LU",
    "IE": "IE_SEM",
    "LU": "DE_LU"
}


def fetch_and_save_net_transfer_capacities(country_code: str, year: int) -> None:
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

    logger.info(f"Starting fetch for net transfer capacities for country: {original_country_code} (using code: {entsoe_country_code}), year: {year}")

    load_dotenv()
    api_token = os.getenv("ENTSOE_API_TOKEN")
    if not api_token:
        logger.error("ENTSOE_API_TOKEN environment variable not set.")
        raise ValueError("ENTSOE_API_TOKEN environment variable not set.")

    client = EntsoePandasClient(api_key=api_token)

    start = pd.Timestamp(f"{year}-01-01", tz="UTC")
    end = pd.Timestamp(f"{year}-12-31 23:59", tz="UTC")


    logger.info(f"Fetching net transfer capacities data for {entsoe_country_code} for the year {year}...")
    # Define output path and ensure the directory exists
    # We use the original country code for the output file to maintain consistency.
    output_dir = RESULTS_DIR / "net_transfer_capacities"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"net_transfer_capacities_{original_country_code}_{year}.parquet"
    try:
        # Fetch data from ENTSO-E (returns a pandas DataFrame)
        area = lookup_area(entsoe_country_code)
        netcs = []
        for neighbour in NEIGHBOURS[area.name]:
            try:
                netc = client.query_net_transfer_capacity_dayahead(
                    country_code_from=country_code,
                    country_code_to=neighbour,
                    end=end,
                    start=start
                )

            except NoMatchingDataError:
                continue
            netc.name = neighbour
            netcs.append(netc)


        if len(netcs) == 0:
            logger.warning(f"No net transfer capacities data returned for {country_code} for {year}.")
            output_file.touch()
            return

        df = pd.concat(netcs, axis=1, sort=True)
        df = df.tz_convert(area.tz)
        df = df.truncate(before=start, after=end)
        df = df.resample('h').first()

        logger.info("Successfully fetched data from ENTSO-E.")

        # Convert to Polars DataFrame
        flow_df_pl = pl.from_pandas(df)

        # Save the DataFrame
        flow_df_pl.write_parquet(output_file)
        logger.info(f"Data saved to {output_file}")

    except Exception as e:
        logger.warning(f"An error occurred while fetching data for {original_country_code} ({year}): {e}", exc_info=True)
        output_file.touch()



if __name__ == "__main__":
    try:
        fetch_and_save_net_transfer_capacities(
            country_code=snakemake.params.country, year=int(snakemake.params.year)
        )
    except NameError:
        fetch_and_save_net_transfer_capacities(
            country_code="FR", year=2022
        )
        logger.error("This script is intended to be run via Snakemake's 'script' directive.")