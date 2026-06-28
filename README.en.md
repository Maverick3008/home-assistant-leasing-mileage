# Leasing Mileage for Home Assistant

**Leasing Mileage** is a Home Assistant custom integration that calculates lease distance metrics for one or more vehicles and groups all generated sensors per vehicle.

The integration is configured entirely from the Home Assistant UI. For each vehicle, you enter the vehicle name, lease period, odometer entity, unit system, included lease distance, cost per excess distance and currency.

## Features

Each lease vehicle is represented as its own Home Assistant device. The integration creates these sensors for the device:

| Sensor | Description |
|---|---|
| Projected odometer at lease end | Projected odometer value at the end of the lease based on the distance driven per day so far. |
| Distance per day | Average distance driven per day since the lease start. |
| Projected excess distance | Expected excess distance compared with the included lease distance. |
| Estimated excess fee | Estimated fee based on excess distance and cost per excess distance. |
| Remaining lease distance | Remaining distance budget within the lease. |
| Remaining distance per day | Distance that can still be driven per day until the lease end. |
| Remaining lease days | Number of remaining days until the lease end. |

## Example configuration in kilometers

| Field | Example |
|---|---:|
| Lease vehicle name | `Cupra` |
| Lease start | `2024-11-01` |
| Lease end | `2027-10-30` |
| Unit system | `Metric (km)` |
| Current odometer entity | `sensor.garage_homeassistant_kilometerstand` |
| Odometer at lease start | `0` |
| Included lease distance | `32500` |
| Cost per excess distance | `0.10` |
| Currency | `Euro (€)` |

## Example configuration in miles

| Field | Example |
|---|---:|
| Unit system | `Imperial (miles)` |
| Current odometer entity | `sensor.car_odometer_miles` |
| Odometer at lease start | `0` |
| Included lease distance | `20000` |
| Cost per excess distance | `0.15` |
| Currency | `US Dollar ($)` |

Important: The integration does not automatically convert between km and mi. The odometer value, lease-start odometer value and included lease distance must match the selected unit system.

The odometer entity can be either a regular `sensor` or an `input_number`. This is useful if you want to maintain the odometer value manually.

If your odometer entity reports the full vehicle odometer and the vehicle did not start the lease at 0 km or 0 mi, enter the odometer value from the lease start in **Odometer at lease start**.

## Units and currency

When adding or editing a vehicle, you can choose:

- **Metric (km)**: all distance sensors show `km` or `km/day`.
- **Imperial (miles)**: all distance sensors show `mi` or `mi/day`.

For the estimated excess fee sensor, you can choose:

- Euro (`€`)
- US Dollar (`$`)
- British Pound (`£`)
- Swiss Franc (`CHF`)

## HACS installation as a custom repository

1. Create a GitHub repository, for example `home-assistant-leasing-mileage`.
2. Upload all files from this project to the repository.
3. Open HACS in Home Assistant.
4. Open the three-dot menu in the top right → **Custom repositories**.
5. Add the repository URL.
6. Select category **Integration**.
7. Install the integration.
8. Restart Home Assistant.
9. Go to **Settings → Devices & services → Add integration → Leasing Mileage**.

## Manual installation

Copy this folder:

```text
custom_components/leasing_mileage
```

to:

```text
/config/custom_components/leasing_mileage
```

Then restart Home Assistant and add the integration from the Home Assistant UI.

## Multiple vehicles

You can add the integration multiple times. Each vehicle gets its own config entry and its own Home Assistant device.

## Calculation logic

```text
driven_distance = current_odometer - lease_start_odometer
days_so_far = today - lease_start
total_days = lease_end - lease_start
distance_per_day = driven_distance / days_so_far
projected_driven_distance = distance_per_day * total_days
projected_odometer = lease_start_odometer + projected_driven_distance
excess_distance = max(projected_driven_distance - included_lease_distance, 0)
estimated_fee = excess_distance * cost_per_excess_distance
```

The sensors update when the odometer entity changes and once per day shortly after midnight.

## GitHub repository description

```text
Home Assistant custom integration to track lease mileage, projected distance at lease end, excess distance and estimated excess distance fees per vehicle.
```
