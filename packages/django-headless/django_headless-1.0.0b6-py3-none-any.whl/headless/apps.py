from django.apps import AppConfig

from . import VERSION
from .utils import is_runserver, log


class DjangoHeadlessConfig(AppConfig):
    name = "headless"
    label = "headless"

    def ready(self):
        from .registry import headless_registry

        if is_runserver():
            log("\n")
            log("----------------------------------------")
            log("Django Headless")
            log(f"Version {VERSION}")
            log("----------------------------------------")
            log(
                ":white_check_mark:",
                f"[green]Found {len(headless_registry)} exposed models:[/green]",
            )
            for model_config in headless_registry.get_models():
                model = model_config["model"]
                print(f"   - {model._meta.verbose_name} ({model._meta.label_lower})")
