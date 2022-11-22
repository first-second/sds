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
from .serializers import RegistrationSerializer
from rest_framework.views import APIView
from rest_framework.response import Response


engine = create_engine(
    'sqlite:///db.sqlite3',
    )

#db_connection = sql.connect(host='localhost', database='sds_db', user='adarsh', password='Dbpass@1')

#db_cursor = db_connection.cursor()

# [model -> view]Create your views here.what needs to be shown in webpage

def count_rows():
    query=pd.read_sql('select * from main_registration',con=engine)
    df=pd.DataFrame(query)
    total = df['id'].count()
    return total

def home(request):
    #sitename = 'SHARMA DRIVING SCHOOL'
    #registerdata = Registration.objects.raw('select id,address from main_registration')
    #data = {
    #    'registerdata':registerdata
    #}
    total=count_rows()
    chart = pd.read_sql('select count(address) as count,address from main_registration group by address',con=engine)
    df = pd.DataFrame(chart)
    X = list(df.iloc[:,1])
    Y = list(df.iloc[:,0])
    plt.bar(X,Y, color=['orange', 'red', 'green', 'blue', 'cyan', 'yellow'])
    plt.xlabel("Areas covered")
    plt.ylabel("No. of counts")
    plt.savefig('./main/static/img/foo.png',dpi=300,) 
    
    return render(request, 'front/home.html',{'total':total})

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

class RegistrationList(APIView):
    def get(self, request):
        Registration1=Registration.objects.all()
        serializer=RegistrationSerializer(Registration1,many=True)
        return Response(serializer.data)
    def post(self):
        pass


    


