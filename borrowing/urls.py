from django.urls import path, include
from rest_framework import routers

from borrowing.views import BorrowingViewSet, PaymentsViewSet

app_name = "borrowing"

router = routers.DefaultRouter()
router.register("borrowings", BorrowingViewSet)
router.register("payments", PaymentsViewSet)

urlpatterns = [path("", include(router.urls))]
