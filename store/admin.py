from django.contrib import admin
from . import models


admin.site.register(models.Collection)


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'unit_price', 'inventory_status']
    list_editable = ['unit_price']
    list_per_page = 10
   # admin.site.register(models.Product, ProductAdmin)

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        return 'Ok'


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership']
    ordering = ['first_name', 'last_name']
    list_editable = ['membership']
    list_per_page = 10
