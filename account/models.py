from django.db import models
from django.contrib.auth.models import User


class UserBankDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True)
    bank_code = models.IntegerField()
    account_number = models.BigIntegerField()
