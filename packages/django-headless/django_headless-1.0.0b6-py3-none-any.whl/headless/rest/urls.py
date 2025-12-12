from .routers import rest_router, singleton_urls

urlpatterns = rest_router.urls + singleton_urls
