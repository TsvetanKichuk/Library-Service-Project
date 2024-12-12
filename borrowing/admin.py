from django.contrib import admin

from borrowing.models import Borrowing, Payments

admin.site.register(Borrowing)
admin.site.register(Payments)
