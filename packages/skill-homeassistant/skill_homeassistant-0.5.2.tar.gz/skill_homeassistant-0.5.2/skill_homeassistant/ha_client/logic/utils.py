# pylint: disable=missing-function-docstring,missing-class-docstring,missing-module-docstring

from typing import Optional

from skill_homeassistant.ha_client.constants import SUPPORTED_DEVICES


def map_entity_to_device_type(entity):
    """Map an entity to a device type.

    Args:
        entity (str): The entity to map.
    """
    try:
        if entity.split(".")[0] in SUPPORTED_DEVICES:
            return entity.split(".")[0]
        return None
    except Exception as e:  # pylint: disable=broad-exception-caught
        print(f"Error mapping entity to device type: {e}")
        return None


def check_if_device_type_is_group(device_attributes):
    """Check if a device is a group.

    Args:
        device_attributes (dict): The attributes of the device.
    """
    # Check if icon name in attributes has "-group" in it
    if "icon" in device_attributes:
        if "-group" in device_attributes["icon"]:
            return True
        return False
    return False


def get_device_info(devices_list, device_id):
    return [x for x in devices_list if x["id"] == device_id][0]


def get_percentage_brightness_from_ha_value(brightness) -> int:
    brightness = brightness or 0
    return round(int(brightness) / 255 * 100)


def get_ha_value_from_percentage_brightness(brightness) -> int:
    brightness = brightness or 0
    return round(int(brightness) / 100 * 255)


def search_for_device_by_id(devices_list, device_id) -> Optional[int]:
    """Returns index of device or None if not found."""
    for i, dic in enumerate(devices_list):
        if dic["id"] == device_id:
            return i
    return None
