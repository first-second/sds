import matplotlib
matplotlib.use('Agg')
from django.shortcuts import render
from .models import Registration
from .models import Orders
from .models import OrderUpdate
from .forms import RegistrationForm
from django.http import HttpResponseRedirect
import matplotlib.pyplot as plt
import pandas as pd
#import mysql.connector as sql
from urllib.parse import quote
from sqlalchemy import create_engine
from .serializers import RegistrationSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from datetime import date,timedelta
from rest_framework import status
from rest_framework.decorators import api_view
from django.http import HttpResponse
from rest_framework.authtoken.views import ObtainAuthToken
from . import checksum
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .auth_backends import RegistrationBackend
from django.contrib.auth.forms import AuthenticationForm
import plotly.graph_objects as go
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.encoding import force_str
from django.urls import reverse
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.http import HttpResponse



MERCHANT_KEY ='dP64425807474247'

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
     
    
    return render(request, 'front/home.html')

def about(request):

    return render(request, 'front/about.html')

def contact(request):

    return render(request, 'front/contact.html')


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            # Send activation email
            current_site = get_current_site(request)
            mail_subject = 'Activate your account'
            message = render_to_string('front/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uidb64': urlsafe_base64_encode(force_bytes(str(user.pk))),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email_address')
            email = EmailMessage(mail_subject, message, to=[to_email])
            print(message,email,to_email)
            email.send()

            return redirect('registration_success')
    else:
        form = RegistrationForm()
    
    return render(request, 'front/register.html', {'form': form})

def activate_account(request, uidb64, token):
    try:
        uid = str(urlsafe_base64_decode(uidb64), 'utf-8')
        user = get_user_model().objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'front/account_activation_success.html')
    else:
        return render(request, 'front/account_activation_failure.html')
    
def registration_success(request):
    return render(request, 'front/registration_success.html')

def certificate(request):
    ref=date.today()-timedelta(days=15)
    if request.method == 'GET':
        query= request.GET.get('q')

        submitbutton= request.GET.get('submit')
        
        if query is not None:
            #lookups= Q(name__icontains=query) | Q(address__icontains=query)
            lookups= Q(date__icontains=query)
            results= Registration.objects.filter(lookups).distinct()

            context={'results': results,
                     'submitbutton': submitbutton}
            #print("ref",ref)
            return render(request, 'front/certificate.html', context)

        else:
            new_date={"ref":str(ref)}
            print("ref",ref)
            return render(request, 'front/certificate.html',new_date)

    else:
        #print("ref",ref)
        return render(request, 'front/certificate.html',{'ref':ref})
    #return render(request, 'front/certificate.html')

@api_view(['GET','POST'])
def Registration_list(request):
    if request.method == 'GET':
        register=Registration.objects.all()
        serializer=RegistrationSerializer(register,many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer=RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)


def dataView(request):
    total = Registration.objects.all().count()
    chart = pd.read_sql('select count(address) as count,address from main_registration group by address', con=engine)
    df = pd.DataFrame(chart)
    X = list(df.iloc[:, 1])
    Y = list(df.iloc[:, 0])

    # Define a color palette
    color_palette = ['#4C78A8', '#F58518', '#E45756', '#72B7B2', '#54A24B', '#EECA3B']

    # Create a bar chart using Plotly with gridlines
    fig = go.Figure(data=[go.Bar(x=X, y=Y, marker_color=color_palette)])
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

    return render(request, 'front/data.html', {'total': total, 'chart_html': chart_html})

def checkout(request):
    if request.method=="POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amount', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        order = Orders(items_json=items_json, name=name, email=email, address=address, city=city,
                       state=state, zip_code=zip_code, phone=phone, amount=amount)
        order.save()
        update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
        update.save()
        thank = True
        id = order.order_id
        #return render(request, 'front/checkout.html', {'thank':thank, 'id': id})
    #return render(request, 'front/checkout.html')
        param_dict={

                'MID': 'rlTBWW05668077930924',
                'TXN_AMOUNT': '1',
                'CUST_ID': 'firstsecondis72@gmail.com',
                'INDUSTRY_TYPE_ID': 'Retail',
                'WEBSITE': 'WEBSTAGING',
                'CHANNEL_ID': 'WEB',
                'CALLBACK_URL':'http://127.0.0.1:8000/main/handlerequest/',

        }
        param_dict['CHECKSUMHASH'] = checksum.generate_checksum(param_dict, MERCHANT_KEY)
        return render(request, 'front/paytm.html', {'param_dict': param_dict})
    return render(request, 'front/checkout.html')

@csrf_exempt
def handlerequest(request):
    # paytm will send you post request here
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            Checksum = form[i]
    print(response_dict,MERCHANT_KEY)
    verify = checksum.verify_checksum(response_dict, MERCHANT_KEY, Checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
    return render(request, 'front/paymentstatus.html', {'response': response_dict})

def LoginPage(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = RegistrationBackend().authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                messages.info(request, f"You are now logged in as {username}.")
                return render(request=request, template_name="front/userpage.html")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        # Clear login message if present
        if 'login_message' in request.session:
            del request.session['login_message']
    form = AuthenticationForm()
    return render(request=request, template_name="front/login.html", context={"login_form": form})


def logout_request(request):
    logout(request)
    request.session['login_message'] = False  # Set login message to False
    messages.success(request, "You have successfully logged out.")
    return render(request=request, template_name="front/home.html")

