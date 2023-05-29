from django.contrib import admin

# Register your models here.
from .models import Category, Product  #buradaki directory de olduğu için from . diyoruz.


@admin.register(Category) # prepopulated field. Daha önce oluşturulmuşsa belli kısmı oto gelir.
class CategoryAdmin(admin.ModelAdmin):

    prepopulated_fields = {'slug': ('name',)} # isim yazıldığında oto slug da aynı olacak

@admin.register(Product) 
class ProductAdmin(admin.ModelAdmin):

    prepopulated_fields = {'slug': ('title',)}










