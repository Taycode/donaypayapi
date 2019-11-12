from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import CreateUserSerializer, LoginSerializer
from account.serializers import UserBankDetailsSerializer
from .forms import LoginForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate


def login_view(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect('index')
        else:
            form = LoginForm
            args = {'form': form}
            return render(request, 'account/login.html', args)

    else:
        username = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return redirect('normal_login')


def index(request):
    if request.user.is_authenticated:
        return render(request, 'account/index.html')
    else:
        return redirect('normal_login')


def logout_view(request):
    logout(request)
    return redirect('index')


class SignUpView(APIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = CreateUserSerializer

    @staticmethod
    def post(request):
        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            serializer.data.update({'status': 'success'})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            serializer.errors.update({'status': 'fail'})
            return Response(serializer.errors, status=status.HTTP_200_OK)


class LoginView(APIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = LoginSerializer

    @staticmethod
    def post(request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.authenticate_user(serializer.data)
            if user is not None:
                return Response(user, status=status.HTTP_200_OK)

            else:
                data = {'status': 'fail', 'error': 'wrong credentials'}
                return Response(data, status=status.HTTP_200_OK)

        else:
            serializer.errors.update({'status': 'fail'})
            return Response(serializer.errors, status=status.HTTP_200_OK)


class UserBankDetailView(APIView):
    serializer_class = UserBankDetailsSerializer

    @staticmethod
    def post(request):
        serializer = UserBankDetailsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            serializer.data.update({{'status': 'success'}})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            serializer.errors.update({{'status': 'fail'}})
            return Response(serializer.errors, status=status.HTTP_200_OK)
