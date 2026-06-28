# Leasing Mileage for Home Assistant

**Leasing Mileage** is a Home Assistant custom integration that calculates lease mileage for one or more vehicles and groups all related sensors per vehicle.

The integration is fully configured through the Home Assistant UI. For each vehicle, you enter the vehicle name, lease period, odometer sensor, included lease mileage and cost per excess kilometer.

## Features

Each configured lease vehicle creates its own Home Assistant device. The device contains several sensors:

| Sensor | Description |
|---|---|
| Projected mileage at lease end | Projected odometer reading at the end of the lease based on the average mileage per day so far. |
| Mileage per day | Average kilometers driven per day since the lease start date. |
| Projected excess mileage | Estimated excess kilometers compared with the included lease mileage. |
| Estimated excess mileage fee | Estimated fee based on projected excess kilometers and cost per excess kilometer. |
| Remaining lease mileage | Remaining kilometers until the included lease mileage is reached. |
| Remaining mileage per day | Kilometers that can still be driven per day until the lease end date. |
| Lease days remaining | Number of days remaining until the lease end date. |

## Example configuration

| Field | Example |
|---|---:|
| Lease vehicle name | `Cupra` |
| Lease start | `2024-11-01` |
| Lease end | `2027-10-30` |
| Current odometer sensor | `sensor.cupra_leon_kilometerstand` |
| Odometer at lease start | `0` |
| Included lease mileage | `32500` |
| Cost per excess km | `0.10` |

If your odometer sensor returns the full vehicle odometer reading and the vehicle did not start at 0 km when the lease began, enter the odometer reading from the lease start date in **Odometer at lease start**.

## HACS custom repository installation

1. Create a GitHub repository, for example `home-assistant-leasing-mileage`.
2. Upload all files from this project to the repository.
3. Open HACS in Home Assistant.
4. Click the three-dot menu → **Custom repositories**.
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

Then restart Home Assistant and add the integration through the Home Assistant UI.

## Multiple vehicles

You can add the integration multiple times. Each vehicle gets its own config entry and its own Home Assistant device.

## Calculation logic

```text
driven_km = current_odometer - start_odometer
days_so_far = today - lease_start
total_days = lease_end - lease_start
km_per_day = driven_km / days_so_far
projected_driven_km = km_per_day * total_days
projected_odometer = start_odometer + projected_driven_km
excess_km = max(projected_driven_km - included_lease_km, 0)
excess_fee = excess_km * cost_per_excess_km
```

The sensors update whenever the odometer sensor changes and once per day shortly after midnight.

## GitHub repository description

```text
Home Assistant custom integration to track lease mileage, projected mileage at lease end, excess kilometers and estimated excess mileage fees per vehicle.
```
