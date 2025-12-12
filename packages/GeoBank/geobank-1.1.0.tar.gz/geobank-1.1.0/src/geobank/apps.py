from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class GeoBankConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "geobank"
    verbose_name = _("GeoBank")
