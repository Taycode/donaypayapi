from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import CreateUserSerializer, LoginSerializer
from tayflutterwave import tay_flutterwave


class SignUpView(APIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = CreateUserSerializer

    @staticmethod
    def post(request):
        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
                data = {'error': 'wrong credentials'}
                return Response(data, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
