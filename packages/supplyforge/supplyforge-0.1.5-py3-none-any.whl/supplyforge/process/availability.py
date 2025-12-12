"""
Module for processing unavailability data to calculate hourly availability.
"""

import logging

import polars as pl
from supplyforge import RESULTS_DIR

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def calculate_availability(country_code: str, year: int) -> None:
    """
    Calculates hourly availability per plant type as a share of installed capacity.

    Args:
        country_code: The two-letter country code.
        year: The year for which to process the data.
    """
    logger.info(f"Calculating availability for {country_code} for the year {year}...")

    # Define paths
    unavailability_file = RESULTS_DIR / "unavailability" / f"unavailability_{country_code}_{year}.parquet"
    installed_capacity_file = (
        RESULTS_DIR / "installed_capacities" / f"installed_capacities_{country_code}_{year}.parquet"
    )
    output_dir = RESULTS_DIR / "availability"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"availability_{country_code}_{year}.parquet"

    # Load data
    missing_input_data = False
    try:
        unavailability_df = pl.read_parquet(unavailability_file)
        installed_capacity_df = pl.read_parquet(installed_capacity_file)
    except:
        missing_input_data = True


    if missing_input_data or installed_capacity_df.is_empty() or unavailability_df.is_empty():
        logger.warning(f"Unavailability data for {country_code} {year} is empty. Skipping calculation.")
        # Create an empty dataframe with the correct schema and save it
        (
            pl.DataFrame(schema={
                "hour": pl.Datetime(time_unit='us', time_zone='UTC'),
                "plant_type": pl.String,
                "total_unavailable_capacity": pl.Float64,
                "installed_capacity": pl.Float64,
                "availability_share": pl.Float64
            })
            .write_parquet(output_file)
        )
        logger.info(f"Empty availability data frame saved to {output_file}")
        return

    # 1. Process Installed Capacity Data
    # Melt to long format. The column names from installed capacity become 'plant_type'.
    value_vars = [col for col in installed_capacity_df.columns if col != "index"]
    installed_capacity_long = (
        installed_capacity_df.unpivot(index="index", on=value_vars, variable_name="plant_type", value_name="installed_capacity")
        .group_by("plant_type")
        .agg(pl.sum("installed_capacity"))
    )

    # 2. Process Unavailability Data
    # Ensure datetime columns are in UTC
    unavailability_df = unavailability_df.with_columns(
        pl.col("start").dt.convert_time_zone("UTC"),
        pl.col("end").dt.convert_time_zone("UTC"),
    )

    # Calculate unavailable capacity for each event
    unavailability_df = unavailability_df.with_columns(
        (pl.col("nominal_power") - pl.col("avail_qty").cast(pl.Float64)).alias("unavailable_capacity")
    ).filter((pl.col("unavailable_capacity") > 0)
             & ((pl.col("docstatus").is_null()) | (pl.col("docstatus") != "Cancelled"))
             )

    # Create a complete hourly timeseries for the year in UTC
    hourly_range = pl.datetime_range(
        start=pl.datetime(year, 1, 1),
        end=pl.datetime(year, 12, 31, 23, 59, 59),
        interval="1h",
        time_zone="UTC",
        eager=True,
    ).alias("hour")

    # 3. Calculate total unavailable capacity per hour and plant type
    # This is more memory-efficient than creating a large grid first.
    # It expands each unavailability event into the hours it covers.
    total_unavailable_by_hour = (
        unavailability_df.lazy()
        .with_columns(
            # Group start/end to apply the function row-wise, creating a list of hours for each event.
            pl.struct(["start", "end"])
            .map_elements(lambda r: pl.datetime_range(r["start"], r["end"], "1h", time_zone="UTC", eager=True).to_list(), return_dtype=pl.List(pl.Datetime(time_zone="UTC")))
            .alias("hour")
        )
        .explode("hour") # Create a row for each hour in the list
        .group_by(["hour", "plant_type"])
        .agg(pl.sum("unavailable_capacity").alias("total_unavailable_capacity"))
        .collect()
    )

    # 4. Combine and Calculate Availability Share
    # Create a full grid of all hours and plant types, then join the results.
    grid = hourly_range.to_frame().join(installed_capacity_long.select("plant_type"), how="cross")
    availability_df = (
        grid.join(total_unavailable_by_hour, on=["hour", "plant_type"], how="left")
        .join(installed_capacity_long, on="plant_type", how="left")
        .with_columns(pl.col("total_unavailable_capacity").fill_null(0.0))
        .with_columns(
            (1 - (pl.col("total_unavailable_capacity") / pl.col("installed_capacity"))).alias("availability_share")
        )
        .filter(pl.col("installed_capacity") > 0)  # Avoid division by zero for types with no capacity
    )

    # Save result
    availability_df.write_parquet(output_file)
    logger.info(f"Availability data saved to {output_file}")


if __name__ == "__main__":
    try:
        calculate_availability(country_code=snakemake.params.country, year=int(snakemake.params.year))
    except NameError:
        logger.error("This script is intended to be run via Snakemake's 'script' directive.")