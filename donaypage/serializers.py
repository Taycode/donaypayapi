from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from account.models import UserBankDetails
from tayflutterwave.tay_flutterwave import Flutterwave
from .models import DonayPage, DonayReceivedTransactions
from .utils import get_flutterwave_sdk

flutterwave = get_flutterwave_sdk()


class DonayPageSerializer(ModelSerializer):
    class Meta:
        model = DonayPage
        fields = '__all__'


class DonayPageCreateSerializer(ModelSerializer):
    class Meta:
        model = DonayPage
        exclude = ['reached_amount', 'percentage']


class DonayReceivedTransactionsSerializer(ModelSerializer):
    class Meta:
        model = DonayReceivedTransactions
        fields = '__all__'


class PaymentFieldSerializer(serializers.Serializer):
    cardno = serializers.CharField(max_length=16, required=True)
    cvv = serializers.CharField(max_length=3, required=True)
    expirymonth = serializers.CharField(max_length=2, required=True)
    expiryyear = serializers.CharField(max_length=2, required=True)
    currency = serializers.CharField(max_length=3, default='NGN')
    suggested_auth = serializers.CharField(default='pin', max_length=10)
    pin = serializers.CharField(max_length=4, required=True)
    amount = serializers.CharField(max_length=10, required=True)
    txRef = serializers.CharField(max_length=20)
    email = serializers.EmailField(required=True)
    phonenumber = serializers.IntegerField(required=False)
    firstname = serializers.CharField(max_length=30)
    lastname = serializers.CharField(max_length=30)

    def create(self, validated_data):
        return flutterwave.pay_via_card(validated_data)


class ConfirmPaymentSerializer(serializers.Serializer):
    transaction_reference = serializers.CharField()
    otp = serializers.CharField()

    def create(self, validated_data):
        transaction_reference = validated_data['transaction_reference']
        otp = validated_data['otp']
        return flutterwave.validate_payment_with_card(transaction_reference, otp)
