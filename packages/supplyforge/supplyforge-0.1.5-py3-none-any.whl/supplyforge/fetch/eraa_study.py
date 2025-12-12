# fetch/eraa.py
import logging
import requests
import zipfile
from pathlib import Path
import shutil

# Constants
from supplyforge import RESULTS_DIR
ERAA_URL = "https://eepublicdownloads.blob.core.windows.net/public-cdn-container/clean-documents/sdc-documents/ERAA/ERAA_2024/Dashboard_raw_data.zip"
TARGET_DIR = RESULTS_DIR / "eraa_study"
DOWNLOAD_LOG = TARGET_DIR / "download.txt"

# Set up logging
LOG_FILE = TARGET_DIR / "eraa_fetch.log"
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def fetch_eraa_data():
    """
    Fetches the ERAA 2024 data, unzips it, and stores the contents in RESULTS_DIR/eraa_study,
    without keeping the intermediate folder from the ZIP file.
    A log of the downloaded files will be created in download.txt.
    """
    try:
        # Ensure target directory exists
        TARGET_DIR.mkdir(parents=True, exist_ok=True)

        # Path to the downloaded file
        zip_file_path = TARGET_DIR / "Dashboard_raw_data.zip"

        # Download file
        logger.info(f"Downloading ERAA data from {ERAA_URL}...")
        response = requests.get(ERAA_URL, stream=True)
        response.raise_for_status()  # Ensure any HTTP request errors are raised

        # Save to ZIP file
        with open(zip_file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        logger.info(f"Downloaded ERAA data to {zip_file_path}.")

        # Unzip the contents and flatten the structure
        logger.info("Unzipping ERAA data...")
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            extracted_files = []
            for file in zip_ref.namelist():
                # Extract each file directly into TARGET_DIR
                target_path = TARGET_DIR / Path(file).name
                if not file.endswith("/"):  # Skip directories
                    with open(target_path, "wb") as output_file:
                        shutil.copyfileobj(zip_ref.open(file), output_file)
                    extracted_files.append(target_path.name)

        logger.info(f"Extracted ERAA data to {TARGET_DIR}.")
        logger.info(f"Extracted files: {', '.join(extracted_files)}")

        # Write the flattened file names to download.txt
        with open(DOWNLOAD_LOG, 'w') as download_file:
            download_file.write("\n".join(extracted_files))
        logger.info(f"Created download log at {DOWNLOAD_LOG}.")

        # Remove ZIP file after successful extraction
        zip_file_path.unlink(missing_ok=True)
        logger.info("Temporary ZIP file removed.")

    except Exception as e:
        logger.error(f"Failed to fetch and process ERAA data: {e}")
        raise


# Execute if run as a script
if __name__ == "__main__":
    fetch_eraa_data()
