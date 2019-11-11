from django.contrib import admin
from .models import DonayReceivedTransactions, DonayPage


admin.site.register(DonayPage)
admin.site.register(DonayReceivedTransactions)
