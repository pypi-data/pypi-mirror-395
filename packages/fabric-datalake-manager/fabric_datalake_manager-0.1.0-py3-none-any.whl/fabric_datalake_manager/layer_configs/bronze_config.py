import json
import os

from dacite import from_dict
from typing import List, Optional

from fabric_datalake_manager.interfaces.config_interface import ILakeConfig

from fabric_datalake_manager.dataclass.bronze_dataclass import BronzeCountry


# ==========================
# Bronze Config Class
# ==========================

class BronzeConfig(ILakeConfig):

    def __init__(self, json_path: str):
        self.path = json_path
        self.countries: Optional[List[BronzeCountry]] = None

        if not self.path:
            # No path provided, nothing to load
            print("No lake path provided to DataPoint; countries not loaded.")
            return

        full_path = os.path.join(self.path, "configs", "config.json")

        # ---------------------------------------
        # Load JSON
        # ---------------------------------------
        try:
            json_text = mssparkutils.fs.head(full_path)
            data = json.loads(json_text)
        except Exception as e:
            print(f"Error loading config: {e}")
            return

        # ---------------------------------------
        # Convert JSON → dataclass list
        # ---------------------------------------
        try:
            raw_countries = data.get("countries", [])
            self.countries = [
                from_dict(data_class=BronzeCountry, data=c)
                for c in raw_countries
            ]
        except Exception as e:
            print(f"Error parsing countries from config: {e}")
            self.countries = []
