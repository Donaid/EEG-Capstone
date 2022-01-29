from django.shortcuts import render

from django.http import HttpResponse
from .models import Users
from django.template import loader

from django.shortcuts import render
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render
from test1.models import feature

def homePage(request):
    all_users = Users.objects.all()
    context = {
        'all_users' : all_users,
    }
    #return HttpResponse(template.render(context, request))
    return render(request,'FYP/homePage.html', context)
    
def detail(request,  user_id):
    return HttpResponse("<h2>this is a detail page : " + str(user_id)+"</h2>")

def signInPage(request):
    all_users = Users.objects.all()

    context = {
        'all_users' : all_users,
     
    }
    
    return render(request,'FYP/signInPage.html', context)
    
def signUpPage(request):
    all_users = Users.objects.all()

    context = {
        'all_users' : all_users,
    }
    
    return render(request,'FYP/signUpPage.html', context)

def profilePage(request):
    all_users = Users.objects.all()

    context = {
        'all_users' : all_users,
    }
    
    #return HttpResponse(template.render(context, request))
    return render(request,'FYP/profilePage.html', context)











    