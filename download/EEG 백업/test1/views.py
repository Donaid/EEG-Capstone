from django.shortcuts import render, redirect
import json
from django.http import HttpResponse

from django.contrib.auth.models import User
from django.template import loader

from django.db.models import Sum
from django.http import JsonResponse
from test1.models import feature
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.models import AbstractBaseUser, UserManager
from django.http import HttpResponseRedirect

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from .forms import SignUpForm
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.views.decorators.csrf import csrf_exempt
from .models import Userss
from .models import userData

@csrf_exempt
def profilePage(request):
    
    

    person = userData.objects.get(id=1)
    persondict = {
        'userName':person.userName,
        'idealStudyTime':person.idealStudyTime,
        'audioVideoHighAttention':person.audioVideoHighAttention,
        'readWriteHighAttention':person.readWriteHighAttention,
        'sessionsCompletedAV':person.sessionsCompletedAV,
        'sessionsCompletedRW':person.sessionsCompletedRW,
        'highToTotalAV':person.highToTotalAV,
        'highToTotalRW':person.highToTotalRW,
        'graphHighAttention':person.graphHighAttention,
        'graphLowAttention':person.graphLowAttention
    }
    personJson = json.dumps(persondict)
    return render(request, 'FYP/profilePage.html', {'personJson': personJson})



def signInPage(request):
    errMsg = {'error':'d'}
    errMsg['error'] = "a"
    if request.method == 'GET':
        return render(request, 'FYP/signInPage.html')

    elif request.method == 'POST':
        username = request.POST.get('userid', None)
        password = request.POST.get('userpw', None)

        if not (username or password):
            errMsg['error'] = "id or password is not entered"
        else:
            user2 = Userss.objects.get(userid = username)
            if user2.userpw == password:
                request.session['user'] = user2.id

                return redirect('homePage')
            else:
                errMsg['error'] = "re-enter password"
        return render(request, 'FYP/signInPage.html', errMsg)
    
    
    
    
def signUpPage(request):
    if request.method == 'POST':
        if request.POST['userpw1'] == request.POST['userpw2']:
            username = request.POST['userid']
            password = request.POST['userpw1']
            
            Userssa = Userss(userid=username,userpw=password)
            Userssa.save()
            
            return redirect('homePage')
        return render(request, 'FYP/signUpPage.html')
    return render(request, 'FYP/signUpPage.html')

def homePage(request):
    all_users = Userss.objects.all()
    context = {
        'all_users' : all_users,
    }
    #return HttpResponse(template.render(context, request))
    return render(request,'FYP/homePage.html', context)
    
def detail(request,  user_id):
    return HttpResponse("<h2>this is a detail page : " + str(user_id)+"</h2>")

def logout(request):
    auth.logout(request)
    return redirect('homePage')





    