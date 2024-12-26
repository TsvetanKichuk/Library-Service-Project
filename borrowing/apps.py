from django.apps import AppConfig


class BorrowingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "borrowing"

    def ready(self):
        try:
            import borrowing.signals
        except ImportError as e:
            raise ImportError(f"Error importing signals module: {e}")
