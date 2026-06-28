# Leasing Mileage für Home Assistant

**Leasing Mileage** ist eine Home-Assistant Custom Integration, die Leasing-Kilometer für ein oder mehrere Fahrzeuge berechnet und die zugehörigen Sensoren pro Fahrzeug gruppiert.

Die Integration wird vollständig über die Home-Assistant Oberfläche eingerichtet. Du gibst pro Fahrzeug die Fahrzeugbezeichnung, den Leasingzeitraum, den Kilometerstand-Sensor, die vereinbarte Leasinglaufleistung und die Kosten pro Mehrkilometer an.

## Funktionen

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

## Beispielkonfiguration

| Feld | Beispiel |
|---|---:|
| Bezeichnung Leasing-Fahrzeug | `Cupra` |
| Leasing Start | `2024-11-01` |
| Leasing Ende | `2027-10-30` |
| Aktueller Kilometerstand | `sensor.cupra_leon_kilometerstand` |
| Kilometerstand zu Leasingstart | `0` |
| Inklusive Leasing-Kilometer | `32500` |
| Kosten je Mehr-km | `0.10` |

Wenn dein Kilometerstand-Sensor den kompletten Tachostand des Autos liefert und das Auto bei Leasingstart nicht bei 0 km war, trage bei **Kilometerstand zu Leasingstart** den damaligen Tachostand ein.

## Installation über HACS als Custom Repository

1. Repository in GitHub erstellen, zum Beispiel `home-assistant-leasing-mileage`.
2. Alle Dateien aus diesem Projekt in das Repository hochladen.
3. In Home Assistant HACS öffnen.
4. Drei Punkte oben rechts → **Custom repositories**.
5. Repository-URL einfügen.
6. Kategorie **Integration** auswählen.
7. Integration installieren.
8. Home Assistant neu starten.
9. **Einstellungen → Geräte & Dienste → Integration hinzufügen → Leasing Mileage** öffnen.

## Manuelle Installation

Kopiere diesen Ordner:

```text
custom_components/leasing_mileage
```

nach:

```text
/config/custom_components/leasing_mileage
```

Danach Home Assistant neu starten und die Integration über die Home-Assistant Oberfläche hinzufügen.

## Mehrere Fahrzeuge

Du kannst die Integration mehrfach hinzufügen. Jedes Fahrzeug bekommt einen eigenen Config Entry und ein eigenes Gerät in Home Assistant.

## Berechnungslogik

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

Die Sensoren aktualisieren sich, wenn sich der Kilometerstand-Sensor ändert, und zusätzlich einmal täglich kurz nach Mitternacht.

## GitHub Repository-Beschreibung

```text
Home Assistant custom integration to track lease mileage, projected mileage at lease end, excess kilometers and estimated excess mileage fees per vehicle.
```
