from rest_framework.serializers import ModelSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .models import UserBankDetails


User = get_user_model()


class CreateUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'].lower(),
            username=validated_data['email'].lower(),
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user=user)
        return user


class LoginSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']

    def authenticate_user(self, validated_data):
        username = self.validated_data['email'].lower()
        password = self.validated_data['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            token = user.auth_token.key
            data = {'status': 'success', 'token': token, 'username': username}
            return data
        return None


class UserBankDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBankDetails
        fields = '__all__'
