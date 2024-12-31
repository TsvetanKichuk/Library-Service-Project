from django.urls import path, include
from rest_framework import routers

from borrowing.views import BorrowingViewSet, ReturnBorrowingView

app_name = "borrowing"

router = routers.DefaultRouter()
router.register("", BorrowingViewSet)
urlpatterns = [path(
        "return/<int:borrowing_id>/",
        ReturnBorrowingView.as_view(),
        name="return-borrowing",
    ),
    path("", include(router.urls))
]
