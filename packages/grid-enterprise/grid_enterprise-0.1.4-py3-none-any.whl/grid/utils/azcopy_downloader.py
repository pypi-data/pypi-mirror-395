import subprocess
import shlex
import os
import logging
from urllib.parse import urlparse

class AzCopyDownloader:
    def __init__(self):
        # Use GRID_DATA_DIR if set, otherwise default to ~/.grid
        data_dir = os.environ.get("GRID_DATA_DIR") or os.path.expanduser("~/.grid")
        self.azcopy_path = os.path.join(data_dir, "utils", "azcopy")
        self.azcopy_url = "https://aka.ms/downloadazcopy-v10-linux"  # Example URL for AzCopy download
        
        self.logger = logging.getLogger("grid.commander")

    def ensure_azcopy_exists(self):
        """
        Ensures that AzCopy is downloaded and available at the specified path.
        """
        azcopy_full_path = os.path.expanduser(self.azcopy_path)
        if not os.path.exists(azcopy_full_path):
            self.logger.info("AzCopy not found. Downloading...")
            # Make the folder if it does not exist
            os.makedirs(os.path.dirname(azcopy_full_path), exist_ok=True)
            try:
                # Download AzCopy
                subprocess.run(shlex.split("wget -q https://aka.ms/downloadazcopy-v10-linux"), check=True)
                # Expand Archive
                subprocess.run(shlex.split(f"tar --strip-components=1 -xvf downloadazcopy-v10-linux -C {os.path.dirname(azcopy_full_path)}"), check=True)
                # Change permissions of AzCopy
                subprocess.run(shlex.split(f"chmod 777 {azcopy_full_path}"), check=True)
                self.logger.info("AzCopy downloaded and ready to use.")
                os.remove("downloadazcopy-v10-linux")

            except subprocess.CalledProcessError as e:
                self.logger.info(f"Failed to download AzCopy: {e}")
            except Exception as e:
                self.logger.info(f"Failed to download AzCopy: {e}")

    def download_az_file(self, container_url: str, destination_path: str, force_redownload: bool = False) -> tuple[bool, str]:
        """
        Download a file from an Azure container using AzCopy.

        :param container_url: The URL of the Azure blob (without SAS).
        :param destination_path: The local folder where the file should be downloaded.
        :param force_redownload: If True, force download and overwrite existing content.
        :return: True if download is successful or skipped, False otherwise.
        """
        dest_dir = os.path.expanduser(destination_path)
        os.makedirs(dest_dir, exist_ok=True)

        # Extract filename from URL
        filename = os.path.basename(urlparse(container_url).path)
        dest_file = os.path.join(dest_dir, filename)

        # Skip if file already exists and not forcing redownload
        if os.path.exists(dest_file) and not force_redownload:
            self.logger.info(f"File already exists at {dest_file}. Skipping download.")
            return True, "exists"

        # Ensure destination directory exists
        try:
            os.makedirs(dest_dir, exist_ok=True)
        except Exception:
            pass
        # Acquire SAS token for the container URL
        from grid.utils.auth_utils import get_sas_token

        sas_token = get_sas_token(container_url)
        if not sas_token:
            self.logger.error(f"Failed to acquire SAS token for {container_url}")
            return False
        # Ensure AzCopy binary is available
        self.ensure_azcopy_exists()
        azcopy_exe = os.path.expanduser(self.azcopy_path)
        src = f"{container_url}?{sas_token}"
        args = [azcopy_exe, "copy", src, dest_dir, "--recursive", "--overwrite=ifSourceNewer"]
        try:
            result = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode == 0:
                return True, result.stdout
            
            return False, result.stdout
        except Exception as e:
            self.logger.error(f"An error occurred during AzCopy download: {e}")
            return False
