from django.db import models
from djano.conf import settings

class UserBankDetails(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True)
    bank_code = models.IntegerField()
    account_number = models.BigIntegerField()
