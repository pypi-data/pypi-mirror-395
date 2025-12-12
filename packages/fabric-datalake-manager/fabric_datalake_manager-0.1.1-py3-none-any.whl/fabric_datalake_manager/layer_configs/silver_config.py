import os
import json

from typing import List
from dacite import from_dict

from fabric_datalake_manager.interfaces.config_interface import ILakeConfig

from fabric_datalake_manager.dataclass.silver_dataclass import SilverCountry

# ==========================
# Silver Config (Root Loader)
# ==========================


class SilverConfig(ILakeConfig):

    @classmethod
    def __init__(self, json_path: str):
        self.path = json_path
        self.countries: List[SilverCountry] = []

        if not self.path:
            print("No lake path provided to SilverConfig; countries not loaded.")
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
                from_dict(data_class=SilverCountry, data=c)
                for c in raw_countries
            ]
        except Exception as e:
            print(f"Error parsing countries from config: {e}")
            self.countries = []
