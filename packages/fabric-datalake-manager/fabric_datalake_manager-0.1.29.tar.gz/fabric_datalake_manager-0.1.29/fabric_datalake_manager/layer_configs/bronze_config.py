from __future__ import annotations

import json
import os
import re
import fsspec

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
            raw_countries = data.get("countries", [])
            self.countries = [
                from_dict(data_class=BronzeCountry, data=c)
                for c in raw_countries
            ]
        except Exception as e:
            print(f"Error reading from JSON '{full_path}': {e}")
            self.countries = []
