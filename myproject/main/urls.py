from django.urls import include, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    re_path(r'^$', views.home, name='home'),
    re_path(r'^about/$', views.about, name='about'),
    re_path(r'^login/$', views.login_page, name='login'),
    re_path(r'^register/$', views.register, name='register'),
    re_path(r'^certificate/$', views.certificate, name='certificate'),
    re_path(r'^contact/$', views.contact, name='contact'),
    re_path(r'^data/$', views.data_view, name='data'),
    re_path(r"logout", views.logout_request, name="logout"),
    re_path(r'registration_success/', views.registration_success, name='registration_success'),
    re_path('verify-otp/', views.verify_otp, name='verify_otp'),
    re_path(r"user_dashboard/", views.user_dashboard, name="user_dashboard"),
    re_path('', include('payment.urls', namespace='payment')),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
