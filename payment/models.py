from django.db import models
from django.contrib.auth.models import User
# Create your models here.

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
   



