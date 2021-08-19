import re
from decimal import Decimal
from time import time

from rest_framework.response import Response
from rest_framework.views import APIView

from api_service.models import Customer, Deal
from api_service.serializers import DealsSerialaizer, FileUploadSerializer

DATETIME_TEMPLATE = re.compile(
    r"([0-9]{4}\-[0][0-9]|[0-9]{4}\-[1][0-2]\-[0-3][0-9]\s[0-2][0-9]\:[0-5][0-9]\:[0-5][0-9])")


class DealsView(APIView):
    def get(self, request):
        deals = Deal.objects.all()
        serialaizer_data = DealsSerialaizer(deals, many=True).data
        return Response({'deals': serialaizer_data})

    def post(self, request):
        deals = request.data.get('deals')
        serialaizer = DealsSerialaizer(data=deals)
        if serialaizer.is_valid(raise_exception=True):
            if deals.get('item') == 'amber':
                return Response(
                    {'Status': 'Error, Desc: <Описание ошибки> - в процессе обработки файла произошла ошибка'})
            deal_saved = serialaizer.save()
        return Response({'Status': 'OK - файл был обработан без ошибок'})


class FileUploadView(APIView):
    def post(self, request):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            file = request.FILES['deals']
            result = self.file_handler(file)
            if result[0] is True:
                return Response(result[1], status=201)
            return Response(result[1], status=422)

    def file_handler(self, file):
        if file.name.endswith('.csv'):
            result = self.file_parser(file)
            if result is None:
                return True, {'Status': 'OK - файл был обработан без ошибок'}
            return False, {'Status': result}
        return False, {'Status': 'Error, Desc: Формат файла не CSV - в процессе обработки файла произошла ошибка'}

    def file_parser(self, file):
        file_chunks = file.chunks(chunk_size=None)
        transaction_number = str(time())
        for chunk in file_chunks:
            decoded_chunk = chunk.decode(encoding='utf-8')
            decoded_chunk = [row for row in decoded_chunk.split('\n') if row]
            for row in decoded_chunk:
                if 'customer,item,total,quantity,date' not in row:
                    validated_data = self.check_data(row)
                    print(validated_data)
                    if validated_data[0]:
                        self.save_data_into_bd(validated_data[1], transaction_number)
                    else:
                        return validated_data[1]

    def save_data_into_bd(self, data: tuple, transaction_number: str):
        customer_name, item, total, quantity, date_ = data
        customer = Customer.objects.get_or_create(name=customer_name)[0]
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
        - формат даты и времени;
        - можно ли перевести в float и int сумму сделки и количество камней.
        :param data: Строка, в которой через запятую перечисляются customer_name, item, total, quantity, date.
        :return: кортеж (False, str: <Описание ошибки>) или (True, (customer_name, item, total, quantity, date))
        """
        print(data)
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
