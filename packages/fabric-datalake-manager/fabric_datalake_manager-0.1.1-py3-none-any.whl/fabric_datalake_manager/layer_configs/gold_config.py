import os
import json

from typing import List
from dacite import from_dict

from fabric_datalake_manager.interfaces.config_interface import ILakeConfig

from fabric_datalake_manager.dataclass.gold_dataclass import GoldScheduleEntities

# ==========================
# Gold Config (Root Loader)
# ==========================


class GoldConfig(ILakeConfig):

    @classmethod
    def __init__(self, json_path: str):
        self.path = json_path
        self.schedules: List[GoldScheduleEntities] = []

        if not self.path:
            print("No lake path provided to GoldConfig; schedules not loaded.")
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
            raw_schedules = data.get("schedules", [])

            self.schedules = [
                from_dict(GoldScheduleEntities, s)
                for s in raw_schedules
            ]

        except Exception as e:
            print(f"Error parsing schedules from gold config: {e}")
            self.schedules = []
