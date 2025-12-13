import os
import json
import datetime
import tempfile
import requests
import xmltodict
from enum import StrEnum
from diskcache import Cache
from datetime import timedelta
from decimal import Decimal, ROUND_HALF_UP

cache_path = os.path.join(tempfile.gettempdir(), "cache_cursvalutarbnr")
cache = Cache(cache_path)


class Currency(StrEnum):
    RON = "RON"
    AED = "AED"
    AUD = "AUD"
    BGN = "BGN"
    BRL = "BRL"
    CAD = "CAD"
    CHF = "CHF"
    CNY = "CNY"
    CZK = "CZK"
    DKK = "DKK"
    EGP = "EGP"
    EUR = "EUR"
    GBP = "GBP"
    HUF = "HUF"
    INR = "INR"
    JPY = "JPY"
    KRW = "KRW"
    MDL = "MDL"
    MXN = "MXN"
    NOK = "NOK"
    NZD = "NZD"
    PLN = "PLN"
    RSD = "RSD"
    RUB = "RUB"
    SEK = "SEK"
    THB = "THB"
    TRY = "TRY"
    UAH = "UAH"
    USD = "USD"
    XAU = "XAU"
    XDR = "XDR"
    ZAR = "ZAR"

    @classmethod
    def values(cls):
        return {e.value for e in cls}


def get_bnr_rates_for_year(year: int):
    """
    Make a request to BNR API to get the XML with rates for the year provided.
    If year is not provided will get the latest rates for current date.

    The return will be a dictionary like:

    {'2024-01-03': {'AED': 1.239,
            'AUD': 3.0693,
            'CAD': 3.4127,
            etc},
        'YYYY-MM-DD': {'CURRENCY': RON_VALUE}
    }

    https://www.bnr.ro/nbrfxrates.xml
    https://www.bnr.ro/nbrfxrates10days.xml
    https://www.bnr.ro/files/xml/years/nbrfxrates{year}.xml
    """
    cache = True
    url = f"https://www.bnr.ro/files/xml/years/nbrfxrates{year}.xml"
    r = requests.get(url)
    bnr_ron_rates = xmltodict.parse(r.content)

    if "Cube" not in bnr_ron_rates["DataSet"]["Body"]:
        cache = False
        r = requests.get("https://www.bnr.ro/nbrfxrates10days.xml")
        bnr_ron_rates = xmltodict.parse(r.content)

    exchange_rates = {}
    for entries in bnr_ron_rates["DataSet"]["Body"]["Cube"]:
        rates = {}
        for entry in entries["Rate"]:
            currency = entry["@currency"]
            value = Decimal(entry["#text"])
            multiplier = Decimal(entry.get("@multiplier", "1"))
            rates[currency] = float((value * multiplier).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP))

        exchange_rates[entries["@date"]] = rates
    
    return exchange_rates, cache


def get_bnr_rates(date: datetime.datetime):
    today = datetime.datetime.now()
    year_requested = date.year
    year_before = date.year - 1

    cached_keys = list(cache.iterkeys())

    for cached_key in cached_keys:
        if cached_key == str(year_requested) and year_requested < today.year:
            return json.loads(cache.get(str(year_requested)))

        if len(cached_key) == len("2024-01-01"):
            cached_exchange_rates = json.loads(cache.get(cached_key))
            latest_cached_date = max(
                [
                    datetime.datetime.strptime(d, "%Y-%m-%d").date()
                    for d in cached_exchange_rates.keys()
                ]
            )
            if date <= latest_cached_date:
                return cached_exchange_rates

    exchange_rates_year_requested, cache_year_requested = get_bnr_rates_for_year(year_requested)
    exchange_rates_year_before, cache_year_before = get_bnr_rates_for_year(year_before)
    exchange_rates_year_before.update(exchange_rates_year_requested)

    if cache_year_requested is not False and cache_year_before is not False:
        if year_requested < today.year:
            with Cache(cache.directory) as reference:
                reference.set(str(year_requested), json.dumps(exchange_rates_year_before))

        if year_requested == today.year:
            with Cache(cache.directory) as reference:
                reference.set(
                    today.date().isoformat(), json.dumps(exchange_rates_year_before)
                )

    return exchange_rates_year_before


def format_date(date: str = None):
    """
    Convert string date in '2024-07-31' (YYYY-MM-DD) format.
    If date is in the future, the latest date will be returned.
    """

    previous_date = datetime.datetime.now().date() - timedelta(days=1)

    if date is None:
        date_obj = previous_date
    elif isinstance(date, datetime.date):
        date_obj = date
    elif isinstance(date, str):
        date_obj = datetime.datetime.strptime(date, "%Y-%m-%d").date()

    if date_obj > previous_date:
        date_obj = previous_date

    return date_obj


def ron_exchange_rate(
    amount: float, currency: Currency, date: str | datetime.date = None
):
    """
    Returns the amount in RON for given currency

    - amount: is the number in given currency to be converted to ron
    - currency: is one of Currency values (can be a string like: "EUR", "USD")
    - date: can be like: "2024-08-06" or datetime.date(2024, 1, 1) or datetime.datetime.now() or datetime.datetime.now().date()

    Usage:

    ```py
    in_ron = ron_exchange_rate(
        amount=1,
        currency="EUR",
        date="2024-08-06"
    )
    # in_ron will be 4.98
    ```
    """

    if currency not in Currency.values():
        raise ValueError(f"Given currency {currency} is not supported.")

    date_obj = format_date(date)

    exchange_rates_raw = get_bnr_rates(date_obj)
    dates_rawer = [
        datetime.datetime.fromisoformat(diso).date()
        for diso in exchange_rates_raw.keys()
    ]

    if date_obj == datetime.date(date_obj.year, 1, 1) or date_obj == datetime.date(
        date_obj.year, 1, 2
    ):
        prev_year = min(dates_rawer).year
        prev_year_dates = [d for d in dates_rawer if d.year == prev_year]
        closest_date = min(prev_year_dates, key=lambda date: abs(date - date_obj))
    else:
        closest_date = min(dates_rawer, key=lambda date: abs(date - date_obj))

    rate = exchange_rates_raw[closest_date.isoformat()][currency]

    result = (Decimal(str(amount)) * Decimal(str(rate))).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)
    return float(result)
