from django.test import TestCase

from api_service.models import Customer, Deal


class CustomerModelTest(TestCase):

    def setUp(cls) -> None:
        Customer.objects.create(username='test_username')

    def test_username_label(self):
        customer = Customer.objects.get(id=1)
        field_label = customer._meta.get_field('username').verbose_name
        self.assertEquals(field_label, 'Логин клиента')

    def test_spent_money_label(self):
        customer = Customer.objects.get(id=1)
        field_label = customer._meta.get_field('spent_money').verbose_name
        self.assertEquals(field_label, 'Всего потрачено средств')

    def test_username_max_length(self):
        customer = Customer.objects.get(id=1)
        max_length = customer._meta.get_field('username').max_length
        self.assertEquals(max_length, 300)

    def test_spent_money_default(self):
        customer = Customer.objects.get(id=1)
        spent_money = customer._meta.get_field('spent_money').default
        self.assertEquals(spent_money, 0.0)

    def test_obj_str_is_username(self):
        customer = Customer.objects.get(id=1)
        expected_customer_str = customer.username
        self.assertEquals(expected_customer_str, str(customer))


class DealModelTest(TestCase):

    def setUp(cls) -> None:
        customer = Customer.objects.create(username='test_username')
        Deal.objects.create(customer=customer,
                            item='opal',
                            total=100.0,
                            quantity=1,
                            date='2021-01-31 12:10:55',
                            transaction_number='1629714491.0902317')

    def test_customer_label(self):
        deal = Deal.objects.get(id=1)
        field_label = deal._meta.get_field('customer').verbose_name
        self.assertEquals(field_label, 'Клиент')

    def test_item_label(self):
        deal = Deal.objects.get(id=1)
        field_label = deal._meta.get_field('item').verbose_name
        self.assertEquals(field_label, 'Наименование товара')

    def test_total_label(self):
        deal = Deal.objects.get(id=1)
        field_label = deal._meta.get_field('total').verbose_name
        self.assertEquals(field_label, 'Сумма сделки')

    def test_quantity_label(self):
        deal = Deal.objects.get(id=1)
        field_label = deal._meta.get_field('quantity').verbose_name
        self.assertEquals(field_label, 'Количество товара, шт')

    def test_date_label(self):
        deal = Deal.objects.get(id=1)
        field_label = deal._meta.get_field('date').verbose_name
        self.assertEquals(field_label, 'Дата и время сделки')

    def test_transaction_number_label(self):
        deal = Deal.objects.get(id=1)
        field_label = deal._meta.get_field('transaction_number').verbose_name
        self.assertEquals(field_label, 'Код транзакции')

    def test_deal_str_is_comb_date_username(self):
        customer = Customer.objects.get(id=1)
        deal = Deal.objects.get(id=1)
        expected_deal_str = f'{deal.date} {customer.username}'
        self.assertEquals(expected_deal_str, str(deal))

    def test_item_max_length(self):
        deal = Deal.objects.get(id=1)
        max_length = deal._meta.get_field('item').max_length
        self.assertEquals(max_length, 300)

    def test_transaction_number_max_length(self):
        deal = Deal.objects.get(id=1)
        max_length = deal._meta.get_field('transaction_number').max_length
        self.assertEquals(max_length, 30)
