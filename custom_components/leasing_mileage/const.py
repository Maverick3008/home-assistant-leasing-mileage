"""Constants for the Leasing Mileage integration."""

from homeassistant.const import Platform

DOMAIN = "leasing_mileage"
PLATFORMS: list[Platform] = [Platform.SENSOR]

CONF_VEHICLE_NAME = "vehicle_name"
CONF_LEASE_START = "lease_start"
CONF_LEASE_END = "lease_end"
CONF_ODOMETER_ENTITY = "odometer_entity"
CONF_START_ODOMETER = "start_odometer"
CONF_INCLUDED_KM = "included_km"
CONF_EXCESS_COST = "excess_cost"
CONF_DISTANCE_UNIT_SYSTEM = "distance_unit_system"
CONF_CURRENCY = "currency"

UNIT_SYSTEM_METRIC = "metric"
UNIT_SYSTEM_IMPERIAL = "imperial"

CURRENCY_EUR = "EUR"
CURRENCY_USD = "USD"
CURRENCY_GBP = "GBP"
CURRENCY_CHF = "CHF"

DISTANCE_UNITS = {
    UNIT_SYSTEM_METRIC: "km",
    UNIT_SYSTEM_IMPERIAL: "mi",
}

CURRENCY_UNITS = {
    CURRENCY_EUR: "€",
    CURRENCY_USD: "$",
    CURRENCY_GBP: "£",
    CURRENCY_CHF: "CHF",
}

DEFAULT_VEHICLE_NAME = "Cupra"
DEFAULT_LEASE_START = "2024-11-01"
DEFAULT_LEASE_END = "2027-10-30"
DEFAULT_START_ODOMETER = 0.0
DEFAULT_INCLUDED_KM = 32500.0
DEFAULT_EXCESS_COST = 0.10
DEFAULT_DISTANCE_UNIT_SYSTEM = UNIT_SYSTEM_METRIC
DEFAULT_CURRENCY = CURRENCY_EUR

ATTR_VEHICLE_NAME = "vehicle_name"
ATTR_LEASE_START = "lease_start"
ATTR_LEASE_END = "lease_end"
ATTR_ODOMETER_ENTITY = "odometer_entity"
ATTR_START_ODOMETER = "start_odometer"
ATTR_CURRENT_ODOMETER = "current_odometer"
ATTR_DRIVEN_KM = "driven_distance"
ATTR_INCLUDED_KM = "included_distance"
ATTR_EXCESS_COST = "excess_cost"
ATTR_DAYS_SO_FAR = "days_so_far"
ATTR_TOTAL_DAYS = "total_days"
ATTR_REMAINING_DAYS = "remaining_days"
ATTR_DISTANCE_UNIT = "distance_unit"
ATTR_DISTANCE_UNIT_SYSTEM = "distance_unit_system"
ATTR_CURRENCY = "currency"
