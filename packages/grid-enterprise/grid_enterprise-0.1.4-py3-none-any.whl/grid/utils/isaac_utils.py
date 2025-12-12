import os 
from typing import Dict, Tuple

class IsaacUtils:
    @staticmethod
    def get_asset_url(env_name: str) -> Tuple[str, str]:
        """
        Downloads the specified environment assets using AzCopyDownloader.

        :param env_name: The name of the environment to download.
        :return: True if download is successful, False otherwise.
        """
        container_url = f"https://gridenterpriseresources.blob.core.windows.net/isaac/{env_name}"  # Replace with actual URL
        destination_path = os.path.join(os.environ.get("GRID_DATA_DIR"), "isaac")

        return container_url, destination_path
    
    @staticmethod
    def post_init_url(client_datastore: str):
        asset_dir = os.path.join(os.environ.get("GRID_DATA_DIR"), "isaac")
        
        if not os.path.exists(asset_dir):
            os.makedirs(asset_dir)
            
        urls = []
        env_name = "common"
        
        urls.append(IsaacUtils.get_asset_url(env_name))

        if client_datastore is not None:
            custom_url = f"https://sfclientdata.blob.core.windows.net/{client_datastore}/*"
            destination_path = os.path.join(os.environ.get("GRID_DATA_DIR"))
            urls.append((custom_url, destination_path))        
        
        return urls
        
    @staticmethod
    def sim_streaming_url(node_ip: str) -> str:
        return f"http://{node_ip}:3080"
    
    @staticmethod
    def create_sample_config() -> Dict:
        sample_session_config = { 
            "sim": {
                "sim_type": "isaac",
                "scene_name": "isaac_tabletop",
                "kwargs": {
                "geo": False,
                },
                "settings": {
                    "robot_name": "isaac_franka_kb",
                },
            },
            "grid": {
                "entities": {
                    "robot": [
                        {
                            "name": "arm:isaac:sim",
                            "kwargs": {}
                        }
                    ],
                    "model": [], 
                },
            }
        }

        return sample_session_config