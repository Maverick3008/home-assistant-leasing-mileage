"""Sensor platform for Leasing Mileage."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import date
from decimal import Decimal, InvalidOperation
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CURRENCY_EURO, STATE_UNAVAILABLE, STATE_UNKNOWN, UnitOfTime
from homeassistant.core import Event, HomeAssistant, callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import async_track_state_change_event, async_track_time_change
from homeassistant.util import dt as dt_util

from .const import (
    ATTR_CURRENT_ODOMETER,
    ATTR_DAYS_SO_FAR,
    ATTR_DRIVEN_KM,
    ATTR_EXCESS_COST,
    ATTR_INCLUDED_KM,
    ATTR_LEASE_END,
    ATTR_LEASE_START,
    ATTR_ODOMETER_ENTITY,
    ATTR_REMAINING_DAYS,
    ATTR_START_ODOMETER,
    ATTR_TOTAL_DAYS,
    ATTR_VEHICLE_NAME,
    CONF_EXCESS_COST,
    CONF_INCLUDED_KM,
    CONF_LEASE_END,
    CONF_LEASE_START,
    CONF_ODOMETER_ENTITY,
    CONF_START_ODOMETER,
    CONF_VEHICLE_NAME,
    DOMAIN,
)


@dataclass(frozen=True, slots=True)
class LeaseMetrics:
    """Calculated lease metrics."""

    vehicle_name: str
    lease_start: date
    lease_end: date
    odometer_entity: str
    current_odometer: float
    start_odometer: float
    driven_km: float
    included_km: float
    excess_cost: float
    days_so_far: int
    total_days: int
    remaining_days: int

    @property
    def km_per_day(self) -> float:
        """Return the average driven kilometers per day."""
        if self.days_so_far <= 0:
            return 0.0
        return self.driven_km / self.days_so_far

    @property
    def projected_driven_km(self) -> float:
        """Return projected driven kilometers for the whole lease period."""
        return self.km_per_day * self.total_days

    @property
    def projected_odometer_at_end(self) -> float:
        """Return projected odometer value at lease end."""
        return self.start_odometer + self.projected_driven_km

    @property
    def projected_excess_km(self) -> float:
        """Return projected excess mileage."""
        return max(self.projected_driven_km - self.included_km, 0.0)

    @property
    def estimated_excess_fee(self) -> float:
        """Return estimated excess mileage fee."""
        return self.projected_excess_km * self.excess_cost

    @property
    def remaining_lease_km(self) -> float:
        """Return remaining mileage budget within the lease."""
        return self.included_km - self.driven_km

    @property
    def remaining_km_per_day(self) -> float:
        """Return remaining mileage budget per remaining day."""
        if self.remaining_days <= 0:
            return 0.0
        return self.remaining_lease_km / self.remaining_days


@dataclass(frozen=True, kw_only=True)
class LeasingSensorEntityDescription(SensorEntityDescription):
    """Description of a Leasing Mileage sensor."""

    value_fn: Callable[[LeaseMetrics], float | int | None]
    precision: int = 0


SENSOR_DESCRIPTIONS: tuple[LeasingSensorEntityDescription, ...] = (
    LeasingSensorEntityDescription(
        key="projected_odometer_at_lease_end",
        name="Kilometerstand zum Leasingende",
        native_unit_of_measurement="km",
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:car-clock",
        value_fn=lambda metrics: metrics.projected_odometer_at_end,
        precision=0,
    ),
    LeasingSensorEntityDescription(
        key="km_per_day",
        name="km pro Tag",
        native_unit_of_measurement="km/Tag",
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:calendar-arrow-right",
        value_fn=lambda metrics: metrics.km_per_day,
        precision=2,
    ),
    LeasingSensorEntityDescription(
        key="projected_excess_km",
        name="Prognose Mehrkilometer",
        native_unit_of_measurement="km",
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:map-marker-distance",
        value_fn=lambda metrics: metrics.projected_excess_km,
        precision=0,
    ),
    LeasingSensorEntityDescription(
        key="estimated_excess_fee",
        name="Leasing Nachzahlung",
        native_unit_of_measurement=CURRENCY_EURO,
        device_class=SensorDeviceClass.MONETARY,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:cash-clock",
        value_fn=lambda metrics: metrics.estimated_excess_fee,
        precision=2,
    ),
    LeasingSensorEntityDescription(
        key="remaining_lease_km",
        name="Restkilometer Leasing",
        native_unit_of_measurement="km",
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:counter",
        value_fn=lambda metrics: metrics.remaining_lease_km,
        precision=0,
    ),
    LeasingSensorEntityDescription(
        key="remaining_km_per_day",
        name="Restkilometer pro Tag",
        native_unit_of_measurement="km/Tag",
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:calendar-today",
        value_fn=lambda metrics: metrics.remaining_km_per_day,
        precision=2,
    ),
    LeasingSensorEntityDescription(
        key="remaining_days",
        name="Resttage Leasing",
        native_unit_of_measurement=UnitOfTime.DAYS,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:calendar-end",
        value_fn=lambda metrics: metrics.remaining_days,
        precision=0,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Leasing Mileage sensors."""
    async_add_entities(
        LeasingMileageSensor(hass, entry, description)
        for description in SENSOR_DESCRIPTIONS
    )


