from rest_framework import serializers
from query.models.counterparties import Farmer


class FarmerSerializer(serializers.ModelSerializer):
    balance = serializers.DecimalField(
        max_digits=18,
        decimal_places=2,
        read_only=True
    )

    class Meta:
        model = Farmer
        fields = (
            "id",
            "name",
            "inn",
            "phone",
            "balance",
        )


class FarmerSummarySerializer(serializers.ModelSerializer):

    quantity = serializers.DecimalField(
        max_digits=20,
        decimal_places=2
    )

    amount = serializers.DecimalField(
        max_digits=20,
        decimal_places=2
    )

    region = serializers.SerializerMethodField()
    district = serializers.SerializerMethodField()
    massive = serializers.SerializerMethodField()

    class Meta:
        model = Farmer
        fields = (
            "id",
            "name",
            "inn",
            "region",
            "district",
            "massive",
            "quantity",
            "amount",
        )

    # 🔹 Massive бўш бўлса хатолик чиқмаслиги учун
    def get_region(self, obj):
        try:
            return obj.massive.district.region.name
        except:
            return None

    def get_district(self, obj):
        try:
            return obj.massive.district.name
        except:
            return None

    def get_massive(self, obj):
        try:
            return obj.massive.name
        except:
            return None