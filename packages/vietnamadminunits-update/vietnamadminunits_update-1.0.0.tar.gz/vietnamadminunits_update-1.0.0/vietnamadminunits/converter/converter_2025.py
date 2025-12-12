import json
import sys
from pathlib import Path
import re


MODULE_DIR = Path(__file__).parent.parent


from ..parser import parse_address, ParseMode
from ..parser.objects import AdminUnit
from ..parser.utils import get_geo_location, check_point_in_polygon, find_nearest_point


# LOAD DATA
with open(MODULE_DIR / 'data/converter_2025.json', 'r') as f:
    converter_data = json.load(f)


DICT_PROVINCE = converter_data['DICT_PROVINCE']
DICT_PROVINCE_WARD_NO_DIVIDED = converter_data['DICT_PROVINCE_WARD_NO_DIVIDED']
DICT_PROVINCE_WARD_DIVIDED = converter_data['DICT_PROVINCE_WARD_DIVIDED']


# MAIN FUNCTION
def convert_address_2025(address: str):
    '''
    Convert address from old format to new format based on the Vietnam administrative unit changes in 2025
    :param address: str - The old address to convert

    :return: AdminUnit object
    '''

    new_ward_key = None

    # Parse địa chỉ cũ trước
    old_unit = parse_address(address, mode=ParseMode.LEGACY, keep_street=True, level=3)

    # Suy province_key cũ ra province_key mới
    new_province_key = next((k for k, v in DICT_PROVINCE.items() if old_unit.province_key and old_unit.province_key in v), None)

    # Tạo old_province_district_ward_key để suy ra ward_key mới
    # Vẫn cho phép trả về province nếu như không có ward_key mới, thay vì raise error
    special_zone = ['huyenbachlongvi', 'huyenconco', 'huyenhoangsa', 'huyenlyson', 'huyencondao'] # Mấy cái đảo thì không có ward
    if old_unit.ward_key or old_unit.district_key in special_zone:
        
        # Ghép các key trong admin unit cũ lại thành old_province_district_ward_key
        old_province_district_ward_key = f"{old_unit.province_key}_{old_unit.district_key}_{old_unit.ward_key if old_unit.ward_key else ''}"

        # 1st attempt: Suy từ old_province_district_ward_key ra new_ward_key, phần lớn các ward cũ không bị chia
        DICT_WARD_NO_DIVIDED = DICT_PROVINCE_WARD_NO_DIVIDED[new_province_key]
        new_ward_key = next((k for k, v in DICT_WARD_NO_DIVIDED.items() if old_province_district_ward_key and old_province_district_ward_key in v), None)


        # 2nd attampt: Các ward cũ bị chia thành nhiều ward mới
        if not new_ward_key:
            new_wards = DICT_PROVINCE_WARD_DIVIDED.get(new_province_key, {}).get(old_province_district_ward_key, [])

            # Nếu không có street thì dùng ngay ward mới mặc định
            if not old_unit.street:
                new_ward_key = next((ward['newWardKey'] for ward in new_wards if ward['isDefaultNewWard']), None)

            # Nếu có street thì lấy location của địa chỉ cũ để so sánh với polygon và location của các ward mới
            else:
                old_location = get_geo_location(old_unit.get_address())

                # Cũng có lúc địa chỉ vớ vẫn không tìm được location
                if old_location:
                    old_point = (old_location.latitude, old_location.longitude)

                    # Tạo danh sách
                    containing_points = [] # Location của ward mới mà có Polygon chứa location của ward cũ
                    new_ward_points = [] # Tất cả location của ward cũ

                    for ward in new_wards:
                        new_point = (ward['newWardLat'], ward['newWardLon'])
                        new_ward_points.append(new_point)
                        is_contain = check_point_in_polygon(point=old_point, polygon_center=new_point, polygon_area_km2=ward['newWardAreaKm2'])
                        if is_contain:
                            containing_points.append(new_point)

                    # Tìm location của ward mới gần với location của ward cũ nhất
                    nearest_point = find_nearest_point(a_point=old_point, list_of_b_points=new_ward_points)

                    # Quyết định:
                    # Nếu chỉ có một ward mới chứa location của ward cũ > chọn ward mới đó
                    if len(containing_points) == 1:
                        default_ward_point = containing_points[0]

                    # Còn lại thì chọn ward mới gần nhất
                    else:
                        default_ward_point = nearest_point


                    # Suy location của ward mới ra new_ward_key
                    new_ward_key = next((ward['newWardKey'] for ward in new_wards if (ward['newWardLat'], ward['newWardLon']) == default_ward_point), None)

                else:
                    new_ward_key = next((ward['newWardKey'] for ward in new_wards if ward['isDefaultNewWard']), None)


    # Tạo lại một địa chỉ theo 34-province format để parse lại
    # Lý do vì convert data sẽ không được cập nhật. Khi chính phủ có những thay đổi, parser data và alias keyword của nó được cập nhật
    new_address_components = [i for i in (old_unit.street, new_ward_key, new_province_key) if i]
    new_address = ','.join(new_address_components)

    level = 2 if new_ward_key else 1
    new_unit = parse_address(new_address, mode=ParseMode.FROM_2025, keep_street=True, level=level)
    new_unit.OldAdminUnit = old_unit

    return new_unit


