# Battery Dispatch Hotel

Small Django service for a behind-the-meter battery dispatch use case for a hotel in Limassol, Cyprus.

## Setup

python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_data
python manage.py runserver

Open:
http://127.0.0.1:8000/reports/weekly/

## Data sources

Solar production is generated as a synthetic 200 kWp PV profile for Limassol, Cyprus.

In a production version, I would pull hourly PV data from renewables.ninja and resample it to 15-minute intervals.

Hotel load is synthetic because there is no clean public 15-minute Cyprus hotel dataset. I modelled a reasonable hotel demand shape with higher afternoon cooling demand and scaled it so the weekly peak is around 200 kW.

Grid tariff:

Day 09:00-23:00: EUR 0.30/kWh
Night 23:00-09:00: EUR 0.15/kWh

## Assumptions

- The hotel load profile is synthetic because I could not find a clean public 15-minute Cyprus hotel dataset.
- The load profile is shaped to represent a hotel with higher afternoon cooling demand and some daily/weekly variation.
- The weekly peak load is scaled to approximately 200 kW.
- The solar profile is synthetic and represents a 200 kWp rooftop PV system in Limassol.
- The tariff uses the provided stylised two-rate TOU structure, not a real EAC commercial tariff.
- Grid export is not allowed, so surplus solar is either stored in the battery or curtailed.
- The dispatch policy is greedy rather than optimised with a linear programming solver.

## Battery assumptions

- Battery capacity: 400 kWh
- Battery power limit: 200 kW
- Minimum SoC: 10%
- Maximum SoC: 95%
- Initial SoC: 50%
- Round-trip efficiency: 88%
- No grid export allowed

## Dispatch policy

Solar covers load first. Surplus solar charges the battery. During expensive day-rate hours, the battery discharges to reduce grid imports. Any surplus solar that cannot be stored is curtailed.

## What I would build next

- Pull real renewables.ninja solar data
- Pull a real EAC commercial tariff
- Add a what-if form for PV and battery size
- Improve dispatch using optimisation
- Add more charts

## AI usage

I used AI as a coding assistant to help structure the Django project, generate boilerplate code, design the dispatch logic, and draft the README. I was responsible for implementing, testing, adapting, and integrating the final application.