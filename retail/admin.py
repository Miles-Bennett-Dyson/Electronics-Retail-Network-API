from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from retail.models import Retail, Product


@admin.register(Retail)
class RetailAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'email',
        'country',
        'city',
        'supplier_link',
        'debt',
        'created_at',
        'get_level')

    @admin.action(description="Обнуление задолженности")
    def debt_reset(self, request, queryset):
        updated_count = queryset.update(debt=0.00)
        self.message_user(request, f"Задолженность обнулена для {updated_count} объектов.")

    def supplier_link(self, obj): # pragma: no cover
        if not obj.supplier:
            return "-"
        url = reverse('admin:retail_retail_change', args=[obj.supplier.pk])
        return format_html('<a href="{}"target="_blank">{}</a>', url, obj.supplier.name)

    supplier_link.short_description = "Поставщик"

    list_filter = ('city',)
    actions = [debt_reset]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin): # pragma: no cover
    list_display = (
        'name',
        'model',
        'release_date',
    )
