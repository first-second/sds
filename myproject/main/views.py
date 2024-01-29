import matplotlib
from .models import Registration
from .forms import RegistrationForm
import pandas as pd
from sqlalchemy import create_engine
from .serializers import RegistrationSerializer
from rest_framework.response import Response
from django.db.models import Q
from datetime import date, timedelta
from rest_framework import status
from rest_framework.decorators import api_view
from django.contrib.auth import login, logout
from django.contrib import messages
from .auth_backends import RegistrationBackend
from django.contrib.auth.forms import AuthenticationForm
import plotly.graph_objects as go
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.utils.crypto import get_random_string
from django.core.files.storage import default_storage
import os
import shutil
from django.conf import settings
from django.views.decorators.csrf import csrf_protect


matplotlib.use('Agg')
MERCHANT_KEY = 'dP64425807474247'

engine = create_engine(
    'sqlite:///db.sqlite3',
    )


#db_connection = sql.connect(host='localhost', database='sds_db', user='adarsh', password='Dbpass@1')

#db_cursor = db_connection.cursor()

# [model -> view]Create your views here.what needs to be shown in webpage

'''def count_rows():
    #query=pd.read_sql('select * from main_registration',con=engine)
    #df=pd.DataFrame(query)
    #total = df['id'].count()
    total=Registration.objects.all().count()
    return total'''


def home(request):
    #sitename = 'SHARMA DRIVING SCHOOL'
    #registerdata = Registration.objects.raw('select id,address from main_registration')
    #data = {
    #    'registerdata':registerdata
    #}
    ip = os.environ.get('EC2_INSTANCE_IP')
     
    return render(request, 'front/home.html', {'ip': ip})


def about(request):
    ip = os.environ.get('EC2_INSTANCE_IP')
    return render(request, 'front/about.html', {'ip': ip})


def contact(request):

    return render(request, 'front/contact.html')


@csrf_protect
def register(request):
    form = RegistrationForm(request.POST or None, request.FILES or None)
    ip = os.environ.get('EC2_INSTANCE_IP')
    print(ip)
    if request.method == "POST":
        if form.is_valid():
            email = form.cleaned_data.get('email_address')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            address = form.cleaned_data.get('address')
            phone = form.cleaned_data.get('phone')
            photo = form.cleaned_data.get('photo')  # Get the uploaded photo from the form
            if photo:
                # Save the photo to the temporary location
                photo_name = f'temp/{username}_photo.jpg'
                photo_path = default_storage.save(photo_name, photo)

                request.session['registration_photo_path'] = photo_path

            otp = get_random_string(length=6, allowed_chars='0123456789')
            request.session['registration_otp'] = otp
            request.session['registration_email'] = email
            request.session['registration_username'] = username
            request.session['registration_password'] = password
            request.session['registration_address'] = address
            request.session['registration_phone'] = phone

            # Send OTP via email
            mail_subject = 'Registration OTP'
            message = f"Your OTP for registration is: {otp}"
            email = EmailMessage(mail_subject, message, to=[email])
            email.send()

            # Redirect to OTP verification page
            return redirect('verify_otp')

    return render(request, 'front/register.html', {'form': form, 'ip': ip})


@csrf_protect
def verify_otp(request):
    if request.method == "POST":
        entered_otp = request.POST.get('otp')
        expected_otp = request.session.get('registration_otp')
        email = request.session.get('registration_email')
        username = request.session.get('registration_username')
        password = request.session.get('registration_password')
        address = request.session.get('registration_address')
        phone = request.session.get('registration_phone')
        #photo = request.session.get('registration_photo')

        if entered_otp == expected_otp:
            # Perform necessary actions after successful OTP verification
            # For example, create the user in the database
            user = Registration.objects.create_user(username=username, email_address=email, password=password,
                                                    address=address, phone=phone)
            photo_path = request.session.get('registration_photo_path')
            if photo_path:
                temp_photo_path = os.path.join(settings.MEDIA_ROOT, photo_path)
                new_photo_path = os.path.join(settings.MEDIA_ROOT, 'photos', f'{username}_photo.jpg')

                # Ensure the 'photos' directory exists
                os.makedirs(os.path.join(settings.MEDIA_ROOT, 'photos'), exist_ok=True)

                shutil.move(temp_photo_path, new_photo_path)

                # Update the user's photo field
                user.photo = f'photos/{username}_photo.jpg'
                user.save()
            # Send success registration email
            mail_subject = 'Registration Successful'
            message = render_to_string('front/account_activation_email.html', {
                'user': user,
            })
            email = EmailMessage(mail_subject, message, to=[email])
            email.send()

            # Clear the temporary data from the session
            del request.session['registration_otp']
            del request.session['registration_email']
            del request.session['registration_username']
            del request.session['registration_password']
            del request.session['registration_address']
            del request.session['registration_phone']

            return redirect('registration_success')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')

    return render(request, 'front/verify_otp.html')

    
