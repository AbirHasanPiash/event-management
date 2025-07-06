from django.apps import AppConfig


class EventsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
<<<<<<<< HEAD:events_v2/apps.py
    name = 'events_v2'

    def ready(self):
        import events_v2.signals
========
    name = 'events_v3'

    def ready(self):
        import events_v3.signals
>>>>>>>> mid-term-exam:events_v3/apps.py
