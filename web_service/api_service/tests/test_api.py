from django.test import TestCase
from unittest.mock import Mock
from io import BytesIO

from api_service.api import DealsView
from api_service.models import Deal


class DealsViewTest(TestCase):

    def test_token_authentication(self):
        pass

    def test_wright_file_format(self):
        pass

    def test_check_format_wrong_file(self):
        view = DealsView()
        file = Mock()
        file.name = 'deals.txt'
        self.assertFalse(view.check_format(file))

    def test_check_format_wright_file(self):
        view = DealsView()
        file = Mock()
        file.name = 'deals.csv'
        self.assertTrue(view.check_format(file))

    def test_check_data_not_enough_columns(self):
        view = DealsView()
        wrong_data = 'user1,daymond,10000.18,1'
        expected_return = (
            False,
            'Error, Desc: not enough values to unpack (expected at least 5, got 4) файл заполнен некорректно - '
            'в процессе обработки файла произошла ошибка')
        self.assertEqual(expected_return, view.check_data(wrong_data))

    def test_check_data_extra_columns(self):
        view = DealsView()
        wrong_data = 'user1,daymond,10000.18,1,2021-08-18 10:01:14,555'
        expected_return = (
            False, 'Error, Desc: файл содержит больше 5 столбцов - в процессе обработки файла произошла ошибка')
        self.assertEqual(expected_return, view.check_data(wrong_data))

    def test_check_data_total_not_digit(self):
        view = DealsView()
        wrong_data = 'user1,daymond,string,1,2021-08-18 10:01:14'
        expected_return = (
            False, "Error, Desc: could not convert string to float: 'string' информация о стоимости или количестве "
                   "камней некорректна - в процессе обработки файла произошла ошибка")
        self.assertEqual(expected_return, view.check_data(wrong_data))

    def test_check_data_quantity_not_digit(self):
        view = DealsView()
        wrong_data = 'user1,daymond,10000.0,string,2021-08-18 10:01:14'
        expected_return = (
            False, "Error, Desc: invalid literal for int() with base 10: 'string' информация о стоимости или "
                   "количестве камней некорректна - в процессе обработки файла произошла ошибка")
        self.assertEqual(expected_return, view.check_data(wrong_data))

    def test_check_data_wrong_date_format(self):
        view = DealsView()
        wrong_data = 'user1,daymond,10000.0,1,31-12-2021 10:01:14'
        expected_return = (
            False, "Error, Desc: Дата 31-12-2021 10:01:14 не соответствует формату YYYY-MM-DD HH:MM:SS"
                   " - в процессе обработки файла произошла ошибка")
        self.assertEqual(expected_return, view.check_data(wrong_data))

    def test_check_data_wrong_time_format(self):
        view = DealsView()
        wrong_data = 'user1,daymond,10000.0,1,31-12-2021 10.01.14'
        expected_return = (
            False, "Error, Desc: Дата 31-12-2021 10.01.14 не соответствует формату YYYY-MM-DD HH:MM:SS"
                   " - в процессе обработки файла произошла ошибка")
        self.assertEqual(expected_return, view.check_data(wrong_data))

    def test_check_data_wright_data(self):
        view = DealsView()
        wright_data = 'user1,daymond,10000.18,1,2021-08-18 10:01:14'
        expected_return = (
            True, ('user1', 'daymond', 10000.18, 1, '2021-08-18 10:01:14.000000+00:00'))
        self.assertEqual(expected_return, view.check_data(wright_data))

    def test_message_if_wrong_file_format(self):
        view = DealsView()
        file = Mock()
        file.name = 'deals.txt'
        expected_result = (
            False,
            {'Status': 'Error, Desc: Формат файла не CSV - в процессе обработки файла произошла ошибка'})
        self.assertEqual(expected_result, view.file_handler(file=file))

    def test_save_data_reduce_spent_money(self):
        view = DealsView()
        data = ('test_user1630050461', 'daymond', 10000.18, 1, '2021-08-18 10:01:14.000000+00:00',)
        transaction_number = '1630050461.490916'
        view.save_data_into_bd(data=data, transaction_number=transaction_number)
        result = Deal.objects.select_related('customer').get(transaction_number='1630050461.490916')
        self.assertEqual(10000.18, result.customer.spent_money)

    def test_save_data_save_to_db(self):
        view = DealsView()
        data = ('test_user1630050461', 'daymond', 10000.18, 1, '2021-08-18 10:01:14.000000+00:00',)
        transaction_number = '1630050461.490916'
        view.save_data_into_bd(data=data, transaction_number=transaction_number)
        expected_result = ['<Deal: 2021-08-18 10:01:14+00:00 test_user1630050461>', ]
        result = Deal.objects.filter(id=1)
        self.assertQuerysetEqual(result, expected_result)
