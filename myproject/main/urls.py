from django.urls import include, re_path
from . import views
#url setup for each page
urlpatterns = [
    re_path(r'^$', views.home, name='home'),
    re_path(r'^about/$',views.about, name='about'),
    re_path(r'^login/$',views.login, name='login'),
    re_path(r'^register/$',views.register, name='register'),
    re_path(r'^certificate/$',views.certificate, name='certificate'),
    re_path(r'^contact/$',views.contact,name='contact'),
    re_path(r'^data/$',views.dataView, name='data'),
    #re_path(r'^about/home/$',views.home,name='home'),
    re_path(r"checkout/", views.checkout, name="checkout"),
    re_path(r"handlerequest/", views.handlerequest, name="handlerequest"),
    ]
