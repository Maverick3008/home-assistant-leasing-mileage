"""Config flow for Leasing Mileage."""

from __future__ import annotations

from datetime import date
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import selector
from homeassistant.helpers.typing import ConfigType
from homeassistant.util import slugify

from .const import (
    CONF_CURRENCY,
    CONF_DISTANCE_UNIT_SYSTEM,
    CONF_EXCESS_COST,
    CONF_INCLUDED_KM,
    CONF_LEASE_END,
    CONF_LEASE_START,
    CONF_ODOMETER_ENTITY,
    CONF_START_ODOMETER,
    CONF_VEHICLE_NAME,
    CURRENCY_CHF,
    CURRENCY_EUR,
    CURRENCY_GBP,
    CURRENCY_USD,
    DEFAULT_CURRENCY,
    DEFAULT_DISTANCE_UNIT_SYSTEM,
    DEFAULT_EXCESS_COST,
    DEFAULT_INCLUDED_KM,
    DEFAULT_LEASE_END,
    DEFAULT_LEASE_START,
    DEFAULT_START_ODOMETER,
    DEFAULT_VEHICLE_NAME,
    DOMAIN,
    UNIT_SYSTEM_IMPERIAL,
    UNIT_SYSTEM_METRIC,
)

UNIT_SYSTEM_OPTIONS = [UNIT_SYSTEM_METRIC, UNIT_SYSTEM_IMPERIAL]

CURRENCY_OPTIONS = [CURRENCY_EUR, CURRENCY_USD, CURRENCY_GBP, CURRENCY_CHF]

VALID_UNIT_SYSTEMS = {UNIT_SYSTEM_METRIC, UNIT_SYSTEM_IMPERIAL}
VALID_CURRENCIES = {CURRENCY_EUR, CURRENCY_USD, CURRENCY_GBP, CURRENCY_CHF}

# These two select fields have a hard fallback label because some Home Assistant
# versions/custom-integration translation caches can show the raw data keys for
# SelectSelector fields in config flows.
FIELD_LABELS = {
    CONF_DISTANCE_UNIT_SYSTEM: {
        "de": "Einheitensystem wählen",
        "en": "Select unit system",
    },
    CONF_CURRENCY: {
        "de": "Währung",
        "en": "Currency",
    },
}

UNIT_SYSTEM_LABELS = {
    UNIT_SYSTEM_METRIC: {
        "de": "Metrisch (km)",
        "en": "Metric (km)",
    },
    UNIT_SYSTEM_IMPERIAL: {
        "de": "Imperial (Meilen)",
        "en": "Imperial (miles)",
    },
}

CURRENCY_LABELS = {
    CURRENCY_EUR: {
        "de": "Euro (€)",
        "en": "Euro (€)",
    },
    CURRENCY_USD: {
        "de": "US-Dollar ($)",
        "en": "US Dollar ($)",
    },
    CURRENCY_GBP: {
        "de": "Britisches Pfund (£)",
        "en": "British Pound (£)",
    },
    CURRENCY_CHF: {
        "de": "Schweizer Franken (CHF)",
        "en": "Swiss Franc (CHF)",
    },
}


def _language(hass: HomeAssistant | None = None) -> str:
    """Return the Home Assistant language as a simple language code."""
    language = "en"
    if hass is not None and getattr(hass.config, "language", None):
        language = str(hass.config.language)
    return "de" if language.lower().startswith("de") else "en"


def _label(labels: dict[str, str], language: str) -> str:
    """Return a localized label with English fallback."""
    return labels.get(language, labels["en"])


def _form_key(key: str, language: str) -> str:
    """Return the key used in the visible form."""
    if key in FIELD_LABELS:
        return _label(FIELD_LABELS[key], language)
    return key


def _normalize_user_input(
    user_input: dict[str, Any] | None, language: str
) -> dict[str, Any] | None:
    """Normalize visible form labels back to internal config keys."""
    if user_input is None:
        return None

    normalized = dict(user_input)
    for internal_key, labels in FIELD_LABELS.items():
        candidate_keys = {internal_key, *labels.values(), _form_key(internal_key, language)}
        for candidate_key in candidate_keys:
            if candidate_key in normalized:
                normalized[internal_key] = normalized.pop(candidate_key)
                break

    return normalized


