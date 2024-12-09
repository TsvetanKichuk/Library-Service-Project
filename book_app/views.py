from django.shortcuts import render

from rest_framework.viewsets import GenericViewSet

from book_app.models import Book


class BookViewSet(GenericViewSet):
    queryset = Book.objects.all()
