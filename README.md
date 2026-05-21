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

Hotel load is synthetic because there is no clean public 15-minute Cyprus hotel dataset.

Grid tariff:
- Day 09:00-23:00: EUR 0.30/kWh
- Night 23:00-09:00: EUR 0.15/kWh

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

I used AI to help structure the Django project, generate boilerplate code, design the dispatch logic, and draft the README.
