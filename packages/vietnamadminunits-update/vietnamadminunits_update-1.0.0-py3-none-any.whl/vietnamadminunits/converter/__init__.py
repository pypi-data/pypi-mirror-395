from .converter_2025 import convert_address_2025, convert_address_to_old_2025
from enum import Enum
from typing import Union


class ConvertMode(Enum):
    CONVERT_2025 = "CONVERT_2025"  # From LEGACY → MERGER_2025
    CONVERT_TO_OLD_2025 = "CONVERT_TO_OLD_2025"  # From MERGER_2025 → LEGACY

    @classmethod
    def available(cls, value=False):
        attrs = list(cls)
        if value:
            attrs = [a.value for a in attrs]
        return attrs


def convert_address(address: str, mode: Union[str, ConvertMode]=ConvertMode.CONVERT_2025):
    '''
    Converts an address from the 63-province format to a standardized 34-province `AdminUnit`.

    :param address: Best format *"(street), ward, district, province"*. Case is ignored, accents are usually ignored except in rare cases.
    :param mode: Currently, only `'CONVERT_2025'` is supported.
    :return: AdminUnit object.
    '''

    if mode in [ConvertMode.CONVERT_2025, ConvertMode.CONVERT_2025.value]:
        return convert_address_2025(address)
    else:
        raise Exception(f"Invalid mode. Available modes are {ConvertMode.available(value=True)}.")


def convert_address_to_old(address: str, mode: Union[str, ConvertMode]=ConvertMode.CONVERT_TO_OLD_2025):
    '''
    Converts an address from the 34-province format to the old 63-province format `AdminUnit`.

    :param address: Best format *"(street), ward, province"*. Case is ignored, accents are usually ignored except in rare cases.
    :param mode: Currently, only `'CONVERT_TO_OLD_2025'` is supported.
    :return: AdminUnit object.
    '''

    if mode in [ConvertMode.CONVERT_TO_OLD_2025, ConvertMode.CONVERT_TO_OLD_2025.value]:
        return convert_address_to_old_2025(address)
    else:
        raise Exception(f"Invalid mode. Available modes are {ConvertMode.available(value=True)}.")