from django.db import models
from django.urls import reverse # for dynamic urls(tuşa atamalar)

# Create your models here.
# App yarattık, modellerimi yaratmak için burayı kullanıcaz.

class Category(models.Model): # model yarattık.

    name = models.CharField(max_length=250, db_index=True) # Küçük string depolamak için charfield. db_index true ise hızlıca db ye bakabilmemizi sağlıyor.Direk isteneni bulabiliyor tüm tabloyu okumak zorunda kalmıyor.
    
    slug = models.SlugField(max_length=250, unique=True) # 1 den fazla category oluşturmamak için.(2 kere shirt olmaması mesela) Genelde URL için kullanılır.string sayı alt ve normal çizgi alır sadece
                                                         #unique özel karakterler için bulunuyor

    class Meta:

        verbose_name_plural = 'categories' #Admin paneli gibi yerlerde sonuna direk s ekleyecek Categorys olacak bu ing yanlış. O yüzden çoğul ismini tanımlıyoruz.

    # data olarak Category(1) olarak değilde --> Shirt olarak görücez örnek. İsmini kulanmasını sağlayacak
    def __str__(self):
        return self.name
    
    # base.html de category kısmında kullanıyoruz.
    def get_absolute_url(self):
         
         return reverse('list-category', args=[self.slug])




class Product(models.Model):

    #Category ve product bağlantısını sağlayacak. / on_delete bağlı olduğu category silinirse ürünler silinsin diye. / null olmasın diye 
    category = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE, null=True)


    title = models.CharField(max_length=250)

    brand = models.CharField(max_length=250, default='un-branded')

    description = models.TextField(blank=True) # Charfield dan daha uzun metinler için kullan.Daha fazla karakter içeriyor / Black ise bunun opsiyonel doldurulması gerektiği ile ilgili.

    slug = models.SlugField(max_length=255) # tüm ürünlerimiz uniq olacağı için

    price = models.DecimalField(max_digits=4, decimal_places=2) # Enfazla 4 hane ve virgülden sonra 2
    
    image = models.ImageField(upload_to = 'images/') # pillow kullanıyoruz. yüklediğimiz fotolar otomatik images folder ına yükleniyor.    


    class Meta:

            verbose_name_plural = 'products' #Admin paneli gibi yerlerde sonuna direk s ekleyecek Categorys olacak bu ing yanlış. O yüzden çoğul ismini tanımlıyoruz.


    # product(1) yada product(2) yerine ismi yazacak: Air Jordan gibi
    def __str__(self):
        return self.title


    # url ismi kullanılmalı. / store.html de title kısmınına bu def'i yazdık.
    def get_absolute_url(self):
         
         return reverse('product-info', args=[self.slug])

