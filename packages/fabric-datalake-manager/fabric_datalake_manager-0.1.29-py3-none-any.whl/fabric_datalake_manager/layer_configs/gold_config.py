from __future__ import annotations

import os
import json
import re
import fsspec

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
        match = re.match(r"abfss://([^@]+)@([^/]+)/(.*)", full_path)

        if not match:
            raise ValueError(f"Invalid ABFSS path: {full_path}")

        container, account_host, file_path = match.groups()
        account_name = account_host.split(".")[0]

        try:
            fs = fsspec.filesystem(
                "abfss",
                account_name=account_name,
                account_host=account_host,
            )

            full_path = f"{container}/{file_path}"
            with fs.open(full_path, "r") as f:
                data = json.load(f)

            # ---------------------------------------
            # Convert JSON → dataclass list
            # ---------------------------------------
            raw_schedules = data.get("schedules", [])

            self.schedules = [
                from_dict(GoldScheduleEntities, s)
                for s in raw_schedules
            ]

        except Exception as e:
            print(f"Error parsing schedules from gold config: {e}")
            self.schedules = []
