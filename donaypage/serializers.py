from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import DonayPage, DonayReceivedTransactions
from tayflutterwave.tay_flutterwave import Flutterwave
from donaypay.settings import flutterwave_secret_key, flutterwave_public_key

flutterwave = Flutterwave(flutterwave_public_key, flutterwave_secret_key)


class DonayPageSerializer(ModelSerializer):
    class Meta:
        model = DonayPage
        fields = '__all__'


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

    def update(self, instance, validated_data):
        pass


class ConfirmPaymentSerializer(serializers.Serializer):
    transaction_reference = serializers.CharField()
    otp = serializers.CharField()

    def create(self, validated_data):
        transaction_reference = validated_data['transaction_reference']
        otp = validated_data['otp']
        return flutterwave.validate_payment_with_card(transaction_reference, otp)

    def update(self, instance, validated_data):
        pass
