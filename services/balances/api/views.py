from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from .exceptions import UserDoesNotExist, NegativePoints, ZeroPoints
from .models import Balance
from .serializers import BalanceSerializer


class Balances(APIView):
    """Increase or decrease user points"""
    @swagger_auto_schema(request_body=BalanceSerializer(), responses={201: 'Success.'})
    def post(self, request, format=None):
        serializer = BalanceSerializer(data=request.data)

        if serializer.is_valid():
            user_id = request.data.get('user_id')
            points = request.data.get('points')

            if points < 0:
                balance = Balance.objects.points_sum(user_id=user_id)
                # Check if residual balance negative
                if balance is None:
                    raise UserDoesNotExist()
                if (balance + points) < 0:
                    raise NegativePoints()
                serializer.save()
            elif points == 0:
                raise ZeroPoints()
            else:
                # If incoming points are positive, simply store them
                serializer.save()
            return Response({'detail': "Success."}, status=201)
        else:
            return Response(serializer.errors, status=400)


class UserBalance(APIView):
    """Return user balance by user_id"""
    def get(self, request, user_id, format=None):
        balance = Balance.objects.points_sum(user_id=user_id)

        if balance and balance >= 0:
            jdata = {'balance': balance}
            return Response(jdata, status=200)
        else:
            raise UserDoesNotExist()
