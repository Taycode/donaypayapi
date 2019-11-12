from rest_framework.response import Response
from .serializers import (
    DonayPageSerializer,
    PaymentFieldSerializer,
    ConfirmPaymentSerializer,
    DonayReceivedTransactionsSerializer
)
from rest_framework.views import APIView
from rest_framework import status
from .models import DonayPage, DonayReceivedTransactions
from rest_framework.parsers import JSONParser, MultiPartParser


class CreateDonayPage(APIView):
    serializer_class = DonayPageSerializer
    parser_classes = [JSONParser, MultiPartParser]

    @staticmethod
    def post(request):
        serializer = DonayPageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            serializer.data.update({'status': 'success'})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            serializer.errors.update({'status': 'fail'})
            return Response(serializer.errors, status=status.HTTP_200_OK)


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
    permission_classes = ()

    @staticmethod
    def post(request, pk):
        serializer = PaymentFieldSerializer(data=request.data)
        if serializer.is_valid():
            donaypage_instance = DonayPage.objects.get(pk=pk)
            res = serializer.save()
            if res['status'] == 'success':
                data = {
                    'donaypage': donaypage_instance.pk,
                    'reference': res['data']['txRef'],
                    'amount': res['data']['amount'],
                    'sender_name': serializer.initial_data['firstname'] + ' ' + serializer.initial_data['lastname']
                }
                serializer = DonayReceivedTransactionsSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(res, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyPayment(APIView):
    serializer_class = ConfirmPaymentSerializer
    permission_classes = ()

    @staticmethod
    def post(request, pk):
        donaypage_instance = DonayPage.objects.get(pk=pk)
        serializer = ConfirmPaymentSerializer(data=request.data)
        if serializer.is_valid():
            res = serializer.save()
            if res['status'] == 'success':
                tx_ref = res['data']['tx']['txRef']
                donay_received_transaction = DonayReceivedTransactions.objects.get(reference=tx_ref)

                serializer = DonayReceivedTransactionsSerializer(donay_received_transaction)
                data = {
                    'donaypage': donaypage_instance.id,
                    'reference': serializer.data['reference'],
                    'amount': serializer.data['amount'],
                    'sender_name': serializer.data['sender_name'],
                    'status': True
                }
                serializer = DonayReceivedTransactionsSerializer(instance=donay_received_transaction, data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ViewAllDonayPages(APIView):
    serializer_class = DonayPageSerializer
    permission_classes = ()

    @staticmethod
    def get(request):
        data = DonayPage.objects.all()
        serializer = DonayPageSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
