import os
import subprocess
from grid.utils.azcopy_downloader import AzCopyDownloader
 
import shutil

from grid.utils.airgen_utils import AirGenUtils
from grid.utils.isaac_utils import IsaacUtils

from typing import Optional
import json
import logging 

logger = logging.getLogger("grid.commander")        # configured in server.py

sim_utils_mapping = {
    "airgen": AirGenUtils,
    "isaac": IsaacUtils,
}

class GRIDAssetDownloader:
    @staticmethod
    def download_sample_notebooks():
        samples_dir = os.path.join(os.environ.get("GRID_DATA_DIR"), "samples")
        # Check if the directory already exists
        if not os.path.exists(samples_dir):
            # Create the directory
            os.makedirs(samples_dir)
            
            # Clone the repository into the samples directory
            repo_url = "https://github.com/genrobo/grid-playground"
            subprocess.run(["git", "clone", "--depth", "1", repo_url, samples_dir], check=True)
            shutil.rmtree(os.path.join(samples_dir, ".git"))
        else:
            logger.info(f"Samples currently at {samples_dir}")

        # Write .devcontainer.json to GRID_DATA_DIR
        devcontainer_content = {
            "name": "GRID (attach)",
            "customizations": {
                "vscode": {
                    "extensions": [
                        "ms-python.python",
                        "ms-toolsai.jupyter",
                        "ms-vscode.cpptools",
                        "ms-azuretools.vscode-docker"
                    ],
                    "settings": {
                        "python.defaultInterpreterPath": "/opt/conda/bin/python"
                    }
                }
            }
        }

        devcontainer_path = os.path.join(os.environ.get("GRID_DATA_DIR"), ".devcontainer/devcontainer.json")
        logger.info(f"Writing devcontainer config to {devcontainer_path}")
        os.makedirs(os.path.dirname(devcontainer_path), exist_ok=True)        
        with open(devcontainer_path, 'w') as f:
            json.dump(devcontainer_content, f, indent=2)

    @staticmethod
    def download_model_weights():
        downloader = AzCopyDownloader()
        weights_dir = os.path.join(os.environ.get("GRID_DATA_DIR"), "models")

        url = "https://gridenterpriseresources.blob.core.windows.net/aimodelweights/weights"
        # Download the model weights via AzCopyDownloader (handles SAS and dirs)
        downloader.download_az_file(url, weights_dir)
            
    @staticmethod
    def download_sim_assets(sim_type: str, client_datastore: Optional[str] = None):
        downloader = AzCopyDownloader()

        sim_utils = sim_utils_mapping.get(sim_type)
        post_init_data = sim_utils.post_init_url(client_datastore)

        for data in post_init_data:
            url, dest_path = data
            downloader.download_az_file(url, dest_path)
        

# Example usage
if __name__ == "__main__":
    GRIDAssetDownloader.download_sample_notebooks()