import re
from decimal import Decimal
from time import time

from django.contrib.auth import authenticate, login
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from api_service.models import Customer, Deal
from api_service.serializers import FileUploadSerializer, CustomersSerializer

#  Формат даты 2021-01-31
DATETIME_TEMPLATE = re.compile(
    r"([0-9]{4}\-[0][0-9]|[0-9]{4}\-[1][0-2]\-[0-3][0-9]\s[0-2][0-9]\:[0-5][0-9]\:[0-5][0-9])")


class DealsView(APIView):
    """
    API для обработки пересылаемого CSV-файла и отображения последних обработанных данных.
    """
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request):
        data_for_response = Customer.objects.prefetch_related('deals').order_by('-spent_money')[:5]
        serializer = CustomersSerializer(data_for_response, many=True).data
        return Response({'response': serializer})

    def post(self, request):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            file = request.FILES['deals']
            result = self.file_handler(file)
            if result[0] is True:
                return Response(result[1], status=201)
            return Response(result[1], status=422)

    def file_handler(self, file) -> tuple:
        """
        Проверяет формат файла, запускает процесс парсинга файла - self.file_parser().
        :param file: Пересылаемый CSV-файл для обработки.
        :return: Если файл обработан успешно - возвращает кортеж (True, dict), в случае ошибки возвращает кортеж
        (False, dict), в dict содержится описание ошибки.
        """
        if file.name.endswith('.csv'):
            result = self.file_parser(file)
            if result is None:
                return True, {'Status': 'OK - файл был обработан без ошибок'}
            return False, {'Status': result}
        return False, {'Status': 'Error, Desc: Формат файла не CSV - в процессе обработки файла произошла ошибка'}

    def file_parser(self, file):
        """
        Построчно парсит CSV-файл с помощью генератора chunks().
        Если проверка данных в строке методом self.check_data возвращает False, прерывает обработку и возвращает
        описание возникшей ошибки.
        :param file: Пересылаемый CSV-файл для обработки.
        :return: None или строку с описанием возникшей ошибки.
        """
        file_chunks = file.chunks(chunk_size=None)
        transaction_number = str(time())
        for chunk in file_chunks:
            decoded_chunk = chunk.decode(encoding='utf-8')
            decoded_chunk = [row for row in decoded_chunk.split('\n') if row]
            for row in decoded_chunk:
                if 'customer,item,total,quantity,date' not in row:
                    validated_data = self.check_data(row)
                    if validated_data[0]:
                        self.save_data_into_bd(validated_data[1], transaction_number)
                    else:
                        return validated_data[1]

    def save_data_into_bd(self, data: tuple, transaction_number: str) -> None:
        """
        Сохраняет данные из файла в БД.
        :param data: Кортеж (str: customer_name, str: item, float: total, int: quantity, str: date)
        :param transaction_number: строка с уникальным номером транзакции, в которой обрабатывается CSV-файл
        :return: None
        """
        customer_name, item, total, quantity, date_ = data
        customer = Customer.objects.get_or_create(username=customer_name)[0]
        Deal.objects.create(
            customer=customer,
            item=item,
            total=float(total),
            quantity=int(quantity),
            date=date_,
            transaction_number=transaction_number
        )
        customer.spent_money = float(
            Decimal(customer.spent_money).quantize(Decimal('1.00')) + Decimal(total).quantize(Decimal('1.00')))
        customer.save()

    def check_data(self, data: str) -> tuple:
        """
        Проверяет данные из файла:
        - все ли пять столбцов заполнены;
        - соответствует ли формат даты и времени шаблону DATETIME_TEMPLATE;
        - можно ли привести к float сумму сделки и к int количество камней.
        :param data: Строка, в которой через запятую перечисляются customer_name, item, total, quantity, date.
        :return: кортеж (False, str: <Описание ошибки>) или
        (True, tuple: (str: customer_name, str: item, float: total, int: quantity, str: date))
        """
        try:
            customer_name, item, total, quantity, date_ = data.split(',')
        except ValueError as exc:
            return False, f'Error, Desc: {exc} файл заполнен некорректно - в процессе обработки файла произошла ошибка'

        try:
            total = float(total)
            quantity = int(quantity)
        except ValueError as exc:
            return False, f'Error, Desc: {exc} информация о стоимости или количестве камней некорректна - ' \
                          f'в процессе обработки файла произошла ошибка'

        date_match = re.match(DATETIME_TEMPLATE, date_)
        try:
            if not date_match:
                raise ValueError(f'Error, Desc: Дата {date_} не соответствует формату YYYY-MM-DD HH:MM:SS - '
                                 f'в процессе обработки файла произошла ошибка')
        except ValueError as exc:
            return False, str(exc)

        return True, (customer_name, item, total, quantity, date_)


class LoginView(APIView):
    def post(self, request, format=None):
        data = request.data

        username = data.get('username', None)
        password = data.get('password', None)

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return Response({'response': f'Вы вошли как {request.user}'}, status=200)
            else:
                return Response(status=404)
        else:
            return Response(status=404)


class Logout(APIView):
    def get(self, request, format=None):
        request.user.auth_token.delete()
        return Response({'response': 'Выход выполнен успешно'}, status=200)
