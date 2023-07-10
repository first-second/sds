from django.test import RequestFactory
from django.contrib.auth.models import User
from main.views import home, about, contact, register, verify_otp, UserDashboard, LoginPage, logout_request
import pytest


@pytest.fixture
def factory():
    return RequestFactory()


@pytest.fixture
def authenticated_user(factory):
    user = Registration.objects.create_user(username='testuser', password='testpassword')
    request = factory.post('/login/')
    request.user = user
    return request


@pytest.fixture
def unauthenticated_user(factory):
    request = factory.post('/login/')
    request.user = AnonymousUser()
    return request


def test_home_view(factory):
    request = factory.get('/')
    response = home(request)
    assert response.status_code == 200
    assert 'ip' in response.context


def test_about_view(factory):
    request = factory.get('/about/')
    response = about(request)
    assert response.status_code == 200
    assert 'ip' in response.context


def test_contact_view(factory):
    request = factory.get('/contact/')
    response = contact(request)
    assert response.status_code == 200


def test_register_view(factory):
    request = factory.get('/register/')
    response = register(request)
    assert response.status_code == 200
    assert 'form' in response.context


def test_verify_otp_view(factory):
    request = factory.get('/verify-otp/')
    response = verify_otp(request)
    assert response.status_code == 200


def test_user_dashboard_view(authenticated_user):
    response = UserDashboard(authenticated_user)
    assert response.status_code == 200


def test_login_view(factory):
    request = factory.get('/login/')
    response = LoginPage(request)
    assert response.status_code == 200
    assert 'login_form' in response.context


def test_logout_request_view(factory):
    request = factory.get('/logout/')
    response = logout_request(request)
    assert response.status_code == 200

