from django.db import models
from django.db.models.signals import post_save
from django.conf import settings
from cloudinary.models import CloudinaryField
from tayflutterwave.tay_flutterwave import Flutterwave
from account.models import UserBankDetails
from .utils import get_flutterwave_sdk


flutterwave = get_flutterwave_sdk()


class DonayPage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True)
    title = models.CharField(max_length=30)
    reached_amount = models.BigIntegerField(default=0)
    expected_amount = models.BigIntegerField()
    beneficiary = models.CharField(max_length=50, blank=True)
    description = models.CharField(max_length=400)
    image = CloudinaryField('image', blank=True)
    percentage = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class DonayReceivedTransactions(models.Model):
    donaypage = models.ForeignKey(DonayPage, on_delete=models.CASCADE)
    reference = models.CharField(max_length=30, blank=True)
    amount = models.BigIntegerField(default=0)
    sender_name = models.CharField(max_length=50, blank=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return "{} - {}".format(self.reference, self.donaypage.title)


def add_to_reached_amount(sender, **kwargs):
    donaypage_instance = kwargs['instance'].donaypage
    if not kwargs['created']:
        if kwargs['instance'].status:
            donaypage_instance.reached_amount += kwargs['instance'].amount
            percentage = (donaypage_instance.reached_amount / donaypage_instance.expected_amount) * 100
            donaypage_instance.percentage = int(round(percentage))
            donaypage_instance.save()
            if donaypage_instance.reached_amount >= donaypage_instance.expected_amount:
                bank_details = UserBankDetails.objects.get(user=donaypage_instance.user)

                data = {
                        "account_bank": bank_details.bank_code,
                        "account_number": bank_details.account_number,
                        "amount": donaypage_instance.reached_amount,
                        "narration": "Donated on Donaypay",
                        "currency": "NGN",
                        "reference": "alphadevs",

                }
                res = flutterwave.transfer_to_bank(data)
                print(res)


post_save.connect(add_to_reached_amount, DonayReceivedTransactions)
