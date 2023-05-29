from decimal import Decimal
from store.models import Product



# Cart özelliklerini burada yaratıyoruz.(session oturum demek. Cookie olarak bunu tutucaz)
class Cart():

    # Eğer ilk defa sitemize giriyorsa oturum aç, daha önce ziyaret etmişse devam
    def __init__(self, request):
        
        self.session = request.session
        cart = self.session.get('session_key') # Daha önce girmişse oturumu al

        if 'session_key' not in request.session: # Yeni kullanıcı için oturumun yarat

            cart = self.session['session_key'] = {} # session kontrolü yapılarak çalışıp çalışmadığına bakarız. 

        # cartı buraya atarak sayfanın her yerinde bir şey varsa görmesi sağlanacak
        self.cart = cart


    def add(self, product, product_qty):

        product_id = str(product.id)

        if product_id in self.cart:
            
            self.cart[product_id]['qty'] = product_qty  #eğer sepette ürün varsa sadece qty ile ilglenmek için

        else:

            self.cart[product_id] = {'price': str(product.price), 'qty': product_qty} # product-info da document.getElementById("cart-qty").textContent = json.qty sonda kullanıyoruz key'i


        self.session.modified = True


    def delete(self, product):

        product_id = str(product)

        if product_id in self.cart:

            del self.cart[product_id]

        self.session.modified = True


    def update(self,product,qty):

        product_id = str(product)
        product_quantity = qty

        if product_id in self.cart:   # istediğim ürün sepettemi ?

            self.cart[product_id]['qty'] = product_quantity  # istediğim ürünün sadece adedini istiyorum, onuda girilen adede eşitleyerek güncelliyoruz.

        self.session.modified = True




    # cart içerisinde sayfayı korumak için bunu ekledik. (base.html --> <div id="cart-qty" class="d-inline-flex">)
    def __len__(self):

        return sum(item['qty'] for item in self.cart.values())



    # sepete giren ürünlerin üzerinde gezmek için.
    def __iter__(self):

        all_product_ids = self.cart.keys()

        products = Product.objects.filter(id__in=all_product_ids)

        import copy

        cart = copy.deepcopy(self.cart)
        #cart = self.cart.copy()  # deep copy yapacağımız için iptal

        for product in products:

            cart[str(product.id)]['product'] = product


        for item in cart.values():

            item['price'] = Decimal(item['price'])    # str yi ondalığa çevirdi

            item['total'] = item['price'] * item['qty'] # toplam ürün fiyatı

            yield item # return total cost



    def get_total(self):

        return sum(Decimal(item['price'])*item['qty'] for item in self.cart.values())



