from django.apps import AppConfig


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cleaning_app.main'

    # def ready(self):
    #     import cleaning_app.main.signals