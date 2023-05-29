
from .cart import Cart # .cart demek cart.py içerisine ulaş Cart classını kullan


# sayesinde cart içerisinedeki def lere template içinde direk ulaşabiliyoruz.
def cart(request):

    return {'cart': Cart(request)}















