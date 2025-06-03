import argparse
from datetime import datetime, timedelta
from Octopus_Functions import get_consumption_between_dates
from TADO_functions import tado_login
from logging_functions import create_debug_info_console_logger
from datetime import date


def parse_args():
    """
    Parses command-line arguments for Tado and Octopus API credentials and meter details.
    """
    parser = argparse.ArgumentParser(
            description="Tado and Octopus API Interaction Script"
        )
    try:
        # Tado API arguments
        parser.add_argument("--tado-email", required=True, help="Tado account email")
        parser.add_argument("--tado-password", required=True, help="Tado account password")

        # Octopus API arguments
        parser.add_argument(
            "--mprn",
            required=True,
            help="MPRN (Meter Point Reference Number) for the gas meter",
        )
        parser.add_argument(
            "--gas-serial-number", required=True, help="Gas meter serial number"
        )
        parser.add_argument("--octopus-api-key", required=True, help="Octopus API key")
    except argparse.ArgumentError as e:
        print(f"Error parsing arguments: {e}")
        parser.print_help()
        exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        parser.print_help()
        exit(1)
        parser.print_help()
        exit(1) # This line is unreachable, but kept for clarity
    finally:
        return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    log_obj = create_debug_info_console_logger("sync_octopus_tado")

    # tado = Tado(args.tado_email, args.tado_password)
    tado = tado_login(username=args.tado_email, password=args.tado_password, logger_=log_obj)
    result = tado.get_eiq_meter_readings()

    first_date_reading_submitted_to_tado = datetime(year=9999, month=12, day=31)
    first_reading_submitted_to_tado = 999999999

    last_date_reading_submitted_to_tado = datetime(year=2000, month=1, day=1)
    last_reading_submitted_to_tado = 0
    for reading in result["readings"]:
        this_date = datetime(year=int(reading["date"][:4]),
                             month=int(reading["date"][5:7]),
                             day=int(reading["date"][8:]))
        if this_date > last_date_reading_submitted_to_tado:
            last_date_reading_submitted_to_tado = this_date
            last_reading_submitted_to_tado = reading["reading"]
        # This date needs to be hardcoded for me, as this is the date I was moved from bulb to tado
        # There is a meter reading submitted for this date in tado as well, so they can synchronise
        # if datetime(year=2023, month=2, day=24) <= this_date < first_date_reading_submitted_to_tado:
        # Get the date 2 years ago from today plus 30 days
        two_years_ago = datetime.now() - timedelta(days=2*365 - 30)
        if two_years_ago <= this_date < first_date_reading_submitted_to_tado:
            first_date_reading_submitted_to_tado = this_date
            first_reading_submitted_to_tado = reading["reading"]
    log_obj.info(f"Reading submitted to tado on {first_date_reading_submitted_to_tado} was "
                 f"{first_reading_submitted_to_tado} this was about 2 years ago")
    log_obj.info(f"Last reading submitted to tado on {last_date_reading_submitted_to_tado} was "
                 f"{last_reading_submitted_to_tado}")

    if (datetime.now() - last_date_reading_submitted_to_tado).days > 30:
        # We need to just get the consumption between 2 dates
        to_date = last_date_reading_submitted_to_tado + timedelta(days=30)
        # With the below we make sure that we get exactly 1 month in advance of the previous reading,
        # This also takes in account December to January rollover,
        # TODO Days over 28 are not supported because of February
        to_date = datetime(year=to_date.year, month=to_date.month, day=last_date_reading_submitted_to_tado.day)
    else:
        # We just need to get the consumption from this date onwards
        to_date = datetime.now()
    log_obj.debug(f"Getting consumption between {first_date_reading_submitted_to_tado} and {to_date}")
    # Get consumption from Octopus Energy API
    consumption = get_consumption_between_dates(first_date_reading_submitted_to_tado, to_date,
                                                args.octopus_api_key, args.mprn, args.gas_serial_number, log_obj)
    # Get total consumption from Octopus Energy API
    # consumption = get_meter_reading_total_consumption(args.octopus_api_key, args.mprn, args.gas_serial_number)

    new_reading = int(first_reading_submitted_to_tado + consumption)
    if new_reading < last_reading_submitted_to_tado:
        log_obj.warning(f"Something went wrong new reading {new_reading} is lower than the highest reading already "
                     f"submitted {last_reading_submitted_to_tado}")
        log_obj.error(f"The current reading can't be less than the previously added reading, "
                      f"please check the value or date and try again.")
        log_obj.error(f"Octopus has no data from bulb!!!")
    else:
        log_obj.info(f"Submitting new_date {to_date} with new_reading {new_reading}")
        # send_reading_to_tado_with_date(args.tado_email, args.tado_password, new_reading, to_date)
        tado.set_eiq_meter_readings(reading=int(new_reading), date=to_date.strftime('%Y-%m-%d'))

    # Send the total consumption to Tado
    # send_reading_to_tado(args.tado_email, args.tado_password, consumption)
