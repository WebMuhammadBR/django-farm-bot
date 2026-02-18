from decimal import Decimal

from django.db.models import Sum
from django.db.models.functions import Coalesce
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from query.models.bot import BotUser
from query.models.counterparties import Farmer
from query.models.documents import MineralWarehouseReceipt, GoodsGivenDocument, Warehouse
from .serializers import (
    FarmerSerializer,
    FarmerSummarySerializer,
    MineralWarehouseReceiptSerializer,
    GoodsGivenDocumentSummarySerializer,
    WarehouseSerializer,
)


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
            .select_related("massive__district__region")
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


class MineralWarehouseReceiptListAPIView(ListAPIView):
    serializer_class = MineralWarehouseReceiptSerializer

    def get_queryset(self):
        return MineralWarehouseReceipt.objects.select_related("warehouse", "product").order_by("-date", "-id")


class GoodsGivenDocumentListAPIView(ListAPIView):
    serializer_class = GoodsGivenDocumentSummarySerializer

    def get_queryset(self):
        return (
            GoodsGivenDocument.objects
            .select_related("warehouse", "farmer")
            .annotate(
                quantity=Coalesce(Sum("items__quantity"), Decimal("0.00")),
            )
            .order_by("-date", "-id")
        )


class WarehouseListAPIView(ListAPIView):
    serializer_class = WarehouseSerializer

    def get_queryset(self):
        return Warehouse.objects.all().order_by("name")


class MineralWarehouseTotalsAPIView(APIView):

    def get(self, request):
        total_in = MineralWarehouseReceipt.objects.aggregate(
            value=Coalesce(Sum("quantity"), Decimal("0.00")),
            amount=Coalesce(Sum("amount"), Decimal("0.00")),
        )

        total_out = GoodsGivenDocument.objects.aggregate(
            value=Coalesce(Sum("items__quantity"), Decimal("0.00")),
            amount=Coalesce(Sum("items__amount"), Decimal("0.00")),
        )

        balance = total_in["value"] - total_out["value"]
        balance_amount = total_in["amount"] - total_out["amount"]

        return Response(
            {
                "total_in": total_in["value"],
                "total_out": total_out["value"],
                "balance": balance,
                "total_in_amount": total_in["amount"],
                "total_out_amount": total_out["amount"],
                "balance_amount": balance_amount,
            }
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
