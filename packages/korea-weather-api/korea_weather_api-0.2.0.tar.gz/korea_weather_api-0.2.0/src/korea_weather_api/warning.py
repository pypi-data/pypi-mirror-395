from datetime import datetime, timedelta
from typing import Optional
import requests

from .base import BaseApi


class Warning(BaseApi):
    @staticmethod
    def get_warning_data(
        start_dt: datetime,
        end_dt: datetime,
        auth_key: str,
        region: Optional[str] = None,
    ):
        if start_dt > end_dt:
            raise ValueError("start_dt must be earlier than or equal to end_dt.")

        if end_dt - start_dt > timedelta(days=365):
            raise ValueError("The maximum period is 1 year.")

        def _convert_warning(value: str) -> str:
            WARNING_TYPES = {
                "W": "strong_wind",
                "R": "heavy_rain",
                "C": "cold_wave",
                "D": "dry",
                "O": "tsunami",
                "N": "earthquake_tsunami",
                "V": "high_seas",
                "T": "typhoon",
                "S": "heavy_snow",
                "Y": "yellow_dust",
                "H": "heat_wave",
                "F": "fog",
            }
            return WARNING_TYPES[value]

        def _convert_command(value: str) -> str:
            COMMAND_TYPES = {
                "1": "forecasted",
                "2": "upgraded",
                "3": "lifted_forecasted",
                "4": "lifted_upgraded",
                "5": "extended",
                "6": "downgraded",
                "7": "lifted_downgraded",
            }
            return COMMAND_TYPES[value]

        params = {
            "disp": "0",
            "help": "0",
            "authKey": auth_key,
        }
        if region is not None:
            params["reg"] = region
        if start_dt is not None:
            params["tmfc1"] = start_dt.strftime("%Y%m%d%H%M")
        if end_dt is not None:
            params["tmfc2"] = end_dt.strftime("%Y%m%d%H%M")

        response = requests.get(
            f"{Warning.BASE_URL}/wrn_met_data.php",
            params=params,
        )

        if response.status_code != 200:
            raise ValueError(response.json()["result"]["message"])

        data = Warning._preprocess_data(response)

        result = []

        while data:
            elem = data.pop().split(",")
            elem = [i.strip() for i in elem]

            record = {
                "forecast_dt": datetime.strptime(elem[0], "%Y%m%d%H%M"),
                "effect_dt": datetime.strptime(elem[1], "%Y%m%d%H%M"),
                "input_dt": datetime.strptime(elem[2], "%Y%m%d%H%M"),
                "station_id": elem[3],
                "region_id": elem[4],
                "warning": _convert_warning(elem[5]),
                "level": int(elem[6]),
                "command": _convert_command(elem[7]),
            }

            result.append(record)

        return result
