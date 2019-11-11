from rest_framework.response import Response
from .serializers import DonayPageSerializer, PaymentFieldSerializer, ConfirmPaymentSerializer
from rest_framework.views import APIView
from rest_framework import status
from .models import DonayPage


class CreateDonayPage(APIView):
    serializer_class = DonayPageSerializer

    @staticmethod
    def post(request):
        serializer = DonayPageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ViewDonayPage(APIView):
    serializer_class = DonayPageSerializer
    permission_classes = ()

    @staticmethod
    def get(request, pk):
        donaypage = DonayPage.objects.get(id=pk)
        serializer = DonayPageSerializer(donaypage)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CollectPayment(APIView):
    serializer_class = PaymentFieldSerializer

    @staticmethod
    def post(request):
        serializer = PaymentFieldSerializer(data=request.data)
        if serializer.is_valid():
            res = serializer.save()
            return Response(res, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyPayment(APIView):
    serializer_class = ConfirmPaymentSerializer

    @staticmethod
    def post(request):
        serializer = PaymentFieldSerializer(data=request.data)
        if serializer.is_valid():
            res = serializer.save()
            return Response(res, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