def _display_errors(errors: dict[str, str], language: str) -> dict[str, str]:
    """Map internal error keys to visible form keys."""
    return {_form_key(key, language): value for key, value in errors.items()}


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


def _select_selector(
    options: list[str], option_labels: dict[str, dict[str, str]], language: str
) -> selector.SelectSelector:
    """Return a Home Assistant select selector displayed as radio/list buttons."""
    return selector.SelectSelector(
        selector.SelectSelectorConfig(
            options=[
                {"value": option, "label": _label(option_labels[option], language)}
                for option in options
            ],
            mode=selector.SelectSelectorMode.LIST,
        )
    )


def _required_with_optional_default(key: str, default: Any | None) -> vol.Required:
    """Return a voluptuous Required marker without forcing a None default."""
    if default is None:
        return vol.Required(key)
    return vol.Required(key, default=default)


def _schema(defaults: ConfigType | None = None, language: str = "en") -> vol.Schema:
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
            vol.Required(
                _form_key(CONF_DISTANCE_UNIT_SYSTEM, language),
                default=defaults.get(
                    CONF_DISTANCE_UNIT_SYSTEM, DEFAULT_DISTANCE_UNIT_SYSTEM
                ),
            ): _select_selector(UNIT_SYSTEM_OPTIONS, UNIT_SYSTEM_LABELS, language),
            _required_with_optional_default(
                CONF_ODOMETER_ENTITY, defaults.get(CONF_ODOMETER_ENTITY)
            ): selector.EntitySelector(
                selector.EntitySelectorConfig(domain=["sensor", "input_number"])
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
            vol.Required(
                _form_key(CONF_CURRENCY, language),
                default=defaults.get(CONF_CURRENCY, DEFAULT_CURRENCY),
            ): _select_selector(CURRENCY_OPTIONS, CURRENCY_LABELS, language),
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

    if user_input.get(CONF_DISTANCE_UNIT_SYSTEM) not in VALID_UNIT_SYSTEMS:
        errors[CONF_DISTANCE_UNIT_SYSTEM] = "invalid_unit_system"

    if user_input.get(CONF_CURRENCY) not in VALID_CURRENCIES:
        errors[CONF_CURRENCY] = "invalid_currency"

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
        language = _language(self.hass)
        normalized_input = _normalize_user_input(user_input, language)
        errors: dict[str, str] = {}

        if normalized_input is not None:
            errors = _validate_user_input(normalized_input)

            if not errors:
                vehicle_name = str(normalized_input[CONF_VEHICLE_NAME]).strip()
                normalized_input[CONF_VEHICLE_NAME] = vehicle_name

                await self.async_set_unique_id(slugify(vehicle_name))
                self._abort_if_unique_id_configured()

                return self.async_create_entry(title=vehicle_name, data=normalized_input)

        return self.async_show_form(
            step_id="user",
            data_schema=_schema(normalized_input, language),
            errors=_display_errors(errors, language),
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
        language = _language(self.hass)
        current_values = {**self.config_entry.data, **self.config_entry.options}
        current_values.setdefault(CONF_DISTANCE_UNIT_SYSTEM, DEFAULT_DISTANCE_UNIT_SYSTEM)
        current_values.setdefault(CONF_CURRENCY, DEFAULT_CURRENCY)
        normalized_input = _normalize_user_input(user_input, language)
        errors: dict[str, str] = {}

        if normalized_input is not None:
            errors = _validate_user_input(normalized_input)
            if not errors:
                vehicle_name = str(normalized_input[CONF_VEHICLE_NAME]).strip()
                normalized_input[CONF_VEHICLE_NAME] = vehicle_name
                self.hass.config_entries.async_update_entry(
                    self.config_entry, title=vehicle_name
                )
                return self.async_create_entry(title="", data=normalized_input)

        schema_defaults = normalized_input or current_values

        return self.async_show_form(
            step_id="init",
            data_schema=self.add_suggested_values_to_schema(
                _schema(schema_defaults, language), schema_defaults
            ),
            errors=_display_errors(errors, language),
        )
