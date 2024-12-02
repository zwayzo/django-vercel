from django.apps import AppConfig
# import playground

class PlaygroundConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'playground'
    def ready(self):
        import playground.signals