from django.shortcuts import render, get_object_or_404, redirect
from .models import Main, Registration
from .forms import RegistrationForm
from django.http import HttpResponseRedirect

# [model -> view]Create your views here.what needs to be shown in webpage
def home(request):
    sitename = 'SHARMA DRIVING SCHOOL'
    data = Registration.objects.all()
    customer={
        "name":data
    }

    return render(request, 'front/home.html',{'sitename':sitename},{'customer':customer})

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


