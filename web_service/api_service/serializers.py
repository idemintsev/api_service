from rest_framework import serializers
from api_service.models import Deal, Customer


class DealsSerialaizer(serializers.Serializer):
    customer = serializers.CharField(max_length=300)
    item = serializers.CharField(max_length=300)
    total = serializers.FloatField()
    quantity = serializers.IntegerField()
    date = serializers.DateTimeField()

    def create(self, validated_data):
        data = self.data_handler(validated_data)
        return Deal.objects.create(**data)

    def data_handler(self, validated_data: dict) -> dict:
        """
        Заменяет значение ключа 'customer' в validated_data с username на ID этого пользователя.
        """
        username = validated_data.get('customer')
        customer_id = self.get_customer_id_or_create(username)
        validated_data.update(customer=customer_id)
        return validated_data

    def get_customer_id_or_create(self, username: str) -> int:
        """
        Ищет клиента в БД по username данного клиента. Если клиента нет - создает его.
        Возвращает ID клиента.
        """
        result = Customer.objects.get_or_create(name=username)
        customer_id = result[0]
        return customer_id


class FileUploadSerializer(serializers.Serializer):
    deals = serializers.FileField(use_url=True)
