import os 
from typing import Dict, Tuple

class AirGenUtils:
    @staticmethod
    def get_asset_spec(env_name: str) -> Tuple[str, str]:
        """
        Return (blob_url, relative_dest_path).
        The server will prepend GRID_DATA_DIR when it builds the absolute path.
        """
        blob = f"https://gridenterpriseresources.blob.core.windows.net/airgennew/{env_name}.tar"
        rel  = "airgenbins"
        return blob, rel
    
    @staticmethod
    def post_init_url(client_datastore: str):
        asset_dir = os.path.join(os.environ.get("GRID_DATA_DIR"), "airgenbins")
        
        if not os.path.exists(asset_dir):
            os.makedirs(asset_dir)

        urls = []

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
                "sim_type": "airgen",
                "scene_name": "blocks",
                "kwargs": {
                    "geo": False,
                },
                "settings": {
                "Vehicles": {
                    "Drone": {
                        "VehicleType": "Chaos",
                        "VehicleModel": "MCR"
                    }
                    },
                    "CameraDirector": {
                    "FollowDistance": 1,
                        "InterpSpeed": 1,
                        "X": -2, "Y": 0, "Z": -0.5,
                        "Pitch": -8
                    },
                    "OriginGeopoint": {
                    "Latitude": 47.62094998919241,
                    "Longitude": -122.35554810901883,
                    "Altitude": 100
                    }
                }
                },
                "grid": {
                "entities": {
                    "robot": [{"name": "airgen-drone", "kwargs": {}}],
                    "model": []
                }
            }
        }

        return sample_session_config
