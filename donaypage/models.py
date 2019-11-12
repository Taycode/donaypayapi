from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class DonayPage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    title = models.CharField(max_length=30)
    reached_amount = models.BigIntegerField(default=0)
    expected_amount = models.BigIntegerField()
    description = models.CharField(max_length=400)

    def __str__(self):
        return self.title


class DonayReceivedTransactions(models.Model):
    donaypage = models.ForeignKey(DonayPage, on_delete=models.CASCADE)
    reference = models.CharField(max_length=30, blank=True)
    amount = models.BigIntegerField(default=0)
    sender_name = models.CharField(max_length=50, blank=True)
    status = models.BooleanField(default=False)



