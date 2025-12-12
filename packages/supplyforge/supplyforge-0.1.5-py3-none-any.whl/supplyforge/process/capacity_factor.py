"""
Module for calculating hourly capacity factors for generation technologies.
"""

import logging

import polars as pl
from supplyforge import RESULTS_DIR

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def calculate_intermittent_capacity_factors(country_code: str, year: int) -> None:
    """
    Calculates the hourly capacity factor for intermittent renewable generation types.

    The capacity factor is the actual hourly generation as a share of the
    total installed capacity for that generation type.

    Args:
        country_code: The two-letter country code.
        year: The year for which to process the data.
    """
    logger.info(f"Calculating capacity factors for {country_code} for the year {year}...")

    # Define paths
    generation_file = RESULTS_DIR / "generation" / f"generation_{country_code}_{year}.parquet"
    installed_capacity_file = (
        RESULTS_DIR / "installed_capacities" / f"installed_capacities_{country_code}_{year}.parquet"
    )
    output_dir = RESULTS_DIR / "capacity_factors"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"capacity_factors_{country_code}_{year}.parquet"

    # Load data
    try:
        generation_df = pl.read_parquet(generation_file)
        installed_capacity_df = pl.read_parquet(installed_capacity_file)
    except:
        logger.warning(f"Input file not found. Skipping calculation.")
        output_file.touch()
        return None

    # 1. Clean and filter generation column names.
    # We are only interested in 'Actual Aggregated' generation.
    # The original column names are tuples, e.g., ('Solar', 'Actual Aggregated').
    cleaned_columns = {}
    for col in generation_df.columns:
        col_str = str(col) 
        if "('index'" in col_str:
            cleaned_columns[col] = "index"
        elif "'Actual Aggregated'" in col_str:
            # Extract the plant type, e.g., 'Solar' from "('Solar', 'Actual Aggregated')"
            plant_type = col_str.split("'")[1]
            cleaned_columns[col] = plant_type

    generation_df = generation_df.rename(cleaned_columns)

    if generation_df.is_empty() or installed_capacity_df.is_empty():
        logger.warning(
            f"Generation or installed capacity data for {country_code} {year} is empty. "
            "Cannot calculate capacity factors."
        )
        output_file.touch()
        return None


    # 2. Process Installed Capacity Data
    # Unpivot to long format and aggregate total capacity per plant type.
    value_vars = [col for col in installed_capacity_df.columns if col != "index"]
    installed_capacity_long = (
        installed_capacity_df.unpivot(index="index", on=value_vars, variable_name="plant_type", value_name="installed_capacity")
        .group_by("plant_type")
        .agg(pl.sum("installed_capacity"))
    )

    # 3. Process Generation Data
    # Unpivot to long format to get (timestamp, plant_type, generation_mw).
    intermittent_types = ["Solar", "Wind Offshore", "Wind Onshore", "Hydro Run-of-river and poundage"]
    # Filter for columns that are in our intermittent list
    value_cols = [col for col in generation_df.columns if col in intermittent_types]

    generation_long = generation_df.unpivot(
        index="index", on=value_cols, variable_name="plant_type", value_name="generation_mw"
    ).rename({"index": "hour"}).with_columns(pl.col("hour").dt.convert_time_zone("UTC"))

    # 4. Combine and Calculate Capacity Factor
    # Join generation data with aggregated installed capacity.
    capacity_factors_df = (
        generation_long.join(installed_capacity_long, on="plant_type", how="left")
        .with_columns(
            # Calculate capacity factor, handling cases with zero capacity to avoid division errors.
            pl.when(pl.col("installed_capacity") > 0)
            .then(pl.col("generation_mw") / pl.col("installed_capacity"))
            .otherwise(0.0)
            .alias("capacity_factor")
        )
        .filter(pl.col("installed_capacity").is_not_null()) # Only keep types with capacity data
    )
    capacity_factors_df = (
        capacity_factors_df
        .sort(["plant_type", "hour"])
        .group_by_dynamic(
            index_column="hour",
            every="1h",     # resample frequency
            period="1h",     # window size
            group_by="plant_type"
        )
        .agg([
            pl.col("capacity_factor").mean(),
            pl.col("installed_capacity").first(),
            pl.col("generation_mw").mean(),
        ])
    )
    # Save result
    capacity_factors_df.write_parquet(output_file)
    logger.info(f"Capacity factor data saved to {output_file}")


if __name__ == "__main__":
    try:
        calculate_intermittent_capacity_factors(
            country_code=snakemake.params.country, year=int(snakemake.params.year)
        )
    except NameError:
        logger.error("This script is intended to be run via Snakemake's 'script' directive. Running with test values.")

        calculate_intermittent_capacity_factors(
            country_code="ES", year=2024
        )