from django.apps import AppConfig


class BenevalibreAppConfig(AppConfig):
    name = "benevalibre"

    def ready(self):
        from benevalibre.signal_handlers import connect_signal_handlers

        connect_signal_handlers()
