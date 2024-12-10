from django.urls import path, include

from rest_framework import routers

from book_app.views import BookViewSet

router = routers.DefaultRouter()
router.register("book", BookViewSet)
urlpatterns = [path("", include(router.urls))]

app_name = "book_app"
