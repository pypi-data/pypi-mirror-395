from typing import Type

from django.db.models import Model
from django.urls import path
from rest_framework.viewsets import ModelViewSet

from ..registry import ModelConfig, headless_registry
from ..utils import log
from .routers import rest_router, singleton_urls
from .viewsets import SingletonViewSet
from ..settings import headless_settings


class RestBuilder:
    """
    Class for building a REST API for the models in the headless
    registry.
    """

    def __init__(self):
        self._models = headless_registry.get_models()
        self._serializer_classes = {}

    def build(self):
        """
        Builds the REST API by creating view sets and serializers and registering them
        to the router.
        :return:
        """
        log(":building_construction:", "Setting up REST routes")

        for model_config in self._models:
            model_class = model_config["model"]
            singleton = model_config["singleton"]
            view_set = self.get_view_set(model_config)
            base_path = model_class._meta.label_lower

            if singleton:
                singleton_urls.append(
                    path(
                        base_path,
                        view_set.as_view(
                            {
                                "get": "retrieve",
                                "put": "update",
                                "patch": "partial_update",
                            }
                        ),
                    )
                )
            else:
                rest_router.register(base_path, view_set)

    def get_serializer(self, model_class: Type[Model]):
        model_name = model_class._meta.label

        # Return serializer class from cache if it exists
        if self._serializer_classes.get(model_name, None):
            return self._serializer_classes[model_name]

        class Serializer(headless_settings.DEFAULT_SERIALIZER_CLASS):
            class Meta:
                model = model_class
                fields = "__all__"

        self._serializer_classes[model_name] = Serializer

        return Serializer

    def get_view_set(self, model_config: ModelConfig):
        model_class = model_config["model"]
        singleton = model_config["singleton"]
        serializer = self.get_serializer(model_class)

        if singleton:

            class ViewSet(SingletonViewSet):
                queryset = model_class.objects.none()
                serializer_class = serializer

                def get_queryset(self):
                    return model_class.objects.first()

        else:

            class ViewSet(ModelViewSet):
                queryset = model_class.objects.all()
                serializer_class = serializer
                search_fields = model_config["search_fields"]

        return ViewSet
