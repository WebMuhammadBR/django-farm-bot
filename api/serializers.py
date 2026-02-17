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

    def get_region(self, obj):
        massive = obj.massive
        if massive and massive.district and massive.district.region:
            return massive.district.region.name
        return None

    def get_district(self, obj):
        massive = obj.massive
        if massive and massive.district:
            return massive.district.name
        return None

    def get_massive(self, obj):
        if obj.massive:
            return obj.massive.name
        return None
