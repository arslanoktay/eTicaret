from django.shortcuts import render
from .models import Category, Product
from django.shortcuts import get_object_or_404
# Create your views here.

def store(request):

    all_products = Product.objects.all()

    context = {"all_products":all_products} # html döngü buradaki key'e göre kuruluyor.

    return render(request, 'store/store.html', context) # templates/store kısmından 1.store geliyor. Değişirse değişmeli


def categories(request):

    all_categories = Category.objects.all() # tüm kategorileri seçtik

    return {'all_categories': all_categories}


def list_category(request, category_slug=None):

    category = get_object_or_404(Category, slug=category_slug)

    products = Product.objects.filter(category=category)

    return render(request, 'store/list-category.html', {'category':category, 'products':products})


# slug ı alıp bu requesti çağıracak. product nesnesindeki productdaki tabloda slug var mı bakacak.Varsa context ve return ile döndürecek.
def product_info(request, product_slug):

    product = get_object_or_404(Product, slug=product_slug)

    context = {'product': product}

    return render(request, 'store/product-info.html', context)
