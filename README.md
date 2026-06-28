# Leasing Mileage for Home Assistant

[Deutsch](README.de.md) · [English](README.en.md)

---

## Deutsch

**Leasing Mileage** ist eine Home-Assistant Custom Integration, die Leasing-Strecken für ein oder mehrere Fahrzeuge berechnet und die zugehörigen Sensoren pro Fahrzeug gruppiert.

Die Integration wird vollständig über die Home-Assistant Oberfläche eingerichtet. Pro Fahrzeug kannst du auswählen:

- Bezeichnung Leasing-Fahrzeug
- Leasing Start und Leasing Ende
- Einheitensystem: **Metrisch (km)** oder **Imperial (Meilen)**
- Aktueller Kilometerstand/Meilenstand als `sensor` oder `input_number`
- Tachostand zu Leasingstart
- Inklusive Leasing-Strecke
- Preis pro Mehr-Strecke bei Überschreitung
- Währung: `€`, `$`, `£` oder `CHF`

### Sensoren

| Sensor | Beschreibung |
|---|---|
| Tachostand zum Leasingende | Prognostizierter Tachostand am Leasingende. |
| Strecke pro Tag | Durchschnittlich gefahrene Strecke pro Tag. |
| Prognose Mehrstrecke | Erwartete Mehrstrecke gegenüber der vereinbarten Leasing-Strecke. |
| Leasing Nachzahlung | Geschätzte Nachzahlung in der ausgewählten Währung. |
| Reststrecke Leasing | Verbleibende Strecke bis zur vereinbarten Leasing-Strecke. |
| Reststrecke pro Tag | Verbleibende Strecke pro Tag bis Leasingende. |
| Resttage Leasing | Verbleibende Tage bis Leasingende. |

### Beispiel km

```text
Bezeichnung Leasing-Fahrzeug: Cupra
Leasing Start: 2024-11-01
Leasing Ende: 2027-10-30
Einheitensystem: Metrisch (km)
Aktueller Kilometerstand: sensor.garage_homeassistant_kilometerstand
Tachostand zu Leasingstart: 0
Inklusive Leasing-Strecke: 32500
Preis pro Mehr-Strecke bei Überschreitung: 0.10
Währung: Euro (€)
```

Wichtig: Die Integration rechnet nicht automatisch zwischen km und mi um. Die eingegebenen Werte müssen zur gewählten Einheit passen.

### Installation

Kopiere den Ordner:

```text
custom_components/leasing_mileage
```

nach:

```text
/config/custom_components/leasing_mileage
```

Danach Home Assistant neu starten und die Integration über **Einstellungen → Geräte & Dienste → Integration hinzufügen → Leasing Mileage** hinzufügen.

---

## English

**Leasing Mileage** is a Home Assistant custom integration that calculates lease distance metrics for one or more vehicles and groups all generated sensors per vehicle.

The integration is configured entirely from the Home Assistant UI. For each vehicle, you can choose:

- Lease vehicle name
- Lease start and lease end
- Unit system: **Metric (km)** or **Imperial (miles)**
- Current odometer entity as `sensor` or `input_number`
- Odometer at lease start
- Included lease distance
- Cost per excess distance
- Currency: `€`, `$`, `£` or `CHF`

### Sensors

| Sensor | Description |
|---|---|
| Projected odometer at lease end | Projected odometer value at lease end. |
| Distance per day | Average distance driven per day. |
| Projected excess distance | Expected excess distance compared with the included lease distance. |
| Estimated excess fee | Estimated fee in the selected currency. |
| Remaining lease distance | Remaining distance within the lease budget. |
| Remaining distance per day | Remaining distance per day until lease end. |
| Remaining lease days | Remaining days until lease end. |

### Example km

```text
Lease vehicle name: Cupra
Lease start: 2024-11-01
Lease end: 2027-10-30
Unit system: Metric (km)
Current odometer entity: sensor.garage_homeassistant_kilometerstand
Odometer at lease start: 0
Included lease distance: 32500
Cost per excess distance: 0.10
Currency: Euro (€)
```

Important: The integration does not automatically convert between km and mi. The entered values must match the selected unit system.

### Installation

Copy this folder:

```text
custom_components/leasing_mileage
```

to:

```text
/config/custom_components/leasing_mileage
```

Then restart Home Assistant and add the integration from **Settings → Devices & services → Add integration → Leasing Mileage**.
