"""
Module for retrieving aggregate water reservoirs and hydro storage data from ENTSO-E.
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


def fetch_and_save_hydro_storage(country_code: str, year: int) -> None:
    """
    Fetches aggregate water reservoirs and hydro storage from ENTSO-E for a given
    country and year, converts it to a Polars DataFrame, and saves it as a Parquet file.

    An ENTSO-E API token must be set in the `ENTSOE_API_TOKEN` environment variable.

    Args:
        country_code: The two-letter country code (e.g., 'DE', 'FR').
        year: The year for which to fetch the data.
    """
    logger.info(f"Starting fetch for hydro storage for country: {country_code}, year: {year}")

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

    logger.info(f"Fetching hydro storage data for {country_code} for the year {year}...")
    hydro_df_pl = None
    try:
        # Fetch data from ENTSO-E (returns a pandas DataFrame)
        hydro_df_pd = client.query_aggregate_water_reservoirs_and_hydro_storage(
            country_code, start=start, end=end
        )

        if hydro_df_pd is not None and not hydro_df_pd.empty:
            logger.info("Successfully fetched data from ENTSO-E.")
            # Convert pandas Series to a DataFrame and reset the index
            hydro_df_pd = hydro_df_pd.reset_index()
            # Convert to Polars DataFrame and reset index to make timestamp a column
            hydro_df_pl = pl.from_pandas(hydro_df_pd).rename(
                {"index": "timestamp", str(hydro_df_pd.columns[1]): "storage_mwh"}
            )

    except exceptions.NoMatchingDataError:
        logger.warning(f"No hydro storage data found on ENTSO-E for {country_code} for {year}.")
    except Exception as e:
        logger.error(f"An error occurred while fetching data for {country_code} ({year}): {e}", exc_info=True)
        raise

    if hydro_df_pl is None:
        logger.info(f"Creating an empty parquet file for {country_code} for {year}.")
        hydro_df_pl = pl.DataFrame(
            schema={"timestamp": pl.Datetime(time_unit="us", time_zone="UTC"), "storage_mwh": pl.Float64}
        )

    # Define output path and ensure the directory exists
    output_dir = RESULTS_DIR / "hydro_storage"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"hydro_storage_{country_code}_{year}.parquet"

    # Save the DataFrame (either with data or empty)
    hydro_df_pl.write_parquet(output_file)
    logger.info(f"Data saved to {output_file}")

if __name__ == "__main__":
    try:
        fetch_and_save_hydro_storage(
            country_code=snakemake.params.country, year=int(snakemake.params.year)
        )
    except NameError:
        logger.error("This script is intended to be run via Snakemake's 'script' directive.")