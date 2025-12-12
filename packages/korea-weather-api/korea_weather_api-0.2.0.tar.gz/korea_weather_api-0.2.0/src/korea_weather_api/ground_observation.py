from datetime import datetime
from typing import Any, Literal, Optional
import requests

from .base import BaseApi


class GroundObservation(BaseApi):
    @staticmethod
    def _preprocess_data(data):
        for key, value in data.items():
            if key.endswith("_dt"):
                if "-" in value:
                    data[key] = None
                else:
                    value = value.rjust(4, "0")

                    data[key] = datetime(
                        data["dt"].year,
                        data["dt"].month,
                        data["dt"].day,
                        int(value[:2]) % 24,
                        int(value[2:]),
                    )

            elif isinstance(value, int):
                if value == -9:
                    data[key] = None

            elif isinstance(value, float):
                if value == -9.0:
                    data[key] = None

            elif isinstance(value, str):
                if value == "-9" or value == "-":
                    data[key] = None
                else:
                    data[key] = value.strip()

        return data

    @staticmethod
    def get_synoptic_data(
        frequency: Literal["hour", "day"],
        start_dt: datetime,
        end_dt: datetime,
        station_id: str,
        auth_key: str,
    ) -> list[dict[str, Any]]:
        """
        Get ground observation synoptic data.

        Parameters
        ----------
        frequency : Literal["hour", "day"]
            Data frequency.
        start_dt : datetime
            Start datetime to query.
        end_dt : datetime
            End datetime to query.
            If frequency is "day", `end_dt` can be set to `start_dt` + 31 days.
        station_id : str
            Station ID.
        auth_key : str
            Authentication key.

        Returns
        -------
        list[dict[str, Any]]
            Synoptic data.
        """

        if start_dt > end_dt:
            raise ValueError("start_dt must be earlier than or equal to end_dt.")

        if frequency == "hour" and (end_dt - start_dt).days > 31:
            raise ValueError("Up to 31 days can be queried for hourly data.")

        params = {
            "stn": station_id,
            "disp": "1",
            "authKey": auth_key,
        }
        if frequency == "hour":
            separator = None
            if start_dt == end_dt:
                url = f"{GroundObservation.BASE_URL}/kma_sfctm2.php"
                params["tm"] = start_dt.strftime("%Y%m%d%H%M")
            else:
                url = f"{GroundObservation.BASE_URL}/kma_sfctm3.php"
                params["tm1"] = start_dt.strftime("%Y%m%d%H%M")
                params["tm2"] = end_dt.strftime("%Y%m%d%H%M")
        elif frequency == "day":
            separator = ","
            url = f"{GroundObservation.BASE_URL}/kma_sfcdd.php"
            params["tm"] = start_dt.strftime("%Y%m%d")

        response = requests.get(
            url,
            params=params,
        )

        if response.status_code != 200:
            raise ValueError(response.json()["result"]["message"])

        data = GroundObservation._preprocess_data(response)
        if not data:
            raise ValueError("There is no data for the datetime or station.")

        result = []

        while data:
            elem = data.pop().split(separator)
            if frequency == "hour":
                record = {
                    "dt": datetime.strptime(elem[0], "%Y%m%d%H%M"),
                    "station_id": elem[1],
                    "wind_direction": elem[2],
                    "wind_speed": float(elem[3]),
                    "gust_wind_direction": elem[4],
                    "gust_wind_speed": float(elem[5]),
                    "gust_wind_dt": elem[6],
                    "atmospheric_pressure": float(elem[7]),
                    "atmospheric_pressure_sea_level": float(elem[8]),
                    "atmospheric_pressure_change": float(elem[10]),
                    "temperature": float(elem[11]),
                    "temperature_dew_point": float(elem[12]),
                    "humidity": float(elem[13]),
                    "water_vapor_pressure": float(elem[14]),
                    "rainfall": float(elem[15]),
                    "rainfall_day": float(elem[16]),
                    "snow_depth_3h": float(elem[19]),
                    "snow_depth_day": float(elem[20]),
                    "snow_depth_total": float(elem[21]),
                    "cloud_amount_total": int(elem[25]),
                    "cloud_amount_middle": int(elem[26]),
                    "cloud_height_minimum": int(elem[27]),
                    "cloud_type": elem[28],
                    "visibility": float(elem[32]),
                    "sunshine": float(elem[33]),
                    "insolation": float(elem[34]),
                    "temperature_earth_5cm": float(elem[36]),
                    "temperature_earth_10cm": float(elem[37]),
                    "temperature_earth_20cm": float(elem[38]),
                    "temperature_earth_30cm": float(elem[39]),
                    "wave_height": float(elem[41]),
                }

            elif frequency == "day":
                record = {
                    "dt": datetime.strptime(elem[0], "%Y%m%d"),
                    "station_id": elem[1],
                    "wind_speed_average": float(elem[2]),
                    "wind_run": int(elem[3]),
                    "wind_direction_max": elem[4],
                    "wind_speed_max": float(elem[5]),
                    "wind_speed_max_dt": elem[6],
                    "wind_direction_instantaneous": elem[7],
                    "wind_speed_instantaneous": float(elem[8]),
                    "wind_speed_instantaneous_dt": elem[9],
                    "temperature_average": float(elem[10]),
                    "temperature_max": float(elem[11]),
                    "temperature_max_dt": elem[12],
                    "temperature_min": float(elem[13]),
                    "temperature_min_dt": elem[14],
                    "temperature_dew_point": float(elem[15]),
                    "temperature_ground": float(elem[16]),
                    "temperature_grass": float(elem[17]),
                    "humidity_average": float(elem[18]),
                    "humidity_min": float(elem[19]),
                    "humidity_min_dt": elem[20],
                    "water_vapor_pressure": float(elem[21]),
                    "evaporation_small": float(elem[22]),
                    "evaporation_large": float(elem[23]),
                    "fog_duration": float(elem[24]),
                    "atmospheric_pressure": float(elem[25]),
                    "atmospheric_pressure_sea_level": float(elem[26]),
                    "atmospheric_pressure_sea_level_max": float(elem[27]),
                    "atmospheric_pressure_sea_level_max_dt": elem[28],
                    "atmospheric_pressure_sea_level_min": float(elem[29]),
                    "atmospheric_pressure_sea_level_min_dt": elem[30],
                    "cloud_amount": float(elem[31]),
                    "sunshine": float(elem[32]),
                    "sunshine_duration": float(elem[33]),
                    "sunshine_campbell": float(elem[34]),
                    "solar_insolation": float(elem[35]),
                    "solar_insolation_60m_max": float(elem[36]),
                    "solar_insolation_60m_max_dt": elem[37],
                    "rainfall": float(elem[38]),
                    "rainfall_99": float(elem[39]),
                    "rainfall_duration": float(elem[40]),
                    "rainfall_60m_max": float(elem[41]),
                    "rainfall_60m_max_dt": elem[42],
                    "rainfall_10m_max": float(elem[43]),
                    "rainfall_10m_max_dt": elem[44],
                    "rainfall_intensity_max": float(elem[45]),
                    "rainfall_intensity_max_dt": elem[46],
                    "snow_depth_new": float(elem[47]),
                    "snow_depth_new_dt": elem[48],
                    "snow_depth_max": float(elem[49]),
                    "snow_depth_max_dt": elem[50],
                    "temperature_earth_5cm": float(elem[51]),
                    "temperature_earth_10cm": float(elem[52]),
                    "temperature_earth_15cm": float(elem[53]),
                    "temperature_earth_30cm": float(elem[54]),
                    "temperature_earth_50cm": float(elem[55]),
                }

            record = GroundObservation._preprocess_data(record)
            result.append(record)

        return result

    @staticmethod
    def get_station_data(
        auth_key: str,
        dt: Optional[datetime] = None,
    ) -> list[dict[str, Any]]:
        """
        Get ground observation station data.

        Parameters
        ----------
        auth_key : str
            Authentication key.
        dt : Optional[datetime]
            Datetime to query.

        Returns
        -------
        list[dict[str, Any]]
            Station data.
        """

        response = requests.get(
            "https://apihub.kma.go.kr/api/typ01/url/stn_inf.php",
            params={
                "inf": "SFC",
                "tm": dt.strftime("%Y%m%d%H%M%S") if dt is not None else None,
                "authKey": auth_key,
            },
        )

        if response.status_code != 200:
            raise ValueError(response.json()["result"]["message"])
        data = response.text.splitlines()

        data = [elem.split() for elem in data[3:-2]]

        data = [
            {
                "station_id": elem[0],
                "longitude": elem[1],
                "latitude": elem[2],
                "altitude": elem[4],
                "altitude_barometer": elem[5],
                "altitude_thermometer": elem[6],
                "altitude_anemometer": elem[7],
                "altitude_rain_gauge": elem[8],
                "station_name": elem[10],
                "station_name_eng": elem[11],
                "management_facility_id": elem[12],
                "administrative_district_id": elem[13],
            }
            for elem in data
        ]

        return data
