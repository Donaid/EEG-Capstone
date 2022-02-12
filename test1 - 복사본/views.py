from django.shortcuts import render, redirect
import json
from django.http import HttpResponse
from .models import Userss
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

#from django.contrib.auth.models import Users

"""
def signInPage(request):
    a = {
    'aaa' : 'Username or Password is Incorrect',
    }
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        username = request.POST['userid', None]
        password = request.POST['userpw', None]

        user = auth.authenticate(request, username=username, password=password)
        
        if user is not None:
            auth.login(request, user)
            return redirect('homePage')
        else:
            return render(request, 'FYP/signInPage.html',a)
    else:
        return render(request, 'FYP/signInPage.html')
"""

@csrf_exempt
def profilePage(request):

    person = Userss.objects.get(id=1)
    persondict = {
        'userName':4,
        'idealStudyTime':33,
        'audioVideoHighAttentio':40,
        'readWriteHighAttention':50,
        'sessionsCompletedAV':40,
        'sessionsCompletedRW':70,
        'highToTotalAV':90,
        'highToTotalRW':50,
        'graphHighAttention':50,
        'graphLowAttention':50
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

"""
def signInPage(request):
    context = {
        'all_users' : 'l',
    }
    
    if request.method == 'POST':
        userid1 = request.POST['userid']
        userpw1 = request.POST['userpw']
        user = authenticate(request, userid = userid1, userpw = userpw1)
        if user is not None:
            auth.login(request, user)
            return redirect('FYP/homePage.html')
        else:
            return render(request, 'FYP/signInPage.html', context)
    else:
        return render(request, 'FYP/signInPage.html')
"""
"""
class signInPage(View):
    def get(self, request):
        return render(request,'FYP/signInPage.html')
    
    def post(self, request):
        
        id = request.POST.get('userid')
        pw = request.POST.get('userpw')
        msg = False
        infos = Users.objects.all()
        for info in infos:
            if info.userid==id and info.userpw==pw:
                #name=info.username
                msg=True
        msg = 'login is succesful'
        
        context = {
            'msg' : msg,
        }
        return render(request,'FYP/homePage.html', context)
"""
        
def homePage(request):
    all_users = Userss.objects.all()
    context = {
        'all_users' : all_users,
    }
    #return HttpResponse(template.render(context, request))
    return render(request,'FYP/homePage.html', context)
    
def detail(request,  user_id):
    return HttpResponse("<h2>this is a detail page : " + str(user_id)+"</h2>")

"""
def signUpPage(request):
    

    a = {
    'aaa' : 'Username or Password is Incorrect',
    }
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        
        if request.POST['userpw1'] == request.POST['userpw2'] and form.is_valid():
            username = form.cleaned_data.get('userid')
            password = form.cleaned_data.get('userpw1')
            user = User.objects.create(username=username, password=password)
            user = form.save(commit=False)
            user.save()
            auth.login(request, user)
            return redirect('homePage')
    return render(request,'FYP/signUpPage.html', a)




def signUpPage(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('userid')
            raw_password = form.cleaned_data.get('userpw1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('homePage')
    else:
        form = UserCreationForm()
    return render(request, 'FYP/signUpPage.html', {'form': form})


def signUpPage(request):
    form = UserCreationForm(request.POST)
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get('userid')
        password = form.cleaned_data.get('userpw1')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('homePage')
    return render(request, 'FYP/signUpPage.html', {'form': form})


"""
"""
def signUpPage(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SignUpForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            username = form.cleaned_data.get('userid')
            password = form.cleaned_data.get('userpw1')
            user = authenticate(username=username, password=password)
            login(request, user)
            user = form.save(commit=False)
            user.save()
            
            return redirect('homePage')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SignUpForm()

    return render(request, 'FYP/signUpPage.html', {'form': form})


def signUpPage(request):
    if request.method == 'GET':
        form  = SignUpForm()
        context = {'form': form}
        return render(request, 'FYP/signUpPage.html', context)
        if request.method == 'POST':
            form  = SignUpForm(request.POST)
            if form.is_valid():
                
                user = form.cleaned_data.get('userid')
                userpw1 = form.cleaned_data.get('userpw')
                userpw2 = form.cleaned_data.get('userpw2')
                messages.success(request, 'Account was created for ' + user)
                
                Userssa = Userss(userid=user,userpw=userpw1)
                Userssa.save()
                form.save()
                return redirect('homePage')
            else:
                print('Form is not valid')
                messages.error(request, 'Error Processing Your Request')
                context = {'form': form}
                return render(request, 'FYP/signUpPage.html', context)
    
    return render(request, 'FYP/signUpPage.html', {})
"""



def logout(request):
    auth.logout(request)
    return redirect('homePage')





    