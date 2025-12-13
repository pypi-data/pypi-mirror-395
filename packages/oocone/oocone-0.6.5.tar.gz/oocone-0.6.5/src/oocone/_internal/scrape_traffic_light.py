import logging
from typing import Any

from oocone import errors
from oocone.auth import Auth
from oocone.model import UNKNOWN, Quantity, TrafficLightColor, TrafficLightStatus, UnknownT

logger = logging.getLogger(__name__)


async def get_traffic_light_status(auth: Auth) -> TrafficLightStatus:
    """Return the status of the energy traffic light."""
    logger.debug("Scraping current traffic light status...")
    response, _ = await auth.request("GET", "php/getTrafficLightStatus.php")

    try:
        # We parse the response as JSON, even though the Content-Type header might indicate
        # otherwise.
        response_data = await response.json(content_type=None)
    except Exception as e:
        raise errors.UnexpectedResponse from e

    return TrafficLightStatus(
        color=_parse_color(response_data),
        current_energy_price=_parse_current_energy_price(response_data),
    )


def _parse_color(response_data: dict) -> TrafficLightColor | UnknownT:
    try:
        raw = _extract_key_from_response(response_data, "color")
    except KeyError as e:
        logger.warning(e)
        return UNKNOWN

    if raw == "rot":
        return TrafficLightColor.RED
    if raw == "gelb":
        return TrafficLightColor.YELLOW
    if raw == r"grün":
        return TrafficLightColor.GREEN

    logger.warning('Got unexpected color: "%s", raw')
    return UNKNOWN


def _parse_current_energy_price(response_data: dict) -> Quantity | UnknownT:
    try:
        raw = _extract_key_from_response(response_data, "currentEnergyprice")
    except KeyError as e:
        logger.warning(e)
        return UNKNOWN

    try:
        result = Quantity(
            value=float(raw),
            unit="ct/kWh",  # Even though the API does not tell us that directly, the unit is Cents
        )
    except ValueError:
        logger.warning("Could not parse energy price %s as a number", raw)
        return UNKNOWN

    return result


def _extract_key_from_response(response_data: dict[str, Any], key: str) -> Any:
    try:
        result = response_data[key]
    except KeyError:
        msg = f'API response does not contain key "{key}".\nResponse data:\n{response_data}'
        raise KeyError(msg) from None

    return result
