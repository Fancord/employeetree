from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Employee
from mptt.admin import MPTTModelAdmin


def linkify(field_name):
    """
    Превращает значение "foreign key" в ссылку на изменение объекта с которым он связан
    """
    def _linkify(obj):
        linked_obj = getattr(obj, field_name)
        if linked_obj is None:
            return '-'
        app_label = linked_obj._meta.app_label
        model_name = linked_obj._meta.model_name
        view_name = f'admin:{app_label}_{model_name}_change'
        link_url = reverse(view_name, args=[linked_obj.pk])
        return format_html('<a href="{}">{}</a>', link_url, linked_obj)

    _linkify.short_description = field_name  # Sets column name
    return _linkify


class CustomMPTTModelAdmin(MPTTModelAdmin):
    fields = ('fio', 'salary_by_hour', 'salary_sum', 'firstday', 'position', 'boss', 'user')
    list_display_links = ('fio',)
    list_display = ('fio', 'position', linkify(field_name='boss'), 'salary_by_hour', 'salary_sum')
    list_filter = ('position', 'level')
    actions = ['delete_salary_sum', ]
    mptt_level_indent = 20

    def delete_salary_sum(self, request, queryset):
        """
                        Action
        Удаление информации об выплаченой зарплате
        """
        queryset.update(salary_sum=0)
        self.message_user(request, f"Data was updated")

    delete_salary_sum.short_description = "delete the info about 'sum salary paid'"
    delete_salary_sum.allowed_permisssion = ('change',)


admin.site.register(Employee, CustomMPTTModelAdmin)
