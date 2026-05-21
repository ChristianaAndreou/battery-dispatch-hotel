from django.urls import path

from reports.views import weekly_report

urlpatterns = [
    path("weekly/", weekly_report, name="weekly_report"),
]