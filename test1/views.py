from django.forms import ValidationError
from django.shortcuts import render, redirect
import json
from django.http import HttpResponse

from django.contrib.auth.models import User
from django.template import loader

from django.db.models import Sum, Avg
from django.http import JsonResponse
# from test1.models import feature
from django.contrib import auth
from django.contrib.auth.models import AbstractBaseUser, UserManager, User
from django.http import HttpResponseRedirect

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
# from .forms import SignUpForm
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.views.decorators.csrf import csrf_exempt
# from .models import Userss
# from .models import userData
from .models import State, Session
from django.contrib.auth.decorators import login_required
from datetime import datetime
import statistics

# @csrf_exempt
@login_required(redirect_field_name=None)
def profilePage(request):
    # filterStateAll = State.objects.filter(user=request.user)
    # persondict = {
    #     'userName':1,
    #     'idealStudyTime':1,
    #     'audioVideoHighAttention':1,
    #     'readWriteHighAttention':1,
    #     'sessionsCompletedAV':1,
    #     'sessionsCompletedRW':1,
    #     'highToTotalAV':1,
    #     'highToTotalRW':1,
    #     'graphHighAttention':1,
    #     'graphLowAttention':1
    # }
    # personJson = json.dumps(persondict)
    # print(personJson)
    # filterStateAll = State.objects.filter(user=request.user)
    # for state in filterStateAll:
    #     print(state.attention, state.learningMethod, state.session)

    # print(len(State.objects.filter(user=request.user, learningMethod='r')))
    # print(len(State.objects.filter(user=request.user, learningMethod='w')))

    #top
    sessionsCompletedAV = 0
    sessionsCompletedRW = 0
    highToTotalAV = 0
    highToTotalRW = 0
    graphHighAttention = 0

    #bottom
    learningMode = []
    dailySessionData = []
    daily = []
    weekly = []
    latestStateDate = datetime.now()

    try:
        #top
        # totalAV = len(State.objects.filter(user=request.user, learningMethod='w'))
        # totalRW = len(State.objects.filter(user=request.user, learningMethod='r'))
        # highAV = len(State.objects.filter(user=request.user, learningMethod='w', attention__gte=50))
        # highRW = len(State.objects.filter(user=request.user, learningMethod='r', attention__gte=50))
        highAV = 0
        highRW = 0

        #bottom
        latestStateDate = State.objects.filter(user=request.user,).latest('date').date
        latestState = State.objects.filter(user=request.user, date=latestStateDate)
        latestStateDateSession = latestState.latest('session').session
        earliestStateDateSession = latestState.earliest('session').session


        #top
        for x in range(1, latestStateDateSession + 1):
            try:
                tempStateSessions = State.objects.filter(user=request.user, session=x)
                if(tempStateSessions.latest('id').learningMethod == 'r'):
                    sessionsCompletedRW += 1
                    tempRW = tempStateSessions.aggregate(Avg('attention'))
                    if(tempRW['attention__avg'] >= 50):
                        highRW += 1
                elif(tempStateSessions.latest('id').learningMethod == 'w'):
                    sessionsCompletedAV += 1
                    tempAV = tempStateSessions.aggregate(Avg('attention'))
                    if(tempAV['attention__avg'] >= 50):
                        highAV += 1
            except State.DoesNotExist: 
                pass

        totalAV = sessionsCompletedAV
        if(totalAV == 0):
            totalAV = 1

        totalRW = sessionsCompletedRW
        if(totalRW == 0):
            totalRW = 1
        
        highToTotalAV = round((highAV * 100) / totalAV, 2)
        highToTotalRW = round((highRW *100) / totalRW, 2)


        allTotalSessions = sessionsCompletedRW + sessionsCompletedRW
        if(allTotalSessions == 0):
            allTotalSessions = 1
        graphHighAttention = (highAV + highRW) / allTotalSessions
        

        #bottom
        for x in range(earliestStateDateSession, latestStateDateSession + 1):
            try:
                tempStateSessions = State.objects.filter(user=request.user, session=x)
                learningMode.append(tempStateSessions.latest('id').learningMethod)
                count = 0 
                tempAttentionSum = 0
                for tempStateSession in tempStateSessions:
                    tempAttentionSum += tempStateSession.attention
                    count += 1

                dailySessionData.append(round(tempAttentionSum / count, 2))
            except State.DoesNotExist: 
                pass
    except State.DoesNotExist:
        pass

    highW = 0
    lowW = 0
    highR = 0
    lowR = 0
    totalW = 0
    totalR = 0
    for x in range(0, len(learningMode)):
        if(learningMode[x] == 'w'):
            if(dailySessionData[x] >= 50):
                highW += 1
            else:
                lowW += 1
        elif(learningMode[x] == 'r'):
            if(dailySessionData[x] >= 50):
                highR += 1
            else:
                lowR += 1
    
    totalW = highW + lowW
    totalR = highR + lowR
    if(totalW == 0):
        totalW = 1
    if(totalR == 0):
        totalR = 1
    
    daily.append((highW * 100) / (totalW))
    daily.append((lowW * 100) / (totalW))
    daily.append((highR * 100) / (totalR))
    daily.append((lowR * 100) / (totalR))

    persondict = {
        'userName' : request.user.username,
        'date' : latestStateDate.strftime("%Y-%m-%d"),
        'dailySessionData': dailySessionData,
        'learningMode': learningMode,
        'daily' : daily,
        'sessionsCompletedAV' : sessionsCompletedAV,
        'sessionsCompletedRW' : sessionsCompletedRW,
        'highToTotalAV' : highToTotalAV,
        'highToTotalRW' : highToTotalRW,
        'graphHighAttention' : round(graphHighAttention, 2),
        'graphLowAttention' : round(10 - graphHighAttention, 2)
    }
    # print(persondict)
    personJson = json.dumps(persondict)
    return render(request, 'FYP/profilePage.html', {'personJson': personJson})
    # return render(request, 'FYP/profilePage.html')

