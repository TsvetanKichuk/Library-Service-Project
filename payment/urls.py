from django.urls import path, include
from rest_framework import routers

from payment.views import PaymentsViewSet

app_name = "payment"

router = routers.DefaultRouter()
router.register("", PaymentsViewSet)
urlpatterns = [path("", include(router.urls))]