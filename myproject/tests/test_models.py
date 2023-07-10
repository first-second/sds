import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from main.models import Registration

User = get_user_model()

@pytest.mark.django_db
def test_create_user():
    username = 'testuser'
    email = 'test@example.com'
    password = 'testpassword'
    address = 'Test Address'
    phone = '1234567890'
    
    user = Registration.objects.create_user(username=username, email_address=email, password=password, address=address, phone=phone)
    
    assert user.username == username
    assert user.email_address == email
    assert user.check_password(password)
    assert user.address == address
    assert user.phone == phone
    assert user.is_staff == False
    assert user.is_superuser == False
    assert user.is_active == True

@pytest.mark.django_db
def test_create_superuser():
    username = 'adminuser'
    email = 'admin@example.com'
    password = 'adminpassword'
    address = 'Admin Address'
    phone = '9876543210'
    
    superuser = Registration.objects.create_superuser(username=username, email_address=email, password=password, address=address, phone=phone)
    
    assert superuser.username == username
    assert superuser.email_address == email
    assert superuser.check_password(password)
    assert superuser.address == address
    assert superuser.phone == phone
    assert superuser.is_staff == True
    assert superuser.is_superuser == True
    assert superuser.is_active == True

@pytest.mark.django_db
def test_photo_upload():
    username = 'testuser'
    email = 'test@example.com'
    password = 'testpassword'
    address = 'Test Address'
    phone = '1234567890'
    
    photo_file = SimpleUploadedFile('test_photo.jpg', b'myphotocontent', content_type='image/jpeg')
    
    user = Registration.objects.create_user(username=username, email_address=email, password=password, address=address, phone=phone, photo=photo_file)
    
    assert user.photo.url.endswith('test_photo.jpg')


