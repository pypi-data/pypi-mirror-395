from __future__ import annotations

import os
import json
import re
import fsspec

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
                from_dict(data_class=SilverCountry, data=c)
                for c in raw_countries
            ]
        except Exception as e:
            print(f"Error parsing countries from config: {e}")
            self.countries = []
