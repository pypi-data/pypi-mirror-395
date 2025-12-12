from ..parser import parse_address, ParseMode
from ..converter import convert_address, ConvertMode
import warnings
from typing import Union
from tqdm import tqdm

def standardize_admin_unit_columns(df, province: str, district: str=None, ward: str=None, parse_mode: Union[str, ParseMode]=ParseMode.latest(), convert_mode: Union[str, ConvertMode]=None, inplace=False, prefix: str='standardized_', suffix :str='', short_name: bool=True, show_progress: bool=True):
    '''
    Standardizes administrative unit columns *(province, district, ward)* in a DataFrame.

    :param df: `pandas.DataFrame` object.
    :param province: Province column name.
    :param district: District column name.
    :param ward: Ward column name.
    :param parse_mode: `'FROM_2025'` (34-province) or `'LEGACY'` (63-province). Default `ParseMode.latest()`.
    :param convert_mode: Currently, only `'CONVERT_2025'` is supported. Using this will ignore `parse_mode`. Default `None`.
    :param inplace: Replace the original columns with standardized values; otherwise add new columns. Default `False`.
    :param prefix: Added to new column names if `inplace=False`.
    :param suffix: Added to new column names if `inplace=False`.
    :param short_name: Use short or full names for administrative units. Default `True`.
    :param show_progress: Display a progress bar during processing. Default `True`.

    :return: `pandas.DataFrame` object.
    '''

    # INITIATIVE VARS
    admin_unit_columns = [l for l in [ward, district, province] if l]  # Remove None

    # RAISE
    if not province:
        raise ValueError('The name of the province column must be provided')

    if convert_mode:
        if not district or not ward:
            warnings.warn('The names of the District or Ward columns are not provided. Therefore, only the Province level will be converted.', UserWarning)
    else:
        if parse_mode in [ParseMode.FROM_2025, ParseMode.FROM_2025.value] and district:
            warnings.warn('FROM_2025 mode is not support with the district level.', UserWarning)

        if parse_mode in [ParseMode.LEGACY, ParseMode.LEGACY.value] and ward and not district:
            raise ValueError('The name of the district column must be provided in order to parse the ward data.')



    # INITIATIVE VARS
    df = df.copy()
    original_columns = df.columns.tolist()


    # CREATE ADDRESS COLUMN, IT IS MERGING KEY
    df['address'] = ''
    for column in admin_unit_columns:
        df['address'] += ',' + df[column].fillna('')
    df_address = df[['address']].drop_duplicates()


    # PARSE ADDRESS TO NEW ADMIN UNIT
    if convert_mode:
        parser = lambda x: convert_address(address=x, mode=convert_mode)
    else:
        if parse_mode in [ParseMode.FROM_2025, ParseMode.FROM_2025.value]:
            level = 2 if ward else 1
        elif parse_mode in [ParseMode.LEGACY, ParseMode.LEGACY.value]:
            level = 3 if ward else 2 if district else 1
        parser = lambda x: parse_address(address=x, mode=parse_mode, level=level, keep_street=False)


    if show_progress:
        tqdm.pandas(desc="Standardizing unique administrative units")
        df_address['admin_unit'] = df_address['address'].progress_apply(parser)
    else:
        df_address['admin_unit'] = df_address['address'].apply(parser)


    # SPLIT ADMIN UNIT TO COLUMNS
    for col_type, col_name in zip(['province', 'district', 'ward'], [province, district, ward]):
        if not col_name:
            continue
        if col_type == 'district' and convert_mode:
            continue  # skip if in convert_mode mode

        attr = f"{'short_' if short_name else ''}{col_type}"
        target_col = col_name if inplace else f"{prefix}{col_name}{suffix}"
        df_address[target_col] = df_address['admin_unit'].apply(lambda x: getattr(x, attr) if x else None)


    # ADD NEW ADMIN UNIT COLUMNS TO DF
    # Drop original columns (province/district/ward) if inplace
    if inplace:
        df.drop(columns=admin_unit_columns, inplace=True, errors='ignore')

    # Merge standardized columns to df
    df = df.merge(df_address.drop(columns=['admin_unit']), on='address', how='left')

    # Drop address columns
    df.drop(columns=['address'], inplace=True)

    # Keep original column position if inplace
    if inplace:
        original_columns = [col for col in original_columns if col in df.columns]
        df = df[original_columns]

    return df


