from django.apps import AppConfig


class FileExplorerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "file_explorer"
    verbose_name = "文件管理器"

    def ready(self):
        """应用启动时的初始化"""
        try:
            import file_explorer.signals
        except ImportError:
            pass
