from django.contrib import admin
from .models import Category, Product


# 🔹 Category
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


#  Product
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'stock', 'available')
    search_fields = ('name',)
    list_filter = ('category', 'available')