# REVERSE CONVERSION FUNCTION
def convert_address_to_old_2025(address: str):
    '''
    Convert address from new format (34-province) to old format (63-province) based on the Vietnam administrative unit changes in 2025
    :param address: str - The new address to convert

    :return: AdminUnit object
    '''

    old_ward_key = None
    old_district_key = None

    # Parse địa chỉ mới trước
    new_unit = parse_address(address, mode=ParseMode.FROM_2025, keep_street=True, level=2)

    # Suy province_key mới ra province_key cũ
    # DICT_PROVINCE maps: {new_province_key: [list of old_province_keys]}
    old_province_key = None
    old_province_district_ward_key = None

    # Tạo old_province_district_ward_key từ ward_key mới
    if new_unit.ward_key and new_unit.province_key:
        
        # 1st attempt: Suy từ new_ward_key ra old_province_district_ward_key, phần lớn các ward cũ không bị chia
        DICT_WARD_NO_DIVIDED = DICT_PROVINCE_WARD_NO_DIVIDED.get(new_unit.province_key, {})
        old_province_district_ward_keys = DICT_WARD_NO_DIVIDED.get(new_unit.ward_key, [])
        
        if old_province_district_ward_keys:
            # Pick the first old key
            old_province_district_ward_key = old_province_district_ward_keys[0]
        else:
            # 2nd attempt: Các ward cũ bị chia thành nhiều ward mới
            # DICT_PROVINCE_WARD_DIVIDED maps: {new_province_key: {old_province_district_ward_key: [list of new ward info]}}
            DICT_WARD_DIVIDED = DICT_PROVINCE_WARD_DIVIDED.get(new_unit.province_key, {})
            
            # Search for old_province_district_ward_key that contains our new_ward_key
            for old_key, new_wards in DICT_WARD_DIVIDED.items():
                if any(ward.get('newWardKey') == new_unit.ward_key for ward in new_wards):
                    old_province_district_ward_key = old_key
                    break
            
            # If still not found and we have street, try using location
            if not old_province_district_ward_key and new_unit.street:
                new_location = get_geo_location(new_unit.get_address())
                
                if new_location:
                    new_point = (new_location.latitude, new_location.longitude)
                    
                    # Find which old ward's polygon contains this point
                    containing_old_keys = []
                    for old_key, new_wards in DICT_WARD_DIVIDED.items():
                        for ward in new_wards:
                            if ward.get('newWardKey') == new_unit.ward_key:
                                ward_point = (ward.get('newWardLat'), ward.get('newWardLon'))
                                is_contain = check_point_in_polygon(
                                    point=new_point, 
                                    polygon_center=ward_point, 
                                    polygon_area_km2=ward.get('newWardAreaKm2', 0)
                                )
                                if is_contain:
                                    containing_old_keys.append(old_key)
                    
                    if len(containing_old_keys) == 1:
                        old_province_district_ward_key = containing_old_keys[0]
                    elif containing_old_keys:
                        # Multiple matches, pick first
                        old_province_district_ward_key = containing_old_keys[0]
            
            # If still not found, try to find default
            if not old_province_district_ward_key:
                for old_key, new_wards in DICT_WARD_DIVIDED.items():
                    if any(ward.get('newWardKey') == new_unit.ward_key and ward.get('isDefaultNewWard', False) for ward in new_wards):
                        old_province_district_ward_key = old_key
                        break
                
                # Last resort: pick first match
                if not old_province_district_ward_key:
                    for old_key, new_wards in DICT_WARD_DIVIDED.items():
                        if any(ward.get('newWardKey') == new_unit.ward_key for ward in new_wards):
                            old_province_district_ward_key = old_key
                            break

        # Parse old_province_district_ward_key to extract old_province_key, old_district_key and old_ward_key
        if old_province_district_ward_key:
            parts = old_province_district_ward_key.split('_')
            if len(parts) >= 1:
                old_province_key = parts[0] if parts[0] else None
                old_district_key = parts[1] if len(parts) > 1 and parts[1] else None
                old_ward_key = parts[2] if len(parts) > 2 and parts[2] else None
    elif new_unit.province_key:
        # No ward, just get province
        old_province_keys = DICT_PROVINCE.get(new_unit.province_key, [])
        if old_province_keys:
            # Pick the first old province key (usually the main one)
            old_province_key = old_province_keys[0]

    # Tạo lại một địa chỉ theo 63-province format để parse lại
    old_address_components = [i for i in (new_unit.street, old_ward_key, old_district_key, old_province_key) if i]
    old_address = ','.join(old_address_components)

    level = 3 if old_ward_key else (2 if old_district_key else 1)
    old_unit = parse_address(old_address, mode=ParseMode.LEGACY, keep_street=True, level=level)
    old_unit.NewAdminUnit = new_unit

    return old_unit