import math

from reports.models import DispatchResult, TimeSeriesPoint


BATTERY_CAPACITY_KWH = 400
MAX_POWER_KW = 200
MIN_SOC_KWH = BATTERY_CAPACITY_KWH * 0.10
MAX_SOC_KWH = BATTERY_CAPACITY_KWH * 0.95
INITIAL_SOC_KWH = BATTERY_CAPACITY_KWH * 0.50
ROUND_TRIP_EFFICIENCY = 0.88
CHARGE_EFFICIENCY = math.sqrt(ROUND_TRIP_EFFICIENCY)
DISCHARGE_EFFICIENCY = math.sqrt(ROUND_TRIP_EFFICIENCY)
STEP_HOURS = 0.25


def run_dispatch():
    DispatchResult.objects.all().delete()

    soc = INITIAL_SOC_KWH
    results = []

    points = TimeSeriesPoint.objects.order_by("timestamp")

    for point in points:
        solar_kw = point.solar_kw
        load_kw = point.load_kw
        price = point.grid_price_eur_per_kwh

        solar_used_for_load_kw = min(solar_kw, load_kw)
        remaining_load_kw = load_kw - solar_used_for_load_kw
        surplus_solar_kw = max(0, solar_kw - load_kw)

        battery_power_kw = 0
        grid_import_kw = 0
        curtailed_solar_kw = 0
        charged_kwh = 0
        discharged_kwh = 0

        # Charge from surplus solar
        if surplus_solar_kw > 0:
            available_capacity_kwh = MAX_SOC_KWH - soc
            max_charge_by_capacity_kw = available_capacity_kwh / (STEP_HOURS * CHARGE_EFFICIENCY)
            charge_kw = min(surplus_solar_kw, MAX_POWER_KW, max_charge_by_capacity_kw)

            charged_kwh = charge_kw * STEP_HOURS
            soc += charged_kwh * CHARGE_EFFICIENCY
            battery_power_kw = -charge_kw
            curtailed_solar_kw = surplus_solar_kw - charge_kw

        # Discharge during day-rate hours
        elif remaining_load_kw > 0 and price >= 0.30:
            available_energy_kwh = soc - MIN_SOC_KWH
            max_discharge_by_soc_kw = (available_energy_kwh * DISCHARGE_EFFICIENCY) / STEP_HOURS
            discharge_kw = min(remaining_load_kw, MAX_POWER_KW, max_discharge_by_soc_kw)

            discharged_kwh = discharge_kw * STEP_HOURS
            soc -= discharged_kwh / DISCHARGE_EFFICIENCY
            battery_power_kw = discharge_kw
            remaining_load_kw -= discharge_kw

            grid_import_kw = remaining_load_kw

        else:
            grid_import_kw = remaining_load_kw

        results.append(
            DispatchResult(
                timestamp=point.timestamp,
                soc_kwh=soc,
                battery_power_kw=battery_power_kw,
                grid_import_kw=grid_import_kw,
                curtailed_solar_kw=curtailed_solar_kw,
                charged_kwh=charged_kwh,
                discharged_kwh=discharged_kwh,
            )
        )

    DispatchResult.objects.bulk_create(results)