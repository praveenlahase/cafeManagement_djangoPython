from os import path

from django.conf import settings
from django.conf.urls.static import static

from cafeapp import views


from django.urls import path

from django.contrib import admin

urlpatterns=[
    path('', views.index, name='index'),
    path('about/', views.about),
    path('login/', views.ulogin),
    path('logout/', views.ulogout),
    path('registration', views.uregistration),
    path('bookTable', views.bookTable, name='book_table'),
    path('products/', views.products, name='products'),
    path('product/<int:id>/', views.product_details, name='product_details'),
    
    path('makepayment/', views.make_payment, name='make_payment'),
    
    path('process-payment/', views.execute_payment, name='execute_payment'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('payment-failed/', views.payment_failed, name='payment_cancel'),
    # path('paypal/order/create/', paypal_order_create, name='paypal_order_create'),
    path('paypal/execute/', views.execute_payment, name='paypal_execute_payment'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)