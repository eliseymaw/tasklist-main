from django.apps import AppConfig
from django.apps import AppConfig


class MainpageConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mainpage'
    
class MainpageConfig(AppConfig):  # Замени 'MainpageConfig' на своё приложение
    default_auto_field = "django.db.models.BigAutoField"
    name = "mainpage"

    def ready(self):
        import mainpage.signals  # Подключаем сигналы
