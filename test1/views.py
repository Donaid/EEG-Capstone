from sys import getprofile
from urllib.request import Request
from django.forms import ValidationError
from django.shortcuts import render, redirect
import json
from django.http import HttpResponse

from django.contrib.auth.models import User
from django.template import loader

from django.db.models import Sum, Avg
from django.http import JsonResponse
from django.contrib import auth
from django.contrib.auth.models import AbstractBaseUser, UserManager, User
from django.http import HttpResponseRedirect

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.views.decorators.csrf import csrf_exempt
from .models import State, Session
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
import statistics

# @csrf_exempt
@login_required(redirect_field_name=None)
def profilePage(request):
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
        
    except State.DoesNotExist:
        pass

    return render(request, 'FYP/profilePage.html',)

#update profile data
""" 
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
"""

def updateProfileData(request):
    if request.method == "POST" and request.user.is_authenticated:
        
        #bottom
        dataAvailable = 0
        latestStateDate = getProfileLatestDate(request)
        targetDate = latestStateDate

        learningMode = []
        dailySessionData = []
        daily = []
        weekly = []

        if(not isinstance(latestStateDate, str)):
            dataAvailable = 1

        if "targetDate" in request.POST:
            targetDate = datetime.strptime(request.POST['targetDate'], '%Y-%m-%d').date()
            temp = State.objects.filter(user=request.user, date=targetDate)
            if len(temp) == 0:
                dataAvailable = 0
        elif "targetDate" not in request.POST:
            pass
            

        # check if any data in State table
        if(dataAvailable == 1):
            profileDailySessions = getProfileDailySessions(request, targetDate)
            learningMode = profileDailySessions['learningMode']
            dailySessionData = profileDailySessions['dailySessionData']
            daily = getProfileDaily(learningMode, dailySessionData)

        weekly = getProfileWeekly(request, targetDate)

        return HttpResponse(json.dumps({
            'status': 'success onload',
            'userName': request.user.username,
            'idealStudyTime': '1200',
            'audioVideoHighAttention': 1,
            'readWriteHighAttention': 1,
            'sessionsCompletedAV': 1,
            'sessionsCompletedRW': 1,
            'highToTotalAV': 1,
            'highToTotalRW': 1,
            'graphHighAttention': 1,
            'graphLowAttention': 1,
            'dataAvailable': dataAvailable,
            'date': latestStateDate.strftime("%Y-%m-%d") if (not isinstance(latestStateDate, str)) else latestStateDate,
            'learningMode': learningMode,
            'dailySessionData': dailySessionData,
            'daily': daily,
            'weekly': weekly
        }), content_type="application/json")

def getProfileLatestDate(request):
    latestStateDate = datetime.now()
    try:
        latestStateDate = State.objects.filter(user=request.user,).latest('id').date
    except State.DoesNotExist:
        latestStateDate = ''
    
    return latestStateDate

def getProfileDailySessions(request, targetDate):
    profileDailySessions = {
        'learningMode': [],
        'dailySessionData': []
    }

    try:
        latestDateState = State.objects.filter(user=request.user, date=targetDate)
        latestStateLastSession = latestDateState.latest('id').session
        latestStateFirstSession = latestDateState.earliest('id').session

        for x in range(latestStateFirstSession, latestStateLastSession + 1):
            try:
                tempState = State.objects.filter(user=request.user, session=x)
                profileDailySessions['learningMode'].append(tempState.latest('id').learningMethod)
                profileDailySessions['dailySessionData'].append(round(tempState.aggregate(Avg('attention'))['attention__avg'], 2))
            except State.DoesNotExist:
                pass

    except State.DoesNotExist:
        pass

    return profileDailySessions

def getProfileDaily(learningMode, dailySessionData):
    daily = []
    highW = 0 
    lowW = 0 
    highR = 0 
    lowR = 0
    for x in range(0, len(learningMode)):
        if(learningMode[x] == 'w'):
            if(dailySessionData[x] >= 50):
                highW += 1
            else:
                lowW +=1
        elif(learningMode[x] == 'r'):
            if(dailySessionData[x] >= 50):
                highR += 1
            else:
                lowR +=1
    
    totalW = highW + lowW
    totalR = highR + lowR

    if(totalW > 0):
        highW = round((highW * 100) / totalW, 2)
        lowW = round((lowW * 100) / totalW, 2)
    
    if(totalR > 0):
        highR = round((highR * 100) / totalR, 2)
        lowR = round((lowR * 100) / totalR, 2)

    daily.extend((highW, lowW, highR, lowR))
    return daily

def getProfileWeekly(request, targetDate):
    weekly = []
    if not isinstance(targetDate, str):
        weeklySessionData = []
        learningMode = []
        start = targetDate - timedelta(days=targetDate.weekday())

        for singleDate in (start + timedelta(n) for n in range(7)):
            profileWeeklySession = getProfileDailySessions(request, singleDate)
            weeklySessionData.extend(profileWeeklySession['dailySessionData'])
            learningMode.extend(profileWeeklySession['learningMode'])

        weekly = getProfileDaily(learningMode, weeklySessionData)

    return weekly

def signInPage(request):
    errMsg = {}
    errMsg['error'] = ""
    errMsg['inputStatus'] = ""
    if request.method == 'GET':
        if(request.user.is_authenticated):
            return redirect('homePage')
        return render(request, 'FYP/signInPage.html', errMsg)

    elif request.method == 'POST':
        username = request.POST.get('userid', None)
        password = request.POST.get('userpw', None)

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('homePage')
        else:
            errMsg['error'] = "Username or Password is Incorrect"
            errMsg['inputStatus'] = "is-invalid"

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
    idStatus = 'd-none'
    if request.method == 'POST':
        if request.POST['userpw1'] == request.POST['userpw2'] and len(request.POST['userpw1'])>=8 and len(request.POST['userpw1'])<=16:
            username = request.POST['userid']
            password = request.POST['userpw1']
            
            try:
                User.objects.get(username=username)
                idStatus = ''
            except User.DoesNotExist:
                if not (username.isspace() or password.isspace()):
                    User.objects.create_user(username=username, password=password)
                    userCreate = User.objects.get(username=username)
                    Session.objects.create(user=userCreate, latestSession=1)
                    return redirect('homePage')
            
            # return redirect('homePage')
        return render(request, 'FYP/signUpPage.html', {"idStatus": idStatus})
    if(request.user.is_authenticated):
        return redirect('homePage')
    return render(request, 'FYP/signUpPage.html', {"idStatus": idStatus})

@login_required(redirect_field_name=None)
def homePage(request):
    return render(request,'FYP/homePage.html', {'userName' : request.user.username})
    

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
        try: 
            latestStateSession = State.objects.filter(user=request.user,).latest('id').session
            if(latestStateSession >= updateSession.latestSession):
                updateSession.latestSession = latestStateSession + 1
            
            if(request.POST['learningMethod'] == 'r'):
                if(request.POST['consecutiveHigh'] > updateSession.consecutiveHighR):
                    updateSession.consecutiveHighR = request.POST['consecutiveHigh']
            elif(request.POST['learningMethod'] == 'w'):
                updateSession.consecutiveHighW = request.POST['consecutiveHigh']
        except State.DoesNotExist:
            pass

        updateSession.save()

        json_data = json.dumps({'status': 'success'})
        return HttpResponse(json_data, content_type="application/json")



    