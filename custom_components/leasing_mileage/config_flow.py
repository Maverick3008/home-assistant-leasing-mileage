"""Config flow for Leasing Mileage."""

from __future__ import annotations

from datetime import date
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import selector
from homeassistant.helpers.typing import ConfigType
from homeassistant.util import slugify

from .const import (
    CONF_EXCESS_COST,
    CONF_INCLUDED_KM,
    CONF_LEASE_END,
    CONF_LEASE_START,
    CONF_ODOMETER_ENTITY,
    CONF_START_ODOMETER,
    CONF_VEHICLE_NAME,
    DEFAULT_EXCESS_COST,
    DEFAULT_INCLUDED_KM,
    DEFAULT_LEASE_END,
    DEFAULT_LEASE_START,
    DEFAULT_START_ODOMETER,
    DEFAULT_VEHICLE_NAME,
    DOMAIN,
)


def _date_from_string(value: str) -> date:
    """Convert an ISO date string to date."""
    return date.fromisoformat(value)


def _number_selector(min_value: float = 0, step: float = 1) -> selector.NumberSelector:
    """Return a Home Assistant number selector."""
    return selector.NumberSelector(
        selector.NumberSelectorConfig(
            min=min_value,
            max=1_000_000,
            step=step,
            mode=selector.NumberSelectorMode.BOX,
        )
    )


def _required_with_optional_default(key: str, default: Any | None) -> vol.Required:
    """Return a voluptuous Required marker without forcing a None default."""
    if default is None:
        return vol.Required(key)
    return vol.Required(key, default=default)


def _schema(defaults: ConfigType | None = None) -> vol.Schema:
    """Return the config/options schema."""
    defaults = defaults or {}

    return vol.Schema(
        {
            vol.Required(
                CONF_VEHICLE_NAME,
                default=defaults.get(CONF_VEHICLE_NAME, DEFAULT_VEHICLE_NAME),
            ): selector.TextSelector(),
            vol.Required(
                CONF_LEASE_START,
                default=defaults.get(CONF_LEASE_START, DEFAULT_LEASE_START),
            ): selector.DateSelector(),
            vol.Required(
                CONF_LEASE_END,
                default=defaults.get(CONF_LEASE_END, DEFAULT_LEASE_END),
            ): selector.DateSelector(),
            _required_with_optional_default(
                CONF_ODOMETER_ENTITY, defaults.get(CONF_ODOMETER_ENTITY)
            ): selector.EntitySelector(
                selector.EntitySelectorConfig(domain="sensor", "input_number")
            ),
            vol.Required(
                CONF_START_ODOMETER,
                default=defaults.get(CONF_START_ODOMETER, DEFAULT_START_ODOMETER),
            ): _number_selector(0, 1),
            vol.Required(
                CONF_INCLUDED_KM,
                default=defaults.get(CONF_INCLUDED_KM, DEFAULT_INCLUDED_KM),
            ): _number_selector(0, 100),
            vol.Required(
                CONF_EXCESS_COST,
                default=defaults.get(CONF_EXCESS_COST, DEFAULT_EXCESS_COST),
            ): _number_selector(0, 0.01),
        }
    )


def _validate_user_input(user_input: dict[str, Any]) -> dict[str, str]:
    """Validate user input and return config flow errors."""
    errors: dict[str, str] = {}

    vehicle_name = str(user_input.get(CONF_VEHICLE_NAME, "")).strip()
    if not vehicle_name:
        errors[CONF_VEHICLE_NAME] = "vehicle_name_required"

    try:
        lease_start = _date_from_string(user_input[CONF_LEASE_START])
        lease_end = _date_from_string(user_input[CONF_LEASE_END])
    except (KeyError, TypeError, ValueError):
        errors["base"] = "invalid_date"
    else:
        if lease_end <= lease_start:
            errors[CONF_LEASE_END] = "lease_end_before_start"

    for key in (CONF_START_ODOMETER, CONF_INCLUDED_KM, CONF_EXCESS_COST):
        try:
            value = float(user_input[key])
        except (KeyError, TypeError, ValueError):
            errors[key] = "invalid_number"
            continue
        if value < 0:
            errors[key] = "invalid_number"

    if CONF_INCLUDED_KM not in errors and float(user_input.get(CONF_INCLUDED_KM, 0)) <= 0:
        errors[CONF_INCLUDED_KM] = "included_km_required"

    return errors


class LeasingMileageConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Leasing Mileage."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            errors = _validate_user_input(user_input)

            if not errors:
                vehicle_name = str(user_input[CONF_VEHICLE_NAME]).strip()
                user_input[CONF_VEHICLE_NAME] = vehicle_name

                await self.async_set_unique_id(slugify(vehicle_name))
                self._abort_if_unique_id_configured()

                return self.async_create_entry(title=vehicle_name, data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=_schema(user_input),
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> config_entries.OptionsFlow:
        """Create the options flow."""
        return LeasingMileageOptionsFlow()


class LeasingMileageOptionsFlow(config_entries.OptionsFlow):
    """Handle options for Leasing Mileage."""

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        """Manage options."""
        current_values = {**self.config_entry.data, **self.config_entry.options}
        errors: dict[str, str] = {}

        if user_input is not None:
            errors = _validate_user_input(user_input)
            if not errors:
                vehicle_name = str(user_input[CONF_VEHICLE_NAME]).strip()
                user_input[CONF_VEHICLE_NAME] = vehicle_name
                self.hass.config_entries.async_update_entry(
                    self.config_entry, title=vehicle_name
                )
                return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=self.add_suggested_values_to_schema(
                _schema(current_values), current_values
            ),
            errors=errors,
        )
