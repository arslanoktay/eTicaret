from django.db import models
from django.contrib.auth.models import User  # Birşeye FK ekleyeceksek import edilmeli
# Create your models here.
from store.models import Product




class ShippingAdress(models.Model):

    full_name = models.CharField(max_length=300)

    email = models.EmailField(max_length=255)

    address1 = models.CharField(max_length=300)

    address2 = models.CharField(max_length=300)

    city = models.CharField(max_length=255)


    # Optional
    state = models.CharField(max_length=255, null=True, blank=True) # Her ülkede yok boş geçebilsin / null db için belirtiyoruz blank ise client için

    zipcode = models.CharField(max_length=255, null=True, blank=True)


    # FK --> foreign key / müşterilerin tek bir adresi olması için

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) # shipping i mecbur bırakmıyoruz / authenticated ve non authenticated(kimliği doğrulanmamış) -- bir shpiing yaratıldığında admin panelinde hangi üyeye bağlı görüyoruz


    class META:

        verbose_name_plural = 'Shipping Adress'



    def __str__(self):

        return 'Shipping Adress - ' + str(self.id)
   

# geçilen sipariş modeli
class Order(models.Model):

    full_name = models.CharField(max_length=300)

    email = models.EmailField(max_length=255)

    shipping_address = models.TextField(max_length=1000)

    amount_paid = models.DecimalField(max_digits=8, decimal_places=2) # max digit virgül sonrası ve tamsayı toplamı demek

    date_ordered = models.DateTimeField(auto_now_add=True)


    #FK
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
    
        return 'Order - #' + str(self.id)
    

class OrderItem(models.Model):

    # FK ->
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True) # İtemlar Order'a bağlı olmalı

    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True)



    quantity = models.PositiveBigIntegerField(default=1)

    price = models.DecimalField(max_digits=8,decimal_places=2)



    #FK
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) # null True olmazsa guest kullanamaz hata verir / CASCADE -> eğer order giderse itemler silinsin.


    def __str__(self):
    
        return 'Order İtem - #' + str(self.id)