class LeasingMileageSensor(SensorEntity):
    """Representation of a Leasing Mileage sensor."""

    entity_description: LeasingSensorEntityDescription
    _attr_has_entity_name = False

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
        description: LeasingSensorEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        self.hass = hass
        self._entry = entry
        self.entity_description = description
        self._attr_unique_id = f"{entry.entry_id}_{description.key}"
        self._attr_name = f"{self._config[CONF_VEHICLE_NAME]} {description.name}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=self._config[CONF_VEHICLE_NAME],
            manufacturer="Leasing Mileage",
            model="Lease mileage calculator",
        )

    @property
    def _config(self) -> dict[str, Any]:
        """Return merged entry data and options."""
        return {**self._entry.data, **self._entry.options}

    async def async_added_to_hass(self) -> None:
        """Subscribe to source sensor and daily updates."""
        self.async_on_remove(
            async_track_state_change_event(
                self.hass,
                [self._config[CONF_ODOMETER_ENTITY]],
                self._handle_source_sensor_update,
            )
        )
        self.async_on_remove(
            async_track_time_change(
                self.hass,
                self._handle_daily_update,
                hour=0,
                minute=1,
                second=0,
            )
        )

    @callback
    def _handle_source_sensor_update(self, event: Event) -> None:
        """Handle updates of the source odometer sensor."""
        self.async_write_ha_state()

    @callback
    def _handle_daily_update(self, now: Any) -> None:
        """Refresh daily because date-based sensors change without state changes."""
        self.async_write_ha_state()

    @property
    def available(self) -> bool:
        """Return whether the sensor is available."""
        return self._calculate_metrics() is not None

    @property
    def native_value(self) -> float | int | None:
        """Return the state of the sensor."""
        metrics = self._calculate_metrics()
        if metrics is None:
            return None

        value = self.entity_description.value_fn(metrics)
        if value is None:
            return None

        rounded_value = round(float(value), self.entity_description.precision)
        if self.entity_description.precision == 0:
            return int(rounded_value)
        return rounded_value

    @property
    def extra_state_attributes(self) -> dict[str, Any] | None:
        """Return additional attributes useful for debugging and dashboards."""
        metrics = self._calculate_metrics()
        if metrics is None:
            return None

        return {
            ATTR_VEHICLE_NAME: metrics.vehicle_name,
            ATTR_LEASE_START: metrics.lease_start.isoformat(),
            ATTR_LEASE_END: metrics.lease_end.isoformat(),
            ATTR_ODOMETER_ENTITY: metrics.odometer_entity,
            ATTR_START_ODOMETER: round(metrics.start_odometer, 2),
            ATTR_CURRENT_ODOMETER: round(metrics.current_odometer, 2),
            ATTR_DRIVEN_KM: round(metrics.driven_km, 2),
            ATTR_INCLUDED_KM: round(metrics.included_km, 2),
            ATTR_EXCESS_COST: round(metrics.excess_cost, 4),
            ATTR_DAYS_SO_FAR: metrics.days_so_far,
            ATTR_TOTAL_DAYS: metrics.total_days,
            ATTR_REMAINING_DAYS: metrics.remaining_days,
        }

    def _calculate_metrics(self) -> LeaseMetrics | None:
        """Calculate metrics from config and the current odometer sensor state."""
        config = self._config
        odometer_state = self.hass.states.get(config[CONF_ODOMETER_ENTITY])
        if odometer_state is None or odometer_state.state in (
            STATE_UNKNOWN,
            STATE_UNAVAILABLE,
            "none",
        ):
            return None

        current_odometer = _as_float(odometer_state.state)
        if current_odometer is None:
            return None

        try:
            lease_start = date.fromisoformat(config[CONF_LEASE_START])
            lease_end = date.fromisoformat(config[CONF_LEASE_END])
        except (TypeError, ValueError):
            return None

        if lease_end <= lease_start:
            return None

        today = dt_util.now().date()
        start_odometer = float(config.get(CONF_START_ODOMETER, 0))
        included_km = float(config[CONF_INCLUDED_KM])
        excess_cost = float(config[CONF_EXCESS_COST])

        days_so_far = max((today - lease_start).days, 0)
        total_days = max((lease_end - lease_start).days, 0)
        remaining_days = max((lease_end - today).days, 0)
        driven_km = max(current_odometer - start_odometer, 0.0)

        return LeaseMetrics(
            vehicle_name=str(config[CONF_VEHICLE_NAME]),
            lease_start=lease_start,
            lease_end=lease_end,
            odometer_entity=str(config[CONF_ODOMETER_ENTITY]),
            current_odometer=current_odometer,
            start_odometer=start_odometer,
            driven_km=driven_km,
            included_km=included_km,
            excess_cost=excess_cost,
            days_so_far=days_so_far,
            total_days=total_days,
            remaining_days=remaining_days,
        )


def _as_float(value: Any) -> float | None:
    """Convert a Home Assistant state string to float."""
    try:
        return float(Decimal(str(value).replace(",", ".")))
    except (InvalidOperation, ValueError):
        return None
