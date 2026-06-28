# Leasing Mileage für Home Assistant

**Leasing Mileage** ist eine Home-Assistant Custom Integration, die Leasing-Strecken für ein oder mehrere Fahrzeuge berechnet und die zugehörigen Sensoren pro Fahrzeug gruppiert.

Die Integration wird vollständig über die Home-Assistant Oberfläche eingerichtet. Du gibst pro Fahrzeug die Fahrzeugbezeichnung, den Leasingzeitraum, die Kilometerstand-/Meilenstand-Entität, das Einheitensystem, die vereinbarte Leasing-Strecke, den Preis pro Mehr-Strecke und die Währung an.

## Funktionen

Pro Leasingfahrzeug wird ein eigenes Gerät in Home Assistant erstellt. Zu diesem Gerät gehören mehrere Sensoren:

| Sensor | Beschreibung |
|---|---|
| Hochrechnung Leasingende | Prognostizierter Tachostand am Leasingende auf Basis der bisher gefahrenen Strecke pro Tag. |
| Strecke pro Tag | Durchschnittlich gefahrene Strecke pro Tag seit Leasingstart. |
| Prognose Mehrstrecke | Erwartete Mehrstrecke gegenüber der vereinbarten Leasing-Strecke. |
| Leasing Nachzahlung | Geschätzte Nachzahlung anhand der Mehrstrecke und des Preises pro Mehr-Strecke. |
| Reststrecke Leasing | Verbleibende Strecke bis zur vereinbarten Leasing-Strecke. |
| Reststrecke pro Tag | Strecke, die bis Leasingende pro Tag noch gefahren werden kann. |
| Resttage Leasing | Anzahl der verbleibenden Tage bis Leasingende. |

## Beispielkonfiguration in Kilometern

| Feld | Beispiel |
|---|---:|
| Bezeichnung Leasing-Fahrzeug | `Cupra` |
| Leasing Start | `2024-11-01` |
| Leasing Ende | `2027-10-30` |
| Einheitensystem | `Metrisch (km)` |
| Aktueller Kilometerstand | `sensor.garage_homeassistant_kilometerstand` |
| Tachostand zu Leasingstart | `0` |
| Inklusive Leasing-Strecke | `32500` |
| Preis pro Mehr-Strecke bei Überschreitung | `0.10` |
| Währung | `Euro (€)` |

## Beispielkonfiguration in Meilen

| Feld | Beispiel |
|---|---:|
| Einheitensystem | `Imperial (Meilen)` |
| Aktueller Meilenstand | `sensor.car_odometer_miles` |
| Tachostand zu Leasingstart | `0` |
| Inklusive Leasing-Strecke | `20000` |
| Preis pro Mehr-Strecke bei Überschreitung | `0.15` |
| Währung | `US Dollar ($)` |

Wichtig: Die Integration rechnet nicht automatisch zwischen km und mi um. Die Werte für Tachostand, Start-Tachostand und inklusive Leasing-Strecke müssen zur ausgewählten Einheit passen.

Du kannst als Tachostand-Entität entweder einen normalen `sensor` oder einen `input_number` auswählen. Das ist praktisch, wenn du den Wert manuell pflegen möchtest.

Wenn deine Tachostand-Entität den kompletten Tachostand des Autos liefert und das Auto bei Leasingstart nicht bei 0 km bzw. 0 mi war, trage bei **Tachostand zu Leasingstart** den damaligen Tachostand ein.

## Einheiten und Währung

Beim Einrichten oder Bearbeiten eines Fahrzeugs kannst du auswählen:

- **Metrisch (km)**: alle Strecken-Sensoren zeigen `km` bzw. `km/Tag`.
- **Imperial (Meilen)**: alle Strecken-Sensoren zeigen `mi` bzw. `mi/Tag`.

Für den Nachzahlungs-Sensor kannst du auswählen:

- Euro (`€`)
- US Dollar (`$`)
- British Pound (`£`)
- Swiss Franc (`CHF`)

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
gefahrene_strecke = aktueller_tachostand - tachostand_zu_leasingstart
tage_bisher = heute - leasing_start
tage_gesamt = leasing_ende - leasing_start
strecke_pro_tag = gefahrene_strecke / tage_bisher
hochrechnung_gefahrene_strecke = strecke_pro_tag * tage_gesamt
hochrechnung_tachostand = tachostand_zu_leasingstart + hochrechnung_gefahrene_strecke
mehrstrecke = max(hochrechnung_gefahrene_strecke - inklusive_leasing_strecke, 0)
nachzahlung = mehrstrecke * preis_pro_mehr_strecke
```

Die Sensoren aktualisieren sich, wenn sich die Tachostand-Entität ändert, und zusätzlich einmal täglich kurz nach Mitternacht.

## GitHub Repository-Beschreibung

```text
Home Assistant custom integration to track lease mileage, projected distance at lease end, excess distance and estimated excess distance fees per vehicle.
```