def updateProfileData(request):
    if request.method == "POST" and request.user.is_authenticated:
        # print(request.POST['targetDate'])
        targetDate = request.POST['targetDate']
        learningMode = []
        dailySessionData = []
        daily = []
        weekly = []
        dataAvailable = 1
        latestStateDate = datetime.now()

        # try:
        #     datetime.strptime(targetDate, '%Y-%m-%d')
        #     print('valid date')
        # except ValueError:
        #     print('invalid date')

        try:
            latestStateDate = State.objects.filter(user=request.user,).latest('date').date
            latestState = State.objects.filter(user=request.user, date=targetDate)
            latestStateDateSession = latestState.latest('session').session
            earliestStateDateSession = latestState.earliest('session').session

            for x in range(earliestStateDateSession, latestStateDateSession + 1):
                try:
                    tempStateSessions = State.objects.filter(user=request.user, session=x)
                    learningMode.append(tempStateSessions.latest('id').learningMethod)
                    count = 0 
                    tempAttentionSum = 0
                    for tempStateSession in tempStateSessions:
                        tempAttentionSum += tempStateSession.attention
                        count += 1

                    dailySessionData.append(round(tempAttentionSum / count, 2))
                except State.DoesNotExist: 
                    pass
        except State.DoesNotExist:
            dataAvailable = 0

        highW = 0
        lowW = 0
        highR = 0
        lowR = 0
        totalW = 0
        totalR = 0
        for x in range(0, len(learningMode)):
            if(learningMode[x] == 'w'):
                if(dailySessionData[x] >= 50):
                    highW += 1
                else:
                    lowW += 1
            elif(learningMode[x] == 'r'):
                if(dailySessionData[x] >= 50):
                    highR += 1
                else:
                    lowR += 1
        
        totalW = highW + lowW
        totalR = highR + lowR
        if(totalW == 0):
            totalW = 1
        if(totalR == 0):
            totalR = 1
        
        daily.append((highW * 100) / (totalW))
        daily.append((lowW * 100) / (totalW))
        daily.append((highR * 100) / (totalR))
        daily.append((lowR * 100) / (totalR))

        json_data = json.dumps({
            'dataAvailable': dataAvailable,
            'dailySessionData': dailySessionData,
            'learningMode': learningMode,
            'daily' : daily,
            'date' : latestStateDate.strftime("%Y-%m-%d"),
        })

        return HttpResponse(json_data, content_type="application/json")

def signInPage(request):
    errMsg = {'error':'d'}
    errMsg['error'] = ""
    if request.method == 'GET':
        if(request.user.is_authenticated):
            return redirect('homePage')
        return render(request, 'FYP/signInPage.html')

    elif request.method == 'POST':
        username = request.POST.get('userid', None)
        password = request.POST.get('userpw', None)

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('homePage')
        else:
            errMsg['error'] = "re-enter password"

        # if not (username or password):
        #     errMsg['error'] = "id or password is not entered"
        # else:
        #     user2 = Userss.objects.get(userid = username)
        #     if user2.userpw == password:
        #         request.session['user'] = user2.id

        #         return redirect('homePage')
        #     else:
        #         errMsg['error'] = "re-enter password"
        return render(request, 'FYP/signInPage.html', errMsg)
    
    
def signUpPage(request):
    if request.method == 'POST':
        if request.POST['userpw1'] == request.POST['userpw2']:
            username = request.POST['userid']
            password = request.POST['userpw1']
            
            try:
                User.objects.get(username=username)
            except User.DoesNotExist:
                if not (username. isspace() or password. isspace()):
                    User.objects.create_user(username=username, password=password)
                    userCreate = User.objects.get(username=username)
                    Session.objects.create(user=userCreate, latestSession=1)
                    return redirect('homePage')
            
            # return redirect('homePage')
        print("not allowed")
        return render(request, 'FYP/signUpPage.html')
    if(request.user.is_authenticated):
        return redirect('homePage')
    return render(request, 'FYP/signUpPage.html')

@login_required(redirect_field_name=None)
def homePage(request):
    # all_users = Userss.objects.all()
    # context = {
    #     'all_users' : all_users,
    # }
    return render(request,'FYP/homePage.html', {'userName' : request.user.username})
    
def detail(request,  user_id):
    return HttpResponse("<h2>this is a detail page : " + str(user_id)+"</h2>")

@login_required(redirect_field_name=None)
def logout_view(request):
    logout(request)
    return redirect('signInPage')

def saveAttention(request):
    if request.method == "POST" and request.user.is_authenticated:
        latestUserSession = Session.objects.get(user=request.user)
        save_attention = State(attention=request.POST['attention'], learningMethod=request.POST['learningMethod'], user=request.user, session=latestUserSession.latestSession)
        save_attention.save()
        json_data = json.dumps({'status': 'success'})
        return HttpResponse(json_data, content_type="application/json")

def updateLatestSession(request):
    if request.method == "POST" and request.user.is_authenticated:
        updateSession = Session.objects.get(user=request.user)
        updateSession.latestSession = updateSession.latestSession + 1
        updateSession.save()
        json_data = json.dumps({'status': 'success'})
        return HttpResponse(json_data, content_type="application/json")



    