def convert_address_column(df, address: str, convert_mode: Union[str, ConvertMode]=ConvertMode.CONVERT_2025, inplace=False, prefix: str='converted_', suffix :str='', short_name: bool=True, show_progress: bool=True, add_attribute_columns: bool=False):
    '''
    Convert an address column in a DataFrame.

    :param df: `pandas.DataFrame` object.
    :param address: Address column name. Best value format *"(street), ward, district, province"*.
    :param convert_mode: Currently, only `'CONVERT_2025'` is supported.
    :param inplace: Replace the original columns with standardized values; otherwise add new columns. Default `False`.
    :param prefix: Added to new column names if `inplace=False`.
    :param suffix: Added to new column names if `inplace=False`.
    :param short_name: Use short or full names for administrative units. Default `True`.
    :param show_progress: Display a progress bar during processing. Default `True`.

    :return: `pandas.DataFrame` object.
    '''

    def convert_and_get_address(x):
        try:
            admin_unit = convert_address(address=x, mode=convert_mode)
            old_admin_unit = admin_unit.OldAdminUnit

            new_address = admin_unit.get_address(short_name=short_name)
            new_province = admin_unit.short_province if short_name else admin_unit.province
            new_ward = admin_unit.short_ward if short_name else admin_unit.ward
            new_latitude = admin_unit.latitude
            new_longitude = admin_unit.longitude

            old_province = old_admin_unit.short_province if short_name else old_admin_unit.province
            old_district = old_admin_unit.short_district if short_name else old_admin_unit.district
            old_ward = old_admin_unit.short_ward if short_name else old_admin_unit.ward
            old_latitude = old_admin_unit.latitude
            old_longitude = old_admin_unit.longitude

            return (new_address, new_province, new_ward, new_latitude, new_longitude, old_province, old_district, old_ward, old_latitude, old_longitude)
        except Exception as e:
            warnings.warn(f"Failed to convert {x}. {e}", UserWarning)
            return (None, None, None, None, None, None, None, None, None, None)

    # INITIATIVE VARS
    df = df.copy()
    original_columns = df.columns.tolist()

    # CREATE DISTINCT ADDRESS
    df_address = df[[address]].drop_duplicates()

    # CONVERT ADDRESS
    if show_progress:
        tqdm.pandas(desc="Converting unique addresses")
        df_address['new_info'] = df_address[address].fillna('').progress_apply(convert_and_get_address)
    else:
        df_address['new_info'] = df_address[address].fillna('').apply(convert_and_get_address)

    # SPLIT INFO TO COLUMNS
    df_address["new_address"], df_address["new_province"], df_address["new_ward"], df_address["new_latitude"], df_address["new_longitude"], df_address["old_province"], df_address["old_district"], df_address["old_ward"], df_address["old_latitude"], df_address["old_longitude"] = zip(*df_address["new_info"])
    df_address.drop(columns=["new_info"], inplace=True)
    attr_columns = ["new_province", "new_ward", "new_latitude", "new_longitude", "old_province", "old_district", "old_ward", "old_latitude", "old_longitude"]
    if not add_attribute_columns:
        df_address.drop(columns=attr_columns, inplace=True)


    # ADD NEW ADDRESS TO DF
    df = df.merge(df_address, on=address, how='left')

    # ARRANGEMENT
    if inplace:
        df.drop(columns=[address], inplace=True)
        df.rename(columns={'new_address': address}, inplace=True)
        df = df[original_columns + attr_columns if add_attribute_columns else []]
    else:
        df.rename(columns={'new_address': f'{prefix}{address}{suffix}'}, inplace=True)

    return df