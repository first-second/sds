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
from django.db.models import Q
from datetime import date,timedelta
from rest_framework import status
from rest_framework.decorators import api_view
from django.http import HttpResponse
from rest_framework.authtoken.views import ObtainAuthToken


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
    total=Registration.objects.all().count()
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




    


