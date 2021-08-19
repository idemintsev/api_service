from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=300, verbose_name='Логин клиента')
    spent_money = models.FloatField(default=0.0, verbose_name='Всего потрачено средств')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'customers'
        ordering = ['name']
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Deal(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='Клиент', related_name='deals')
    item = models.CharField(max_length=300, verbose_name='Наименование товара')
    total = models.FloatField(verbose_name='Сумма сделки')
    quantity = models.IntegerField(verbose_name='Количество товара, шт')
    date = models.DateTimeField(verbose_name='Дата и время сделки')
    # transaction_number - уникальный номер, который генерируется при обработке каждого CSV-файла.
    transaction_number = models.CharField(max_length=30, verbose_name='Код транзакции')

    def __str__(self):
        return f'{self.date} {self.customer}'

    class Meta:
        db_table = 'deals'
        ordering = ['-date']
        verbose_name = 'Сделка'
        verbose_name_plural = 'Сделки'
