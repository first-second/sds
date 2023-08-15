from django.urls import re_path
from . import views

app_name = 'payment'
urlpatterns = [
    re_path(r'^home/', views.home, name="home"),
    re_path(r'^payment/', views.order_payment, name="payment"),
    re_path(r'^callback/', views.callback, name="callback"),
    # Other payment app URLs
]