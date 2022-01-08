from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from mptt.models import MPTTModel, TreeForeignKey


class Employee(MPTTModel):
    """Базовый класс сотрудника"""
    fio = models.CharField(max_length=100, unique=True, verbose_name='ФИО')
    position = models.CharField(blank=True, max_length=100, verbose_name='Должность')
    salary_by_hour = models.FloatField(blank=True, default=0, verbose_name='Зарплата за час')
    salary_sum = models.FloatField(blank=True, default=0, verbose_name='Всего выплачено')
    firstday = models.DateField(default=timezone.now, verbose_name='Дата приема на работу')
    level = models.IntegerField(blank=True, verbose_name='Уровень')
    boss = TreeForeignKey('self',
                          on_delete=models.CASCADE,
                          null=True, blank=True,
                          related_name='children',
                          verbose_name='Начальник')
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True)

    def __str__(self):
        return self.fio

    def recount_salary(self):
        """Начислени зарплаты каждые 2 часа"""
        self.selary_sum += self.salary_by_hour * 2
        super(Employee, self).save()

    class MPTTMeta:
        parent_attr = 'boss'
        order_insertion_by = ['fio']

    def save(self, *args, **kwargs):
        """Для сохранения уровня в иерархии"""
        self.level = self.get_level()
        super(Employee, self).save(*args, **kwargs)
