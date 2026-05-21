from django.db import models

# Create your models here.
class TimeSeriesPoint(models.Model):
    timestamp = models.DateTimeField(unique=True)
    solar_kw = models.FloatField()
    load_kw = models.FloatField()
    grid_price_eur_per_kwh = models.FloatField()

    def __str__(self):
        return f"{self.timestamp} | solar={self.solar_kw:.1f} load={self.load_kw:.1f}"


class DispatchResult(models.Model):
    timestamp = models.DateTimeField(unique=True)
    soc_kwh = models.FloatField()
    battery_power_kw = models.FloatField()
    grid_import_kw = models.FloatField()
    curtailed_solar_kw = models.FloatField()
    charged_kwh = models.FloatField()
    discharged_kwh = models.FloatField()

    def __str__(self):
        return f"{self.timestamp} | SoC={self.soc_kwh:.1f} kWh"