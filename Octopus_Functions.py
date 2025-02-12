import logging
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime


def get_meter_reading_total_consumption(api_key, mprn, gas_serial_number):
    """
    Retrieves total gas consumption from the Octopus Energy API for the given gas meter point and serial number.
    """
    url = f"https://api.octopus.energy/v1/gas-meter-points/{mprn}/meters/{gas_serial_number}/consumption/?group_by=quarter"
    total_consumption = 0.0

    while url:
        response = requests.get(
            url, auth=HTTPBasicAuth(api_key, "")
        )

        if response.status_code == 200:
            meter_readings = response.json()
            total_consumption += sum(
                interval["consumption"] for interval in meter_readings["results"]
            )
            url = meter_readings.get("next", "")
        else:
            print(
                f"Failed to retrieve data. Status code: {response.status_code}, Message: {response.text}"
            )
            break

    print(f"Total consumption is {total_consumption}")
    return total_consumption


def get_consumption_between_dates(period_from: datetime, period_to: datetime,
                                  api_key: str, mprn: str, gas_serial_number: str, log: logging) -> int:
    """
    Retrieves total gas consumption from the Octopus Energy API for the given gas meter point and serial number.
    """
    url = (f"https://api.octopus.energy/v1/gas-meter-points/{mprn}/meters/{gas_serial_number}/consumption/?"
           f"group_by=quarter&period_from={period_from}&period_to={period_to}")
    total_consumption = 0.0

    while url:
        response = requests.get(
            url, auth=HTTPBasicAuth(api_key, "")
        )

        if response.status_code == 200:
            meter_readings = response.json()
            for interval in meter_readings["results"]:
                # this_consumption = interval["consumption"]
                log.debug(f"Consumption between {interval['interval_start']} -> {interval['interval_end']}")
                log.debug(f"Adding {total_consumption} + {interval['consumption']}")
                total_consumption += interval["consumption"]

            url = meter_readings.get("next", "")
        else:
            log.error(f"Failed to retrieve data. Status code: {response.status_code}, Message: {response.text}")
            break

    log.info(f"Consumption between {period_from} and {period_to} is {total_consumption}")
    return total_consumption


def get_consumption_from_date(period_from: datetime, api_key: str, mprn: str, gas_serial_number: str, log: logging):
    """
    Retrieves total gas consumption from the Octopus Energy API for the given gas meter point and serial number.
    """
    url = (f"https://api.octopus.energy/v1/gas-meter-points/{mprn}/meters/{gas_serial_number}/consumption/?"
           f"group_by=quarter&period_from={period_from}")
    total_consumption = 0.0

    while url:
        response = requests.get(
            url, auth=HTTPBasicAuth(api_key, "")
        )

        if response.status_code == 200:
            meter_readings = response.json()
            total_consumption += sum(
                interval["consumption"] for interval in meter_readings["results"]
            )
            url = meter_readings.get("next", "")
        else:
            log.error(f"Failed to retrieve data. Status code: {response.status_code}, Message: {response.text}")
            break

    log.info(f"Consumption since {period_from} is {total_consumption}")
    return total_consumption