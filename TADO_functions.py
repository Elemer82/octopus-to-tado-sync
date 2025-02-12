from PyTado.interface import Tado
from datetime import datetime


def send_reading_to_tado(username, password, reading):
    """
    Sends the total consumption reading to Tado using its Energy IQ feature.
    """
    tado = Tado(username, password)
    result = tado.set_eiq_meter_readings(reading=int(reading))
    print(result)


def send_reading_to_tado_with_date(username: str, password: str, reading: int = 0,
                                   date: datetime = datetime.now().strftime('%Y-%m-%d')):
    """
    Sends the consumption reading to Tado using its Energy IQ feature.
    """
    tado = Tado(username, password)
    print(f"Submitting reading for {date.strftime('%Y-%m-%d')} with the value of {reading}")
    result = tado.set_eiq_meter_readings(reading=int(reading), date=date.strftime('%Y-%m-%d'))
    print(result)
