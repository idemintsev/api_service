import logging

from rest_framework import serializers

from api_service.models import Customer, Deal

logging.basicConfig(level=logging.INFO)


class DealsSerializer(serializers.Serializer):
    customer = serializers.CharField(max_length=300)
    item = serializers.CharField(max_length=300)
    total = serializers.FloatField()
    quantity = serializers.IntegerField()
    date = serializers.DateTimeField()


class CustomersSerializer(serializers.ModelSerializer):
    gems = serializers.SerializerMethodField('get_gems')

    class Meta:
        model = Customer
        fields = ('username', 'spent_money', 'gems')
        depth = 1

    def get_gems(self, obj) -> set:
        """
        Возвращает множество из купленных камней для каждого пользователя.
        """
        logging.debug(f' obj - {obj}')
        deals_queryset = Deal.objects.select_related('customer').filter(customer=obj)
        logging.debug(f' deals_queryset - {deals_queryset}')
        gems = set([deal.item for deal in deals_queryset])
        logging.debug(f' gems - {gems}')
        return gems


class FileUploadSerializer(serializers.Serializer):
    deals = serializers.FileField(use_url=False)