def registration_success(request):
    return render(request, 'front/registration_success.html')


def certificate(request):
    ip = os.environ.get('EC2_INSTANCE_IP')
    ref = date.today()-timedelta(days=15)
    if request.method == 'GET':
        query = request.GET.get('q')

        submitbutton = request.GET.get('submit')
        
        if query is not None:
            #lookups= Q(name__icontains=query) | Q(address__icontains=query)
            lookups = Q(date__icontains=query)
            results = Registration.objects.filter(lookups).distinct()

            context = {'results': results, 'submitbutton': submitbutton}
            #print("ref",ref)
            return render(request, 'front/certificate.html', context)

        else:
            new_date = {"ref": str(ref), 'ip': ip}
            print("ref", ref)
            return render(request, 'front/certificate.html', new_date)

    else:
        #print("ref",ref)
        return render(request, 'front/certificate.html', {'ref': ref, 'ip': ip})
    #return render(request, 'front/certificate.html',{'ip':ip})


@api_view(['GET', 'POST'])
def registration_list(request):
    if request.method == 'GET':
        registered = Registration.objects.all()
        serializer = RegistrationSerializer(registered, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


def data_view(request):
    ip = os.environ.get('EC2_INSTANCE_IP')
    total = Registration.objects.all().count()
    chart = pd.read_sql('select count(address) as count,address from main_registration group by address', con=engine)
    df = pd.DataFrame(chart)
    x = list(df.iloc[:, 1])
    y = list(df.iloc[:, 0])

    # Define a color palette
    color_palette = ['#4C78A8', '#F58518', '#E45756', '#72B7B2', '#54A24B', '#EECA3B']

    # Create a bar chart using Plotly with gridlines
    fig = go.Figure(data=(go.Bar(x=x, y=y, marker_color=color_palette),))
    fig.update_layout(
        title='Areas Covered',
        xaxis=dict(title='Areas', showgrid=True, gridwidth=0.5, gridcolor='rgba(255, 255, 255, 0.1)'),
        yaxis=dict(title='No. of Counts', showgrid=True, gridwidth=0.5, gridcolor='rgba(255, 255, 255, 0.1)'),
        plot_bgcolor='rgba(0, 0, 0, 0)',  # Transparent background
        paper_bgcolor='rgba(0, 0, 0, 0)',  # Transparent background
        font=dict(family='Arial', size=14, color='black'),
        bargap=0.1,  # Adjust the gap between bars
        bargroupgap=0.05  # Adjust the gap between bar groups
    )

    # Convert the figure to HTML code
    chart_html = fig.to_html(full_html=False)

    return render(request, 'front/data.html', {'total': total, 'chart_html': chart_html, 'ip': ip})


@csrf_protect
def login_page(request):
    ip = os.environ.get('EC2_INSTANCE_IP')
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = RegistrationBackend().authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user, backend='main.auth_backends.RegistrationBackend')
                messages.info(request, f"You are now logged in as {username}.")
                #return render(request=request, template_name="front/userpage.html")
                return redirect('user_dashboard')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        # Clear login message if present
        if 'login_message' in request.session:
            del request.session['login_message']
    form = AuthenticationForm()
    return render(request=request, template_name="front/login.html", context={"login_form": form, 'ip': ip})


def user_dashboard(request):
    context = {
        'user': request.user  # Pass the user to the template context
    }
    return render(request, 'front/userpage.html', context=context)


def logout_request(request):
    logout(request)
    request.session['login_message'] = False  # Set login message to False
    messages.success(request, "You have successfully logged out.")
    return render(request=request, template_name="front/home.html")
