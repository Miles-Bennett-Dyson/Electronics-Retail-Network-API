from rest_framework.routers import DefaultRouter

from retail.apps import RetailConfig
from retail.views import RetailViewSet, ProductViewSet

app_name = RetailConfig.name

router = DefaultRouter()
router.register(r"retail", RetailViewSet, basename="retail")
router.register(r"product", ProductViewSet, basename="product")

urlpatterns = [
] + router.urls
