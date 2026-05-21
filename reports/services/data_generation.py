from datetime import datetime, timedelta
import math

from django.utils import timezone

from reports.models import TimeSeriesPoint


def generate_week_data():
    TimeSeriesPoint.objects.all().delete()

    start = timezone.make_aware(datetime(2026, 7, 6, 0, 0))
    step = timedelta(minutes=15)

    rows = []

    for i in range(7 * 24 * 4):
        ts = start + i * step
        hour = ts.hour + ts.minute / 60
        weekday = ts.weekday()

        # Synthetic solar profile, peak around midday
        if 6 <= hour <= 19:
            solar_shape = math.sin(math.pi * (hour - 6) / 13)
            solar_kw = max(0, 200 * solar_shape)
        else:
            solar_kw = 0

        # Synthetic hotel load profile
        base_load = 85
        morning_bump = 25 * math.exp(-((hour - 8) ** 2) / 8)
        afternoon_cooling = 75 * math.exp(-((hour - 16) ** 2) / 10)
        evening_bump = 35 * math.exp(-((hour - 21) ** 2) / 8)

        weekend_factor = 1.08 if weekday >= 5 else 1.0

        load_kw = (base_load + morning_bump + afternoon_cooling + evening_bump) * weekend_factor

        # Scale so peak is close to 200 kW
        load_kw = load_kw * 200 / 215

        # TOU tariff
        if 9 <= hour < 23:
            price = 0.30
        else:
            price = 0.15

        rows.append(
            TimeSeriesPoint(
                timestamp=ts,
                solar_kw=solar_kw,
                load_kw=load_kw,
                grid_price_eur_per_kwh=price,
            )
        )

    TimeSeriesPoint.objects.bulk_create(rows)