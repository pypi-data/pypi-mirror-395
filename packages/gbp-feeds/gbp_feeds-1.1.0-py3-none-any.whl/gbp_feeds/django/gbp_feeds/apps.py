"""AppConfigs for gbp-ps"""

from django.apps import AppConfig


class GBPFeedsConfig(AppConfig):
    """AppConfig for gbp-feeds"""

    name = "gbp_feeds.django.gbp_feeds"
    verbose_name = "GBP-feeds"
    default_auto_field = "django.db.models.BigAutoField"
