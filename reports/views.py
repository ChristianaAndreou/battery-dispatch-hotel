from django.shortcuts import render

# Create your views here.
import base64
from io import BytesIO

import matplotlib.pyplot as plt
from django.shortcuts import render

from reports.models import DispatchResult, TimeSeriesPoint


def weekly_report(request):
    points = list(TimeSeriesPoint.objects.order_by("timestamp"))
    dispatch = list(DispatchResult.objects.order_by("timestamp"))

    step_hours = 0.25

    no_battery_cost = sum(
        max(0, p.load_kw - p.solar_kw) * step_hours * p.grid_price_eur_per_kwh
        for p in points
    )

    with_battery_cost = sum(
        d.grid_import_kw * step_hours * p.grid_price_eur_per_kwh
        for p, d in zip(points, dispatch)
    )

    saving = no_battery_cost - with_battery_cost

    total_charged = sum(d.charged_kwh for d in dispatch)
    total_discharged = sum(d.discharged_kwh for d in dispatch)

    total_solar = sum(p.solar_kw * step_hours for p in points)
    curtailed = sum(d.curtailed_solar_kw * step_hours for d in dispatch)
    solar_self_consumption = 100 * (total_solar - curtailed) / total_solar if total_solar else 0

    labels = [d.timestamp.strftime("%a %H:%M") for d in dispatch]
    soc_values = [d.soc_kwh for d in dispatch]

    plt.figure(figsize=(12, 4))
    plt.plot(labels, soc_values)
    plt.xticks(labels[::24], rotation=45)
    plt.ylabel("SoC (kWh)")
    plt.title("Battery State of Charge")
    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    plt.close()
    buffer.seek(0)
    chart = base64.b64encode(buffer.getvalue()).decode("utf-8")

    return render(
        request,
        "reports/weekly.html",
        {
            "no_battery_cost": no_battery_cost,
            "with_battery_cost": with_battery_cost,
            "saving": saving,
            "total_charged": total_charged,
            "total_discharged": total_discharged,
            "solar_self_consumption": solar_self_consumption,
            "chart": chart,
        },
    )