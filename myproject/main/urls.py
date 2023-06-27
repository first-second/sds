from django.urls import include, re_path
from . import views
#url setup for each page
urlpatterns = [
    re_path(r'^$', views.home, name='home'),
    re_path(r'^about/$',views.about, name='about'),
    re_path(r'^login/$',views.LoginPage, name='login'),
    re_path(r'^register/$',views.register, name='register'),
    re_path(r'^certificate/$',views.certificate, name='certificate'),
    re_path(r'^contact/$',views.contact,name='contact'),
    re_path(r'^data/$',views.dataView, name='data'),
    #re_path(r'^about/home/$',views.home,name='home'),
    re_path(r"checkout/", views.checkout, name="checkout"),
    re_path(r"handlerequest/", views.handlerequest, name="handlerequest"),
    re_path(r"logout", views.logout_request, name= "logout"),
    #re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate_account, name='activate_account'),
    re_path(r'registration_success/', views.registration_success, name='registration_success'),
    #re_path('send-test-email/', views.send_test_email, name='send_test_email'),
    re_path('verify-otp/', views.verify_otp, name='verify_otp'),
    #re_path('activate/<str:uidb64>/<str:token>/', views.activate_account, name='activate_account'),
    ]
