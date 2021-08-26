from django.test import TestCase

from api_service.models import Customer, Deal
from api_service.serializers import DealsSerializer, CustomersSerializer


class DealsSerializerTest(TestCase):

    def test_customer_max_length(self):
        serializer = DealsSerializer()
        self.assertEqual(serializer.fields['customer'].max_length, 300)

    def test_item_max_length(self):
        serializer = DealsSerializer()
        self.assertEqual(serializer.fields['item'].max_length, 300)


class CustomerSerializerTest(TestCase):
    items_list = ['opal', 'opal', 'amber', 'amber', 'nefrit', 'nefrit', 'daymond', 'sapfir']
    true_items_result = set(items_list)

    def setUp(self) -> None:
        customer = Customer.objects.create(username='test_username')
        for gem in CustomerSerializerTest.items_list:
            Deal.objects.create(customer=customer, item=gem, total=100.0, quantity=1, date='2021-01-31 12:10:55',
                                transaction_number='1629714491.0902317')

    def test_get_gems(self):
        customer = Customer.objects.get(id=1)
        serializer = CustomersSerializer()
        result = serializer.get_gems(customer)
        self.assertEqual(result, CustomerSerializerTest.true_items_result)
