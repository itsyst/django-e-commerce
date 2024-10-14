from store.models import Product
from store.admin import ProductAdmin
from tags.models import TaggedItem
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline


class TagInline(GenericTabularInline):
    autocomplete_fields = ['tag']
    min_num = 1
    extra = 0
    model = TaggedItem


class CustomProductAdmin(ProductAdmin):
    inlines = [TagInline]


admin.site.unregister(Product)
admin.site.register(Product, CustomProductAdmin)
