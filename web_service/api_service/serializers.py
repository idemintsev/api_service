from rest_framework import serializers


class DealsSerialaizer(serializers.Serializer):
    customer = serializers.CharField(max_length=300)
    item = serializers.CharField(max_length=300)
    total = serializers.FloatField()
    quantity = serializers.IntegerField()
    date = serializers.DateTimeField()


class CustomersSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=300)
    spent_money = serializers.FloatField()
    gems = serializers.ListField()


class FileUploadSerializer(serializers.Serializer):
    deals = serializers.FileField(use_url=True)
