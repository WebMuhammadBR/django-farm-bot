from rest_framework.views import APIView
from rest_framework.response import Response
from query.models.counterparties import Farmer
from .serializers import FarmerSerializer
from django.db.models import Sum
from django.db.models.functions import Coalesce
from decimal import Decimal
from rest_framework.generics import ListAPIView
from .serializers import FarmerSummarySerializer
from query.models.bot import BotUser


class FarmerListAPIView(APIView):

    def get(self, request):
        farmers = (
            Farmer.objects
            .filter(is_active=True)
            .select_related("massive__district__region")
            .order_by(
                "massive__district__id",
                "massive__id",
                "name"
            )


        )
        serializer = FarmerSerializer(farmers, many=True)
        return Response(serializer.data)




class FarmerSummaryAPIView(ListAPIView):
    serializer_class = FarmerSummarySerializer

    def get_queryset(self):
        return (
            Farmer.objects
            .select_related("massive__district__region")  # 🔥 ҚЎШИЛДИ
            .annotate(
                quantity=Coalesce(
                    Sum("contracts__planned_quantity"),
                    Decimal("0.00")
                ),
                amount=Coalesce(
                    Sum("contracts__total_amount"),
                    Decimal("0.00")
                ),
            )
            .order_by("massive__district__id", "massive__id")
        )





class BotUserCheckAPIView(APIView):

    def post(self, request):
        telegram_id = request.data.get("telegram_id")
        full_name = request.data.get("full_name")

        user, created = BotUser.objects.get_or_create(
            telegram_id=telegram_id,
            defaults={
                "full_name": full_name,
                "is_active": False,
            }
        )

        return Response({
            "allowed": user.is_active,
            "created": created
        })
