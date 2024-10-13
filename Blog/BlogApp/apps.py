from django.apps import AppConfig


class BlogappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'BlogApp'


class BlogAppConfig(AppConfig):
    name = 'BlogApp'

    def ready(self):
        import BlogApp.signals  # Import the signals.py file