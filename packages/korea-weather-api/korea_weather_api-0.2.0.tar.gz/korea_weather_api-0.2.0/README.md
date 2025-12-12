# korea-weather-api

[![PyPI - Version](https://img.shields.io/pypi/v/korea-weather-api.svg)](https://pypi.org/project/korea-weather-api)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/korea-weather-api.svg)](https://pypi.org/project/korea-weather-api)

-----

## Table of Contents

- [Installation](#installation)
- [API Reference](#api-reference)
- [License](#license)

## Installation

```console
pip install korea-**weather**-api
```

## API Reference

### `GroundObservation`

#### `GroundObservation.get_synoptic_data`

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

#### `GroundObservation.get_station_data`

Get ground observation station data.

Parameters
----------
auth_key : str
    Authentication key.
dt : Optional[datetime.datetime]
    Datetime to query.

Returns
-------
list[dict[str, Any]]
    Station data.

## License

`korea-weather-api` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
