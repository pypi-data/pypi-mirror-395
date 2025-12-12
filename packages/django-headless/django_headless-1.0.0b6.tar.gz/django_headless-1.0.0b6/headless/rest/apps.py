from django.apps import AppConfig

from ..utils import is_runserver


class DjangoHeadlessRestConfig(AppConfig):
    name = "headless.rest"
    label = "headless_rest"

    def ready(self):
        from .builder import RestBuilder

        if is_runserver():
            builder = RestBuilder()
            builder.build()
