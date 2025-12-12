from supplyforge import RESULTS_DIR, PACKAGE_DIR
import polars as pl
import yaml
import logging
logging.basicConfig(level=logging.INFO)

def load_and_merge_eraa_data(country_code: str):

    """
    Loads ERAA capacity factor CSV files for a given country, processes them,
    and saves the merged data into a yearly Parquet file.

    This function processes data for multiple technologies and weather scenarios,
    unpivots the data, and aggregates it, using Polars' lazy API for memory efficiency.

    Args:
        country_code: The two-letter country code (e.g., "DE").
    """
    capa_folder = RESULTS_DIR / "eraa_study" / "capacity_factors"
    technologies = ["Wind_Onshore", "Wind_Offshore", "Solar"]
    years = ["2026", "2028", "2030", "2035"]
    cols = [f"WS{i}" for i in range(1, 36)]

    for year in years:
        lazy_frames_for_year = []
        for tech in technologies:
            logging.info(f"Loading capacity factors for {tech} in {country_code} for year {year}...")
            year_files = list(capa_folder.glob(f"{country_code}*{tech}*{year}.csv"))

            if not year_files:
                logging.warning(f"No files found for {tech} in {country_code} for year {year}. Skipping.")
                continue

            # Create a lazy frame for each file to correctly generate the 'hour' index per file.
            # This is crucial for the subsequent group_by operation.
            lazy_frames_per_tech = [
                pl.scan_csv(f, skip_rows=10).with_row_index(name="hour")
                for f in year_files
            ]

            # Concatenate the lazy frames for the current technology.
            lf_tech = pl.concat(lazy_frames_per_tech, how="vertical")
            lf_tech = lf_tech.unpivot(index="hour", on=cols, variable_name="WS", value_name="capacity_factor")
            lf_tech = lf_tech.with_columns(plant_type=pl.lit(tech).cast(pl.Categorical), WS=pl.col("WS").cast(pl.Categorical))

            if len(year_files) > 1:
                logging.info(f"Merging capacity factors for {tech} in {country_code} for year {year}...")
                lf_tech = lf_tech.group_by(['hour', 'plant_type', 'WS']).agg(pl.col("capacity_factor").mean())

            # Ensure a consistent column order to prevent schema errors during concatenation.
            final_cols = ['hour', 'plant_type', 'WS', 'capacity_factor']
            if lf_tech.columns != final_cols:
                lf_tech = lf_tech.select(final_cols)

            lazy_frames_for_year.append(lf_tech.sort(["hour", "plant_type", "WS"]))

        if lazy_frames_for_year:
            output_path = RESULTS_DIR / f"capacity_factors/capacity_factors_{country_code}_{year}.parquet"
            logging.info(f"Processing and saving data for year {year} to {output_path}...")
            pl.concat(lazy_frames_for_year, how='vertical').sink_parquet(output_path)
            logging.info(f"Successfully saved data for year {year}.")

if __name__ == "__main__":
    conf = yaml.safe_load((PACKAGE_DIR / "config" / "config.yaml").read_text())

    # load_and_merge_eraa_data("SE")
    for country in conf["countries"]:
        load_and_merge_eraa_data(country)