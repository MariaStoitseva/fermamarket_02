from django.apps import AppConfig


class CustomusersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fermamarket_02.customusers'

    def ready(self):
        import fermamarket_02.customusers.signals
