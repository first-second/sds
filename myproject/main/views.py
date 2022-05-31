import matplotlib
matplotlib.use('Agg')
from django.shortcuts import render, get_object_or_404, redirect
from .models import Registration
from .forms import RegistrationForm
from django.http import HttpResponseRedirect
import matplotlib.pyplot as plt
import pandas as pd
#import mysql.connector as sql
from urllib.parse import quote
from sqlalchemy import create_engine




#db_connection = sql.connect(host='localhost', database='sds_db', user='adarsh', password='Dbpass@1')

#db_cursor = db_connection.cursor()


# [model -> view]Create your views here.what needs to be shown in webpage
def home(request):
    #sitename = 'SHARMA DRIVING SCHOOL'
    #registerdata = Registration.objects.raw('select id,address from main_registration')
    #data = {
    #    'registerdata':registerdata
    #}
    engine = create_engine(
    "mysql+pymysql://adarsh:%s@localhost:3306/sds_db" % quote('Dbpass@1'),
    )
    chart = pd.read_sql('select count(address) as count,address from main_registration group by address',con=engine)
    df = pd.DataFrame(chart)
    X = list(df.iloc[:,1])
    Y = list(df.iloc[:,0])
    plt.bar(X,Y, color='black')
    plt.savefig('/home/adarsh/Desktop/myweb/myproject/main/static/img/foo.png',dpi=300,) 
    
    return render(request, 'front/home.html',)

def about(request):

    return render(request, 'front/about.html')

def contact(request):

    return render(request, 'front/contact.html')

def register(request):


    submitted = False
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/register?submitted=True')
    else:
        form = RegistrationForm
        if 'submitted' in request.GET:
                submitted = True
    return render(request, 'front/register.html',{'form':form,'submitted':submitted})


