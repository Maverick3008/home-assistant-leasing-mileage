# Leasing Mileage for Home Assistant

[Deutsch](#deutsch) | [English](#english)

---

## Deutsch

**Leasing Mileage** ist eine Home-Assistant Custom Integration, die Leasing-Kilometer für ein oder mehrere Fahrzeuge berechnet und die zugehörigen Sensoren pro Fahrzeug gruppiert.

Die Integration wird vollständig über die Home-Assistant Oberfläche eingerichtet. Du gibst pro Fahrzeug die Fahrzeugbezeichnung, den Leasingzeitraum, die Kilometerstand-Entität, die vereinbarte Leasinglaufleistung und die Kosten pro Mehrkilometer an.

### Funktionen

Pro Leasingfahrzeug wird ein eigenes Gerät in Home Assistant erstellt. Zu diesem Gerät gehören mehrere Sensoren:

| Sensor | Beschreibung |
|---|---|
| Hochrechnung Leasingende | Prognostizierter Kilometerstand am Leasingende auf Basis der bisher gefahrenen Kilometer pro Tag. |
| Kilometer pro Tag | Durchschnittlich gefahrene Kilometer pro Tag seit Leasingstart. |
| Prognose Mehrkilometer | Erwartete Mehrkilometer gegenüber der vereinbarten Leasinglaufleistung. |
| Leasing Nachzahlung | Geschätzte Nachzahlung anhand der Mehrkilometer und der Kosten pro Mehrkilometer. |
| Restkilometer Leasing | Verbleibende Kilometer bis zur vereinbarten Leasinglaufleistung. |
| Restkilometer pro Tag | Kilometer, die bis Leasingende pro Tag noch gefahren werden können. |
| Resttage Leasing | Anzahl der verbleibenden Tage bis Leasingende. |

### Beispielkonfiguration

Für dein Cupra-Beispiel wären die Werte im Einrichtungsdialog:

| Feld | Beispiel |
|---|---:|
| Bezeichnung Leasing-Fahrzeug | `Cupra` |
| Leasing Start | `2024-11-01` |
| Leasing Ende | `2027-10-30` |
| Aktueller Kilometerstand | `sensor.garage_homeassistant_kilometerstand` |
| Kilometerstand zu Leasingstart | `0` |
| Inklusive Leasing-Kilometer | `32500` |
| Kosten je Mehr-km | `0.10` |

Du kannst als Kilometerstand-Entität entweder einen normalen `sensor` oder einen `input_number` auswählen. Das ist praktisch, wenn du den Kilometerstand manuell pflegen möchtest.

Wenn deine Kilometerstand-Entität den kompletten Tachostand des Autos liefert und das Auto bei Leasingstart nicht bei 0 km war, trage bei **Kilometerstand zu Leasingstart** den damaligen Tachostand ein. Die Berechnung nutzt dann nur die gefahrenen Kilometer innerhalb des Leasingzeitraums.

### Installation über HACS als Custom Repository

1. Repository in GitHub erstellen, zum Beispiel `home-assistant-leasing-mileage`.
2. Alle Dateien aus diesem Projekt in das Repository hochladen.
3. In Home Assistant HACS öffnen.
4. Drei Punkte oben rechts → **Custom repositories**.
5. Repository-URL einfügen.
6. Kategorie **Integration** auswählen.
7. Integration installieren.
8. Home Assistant neu starten.
9. **Einstellungen → Geräte & Dienste → Integration hinzufügen → Leasing Mileage** öffnen.

### Manuelle Installation

Kopiere diesen Ordner:

```text
custom_components/leasing_mileage
```

nach:

```text
/config/custom_components/leasing_mileage
```

Danach Home Assistant neu starten und die Integration über die Home-Assistant Oberfläche hinzufügen.

### Mehrere Fahrzeuge

Du kannst die Integration mehrfach hinzufügen. Jedes Fahrzeug bekommt einen eigenen Config Entry und ein eigenes Gerät in Home Assistant.

### Berechnungslogik

Die Integration berechnet intern:

```text
gefahrene_km = aktueller_kilometerstand - kilometerstand_zu_leasingstart
tage_bisher = heute - leasing_start
tage_gesamt = leasing_ende - leasing_start
km_pro_tag = gefahrene_km / tage_bisher
hochrechnung_gefahrene_km = km_pro_tag * tage_gesamt
hochrechnung_kilometerstand = kilometerstand_zu_leasingstart + hochrechnung_gefahrene_km
mehrkilometer = max(hochrechnung_gefahrene_km - inklusive_leasing_km, 0)
nachzahlung = mehrkilometer * kosten_je_mehr_km
```

Die Sensoren aktualisieren sich, wenn sich die Kilometerstand-Entität ändert, und zusätzlich einmal täglich kurz nach Mitternacht.

### Repository-Beschreibung für GitHub

```text
Home Assistant custom integration to track lease mileage, projected mileage at lease end, excess kilometers and estimated excess mileage fees per vehicle.
```

---

## English

**Leasing Mileage** is a Home Assistant custom integration that calculates lease mileage for one or more vehicles and groups all related sensors per vehicle.

The integration is fully configured through the Home Assistant UI. For each vehicle, you enter the vehicle name, lease period, odometer entity, included lease mileage and cost per excess kilometer.

### Features

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

### Example configuration

For the Cupra example, the setup dialog would use these values:

| Field | Example |
|---|---:|
| Lease vehicle name | `Cupra` |
| Lease start | `2024-11-01` |
| Lease end | `2027-10-30` |
| Current odometer entity | `sensor.garage_homeassistant_kilometerstand` |
| Odometer at lease start | `0` |
| Included lease mileage | `32500` |
| Cost per excess km | `0.10` |

You can select either a regular `sensor` or an `input_number` as the odometer entity. This is useful if you want to maintain the odometer value manually.

If your odometer entity returns the full vehicle odometer reading and the vehicle did not start at 0 km when the lease began, enter the odometer reading from the lease start date in **Odometer at lease start**. The integration will then only use kilometers driven during the lease period.

### HACS custom repository installation

1. Create a GitHub repository, for example `home-assistant-leasing-mileage`.
2. Upload all files from this project to the repository.
3. Open HACS in Home Assistant.
4. Click the three-dot menu → **Custom repositories**.
5. Add the repository URL.
6. Select category **Integration**.
7. Install the integration.
8. Restart Home Assistant.
9. Go to **Settings → Devices & services → Add integration → Leasing Mileage**.

### Manual installation

Copy this folder:

```text
custom_components/leasing_mileage
```

to:

```text
/config/custom_components/leasing_mileage
```

Then restart Home Assistant and add the integration through the Home Assistant UI.

### Multiple vehicles

You can add the integration multiple times. Each vehicle gets its own config entry and its own Home Assistant device.

### Calculation logic

Internally, the integration calculates:

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

The sensors update whenever the odometer entity changes and once per day shortly after midnight.

### GitHub repository description

```text
Home Assistant custom integration to track lease mileage, projected mileage at lease end, excess kilometers and estimated excess mileage fees per vehicle.
```

## Units

All distance and mileage sensors use fixed `km`. The integration intentionally does not assign Home Assistant's `distance` device class to kilometer sensors so Home Assistant does not automatically convert the display to `mi`.
