from django.contrib import admin
from django.urls import path
from . import views

app_name = 'payment'
urlpatterns = [
    path('homepage/', views.homepage, name='homepage'),
    path('paymenthandler/', views.paymenthandler, name='paymenthandler'),
    path('admin/', admin.site.urls),
]