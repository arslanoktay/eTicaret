from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    # Admin url
    path('admin/', admin.site.urls),


    # Store app
    path('', include('store.urls')), # diğer url.py ları çekebilmek için include gerekiyor.


    # Cart app
    path('cart/', include('cart.urls')), # bir üstteki boş olduğu için cart/ yazmak zorundayız.

    # Account app
    path('account/', include('account.urls')),

    # Payment app
    path('payment/', include('payment.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




