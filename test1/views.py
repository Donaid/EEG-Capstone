from django.shortcuts import render, redirect
import json
from django.http import HttpResponse

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.db.models import Avg
from .models import State, Session

from datetime import datetime, timedelta


@login_required(redirect_field_name=None)
def profilePage(request):
    return render(request, 'FYP/profilePage.html',)

def updateProfileData(request):
    if request.method == "POST" and request.user.is_authenticated:
        # top
        idealStudyTime = "-"
        audioVideoHighAttention = 0
        readWriteHighAttention = 0
        profileSummary = {
            'sessionsCompletedAV': 0,
            'sessionsCompletedRW': 0,
            'highToTotalAV': 0,
            'highToTotalRW': 0,
            'graphHighAttention': 0,
            'graphLowAttention': 0
        }

        #bottom
        dataAvailable = 0
        latestStateDate = getProfileLatestDate(request.user)
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

        # check if any data in State table
        if(dataAvailable == 1):
            profileDailySessions = getProfileDailySessions(request.user, targetDate)
            learningMode = profileDailySessions['learningMode']
            dailySessionData = profileDailySessions['dailySessionData']
            daily = getProfileDaily(learningMode, dailySessionData)

            if "targetDate" not in request.POST:
                targetUserSession = Session.objects.get(user=request.user)
                audioVideoHighAttention = targetUserSession.consecutiveHighW
                readWriteHighAttention = targetUserSession.consecutiveHighR
                
                profileSummary = getProfileSummary(request.user)
                idealStudyTime = getProfileIdealTime(request.user)

        weekly = getProfileWeekly(request.user, targetDate)

        return HttpResponse(json.dumps({
            'status': 'success',
            'userName': request.user.username,
            'idealStudyTime': idealStudyTime,
            'audioVideoHighAttention': audioVideoHighAttention,
            'readWriteHighAttention': readWriteHighAttention,
            'sessionsCompletedAV': profileSummary['sessionsCompletedAV'],
            'sessionsCompletedRW': profileSummary['sessionsCompletedRW'],
            'highToTotalAV': profileSummary['highToTotalAV'],
            'highToTotalRW': profileSummary['highToTotalRW'],
            'graphHighAttention': profileSummary['graphHighAttention'],
            'graphLowAttention': profileSummary['graphLowAttention'],
            'dataAvailable': dataAvailable,
            'date': latestStateDate.strftime("%Y-%m-%d") if (not isinstance(latestStateDate, str)) else latestStateDate,
            'learningMode': learningMode,
            'dailySessionData': dailySessionData,
            'daily': daily,
            'weekly': weekly
        }), content_type="application/json")

def getProfileIdealTime(user):
    highestAttention = 0
    idealStudyTime = ""
    for hour in range(0, 24):
        start_time = datetime.strptime(str(hour) + ":00:00.000000", "%H:%M:%S.%f")
        end_time = datetime.strptime(str(hour) + ":59:59.999999", "%H:%M:%S.%f")
        try: 
            targetTimeState = State.objects.filter(user=user, time__range=(start_time, end_time))
            if len(targetTimeState) != 0:
                averageAttention = round(targetTimeState.aggregate(Avg('attention'))['attention__avg'], 2)
                if(averageAttention > 0):
                    if(averageAttention > highestAttention):
                        highestAttention = averageAttention
                        idealStudyTime = start_time.strftime('%H%M')
                    elif(averageAttention == highestAttention):
                        if idealStudyTime.isspace():
                           idealStudyTime =  start_time.strftime('%H%M')
                        else:
                            idealStudyTime += f"/ {start_time.strftime('%H%M')}"
        except State.DoesNotExist:
            pass
    
    return "-" if idealStudyTime.isspace() else idealStudyTime

def getProfileSummary(user):
    profileSummary = {
        'sessionsCompletedAV': 0,
        'sessionsCompletedRW': 0,
        'highToTotalAV': 0,
        'highToTotalRW': 0,
        'graphHighAttention': 0,
        'graphLowAttention': 0
    }

    latestSession = State.objects.filter(user=user).latest('id').session
    for x in range(1, latestSession + 1):
        try:
            targetSession = State.objects.filter(user=user, session=x)
            if len(targetSession) != 0:
                targetSessionAverage = round(targetSession.aggregate(Avg('attention'))['attention__avg'], 2)
                if(targetSession.latest('id').learningMethod == 'r'):
                    profileSummary['sessionsCompletedRW'] += 1
                    if targetSessionAverage >= 50:
                        profileSummary['highToTotalRW'] += 1
                        profileSummary['graphHighAttention'] += 1
                else: 
                    profileSummary['sessionsCompletedAV'] += 1
                    if targetSessionAverage >= 50:
                        profileSummary['highToTotalAV'] += 1
                        profileSummary['graphHighAttention'] += 1
        except State.DoesNotExist:
            pass
        
    profileSummary['graphLowAttention'] = profileSummary['sessionsCompletedAV'] + profileSummary['sessionsCompletedRW'] - profileSummary['graphHighAttention']
    if(profileSummary['sessionsCompletedRW'] > 0):
        profileSummary['highToTotalRW'] = round((profileSummary['highToTotalRW'] * 100) / profileSummary['sessionsCompletedRW'], 2)
    if(profileSummary['sessionsCompletedAV'] > 0):
        profileSummary['highToTotalAV'] = round((profileSummary['highToTotalAV'] * 100) / profileSummary['sessionsCompletedAV'], 2)

    return profileSummary

def getProfileLatestDate(user):
    latestStateDate = datetime.now()
    try:
        latestStateDate = State.objects.filter(user=user,).latest('id').date
    except State.DoesNotExist:
        latestStateDate = ''
    
    return latestStateDate

def getProfileDailySessions(user, targetDate):
    profileDailySessions = {
        'learningMode': [],
        'dailySessionData': []
    }

    try:
        latestDateState = State.objects.filter(user=user, date=targetDate)
        latestStateLastSession = latestDateState.latest('id').session
        latestStateFirstSession = latestDateState.earliest('id').session

        for x in range(latestStateFirstSession, latestStateLastSession + 1):
            try:
                tempState = State.objects.filter(user=user, session=x)
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

def getProfileWeekly(user, targetDate):
    weekly = []
    if not isinstance(targetDate, str):
        weeklySessionData = []
        learningMode = []
        start = targetDate - timedelta(days=targetDate.weekday())

        for singleDate in (start + timedelta(n) for n in range(7)):
            profileWeeklySession = getProfileDailySessions(user, singleDate)
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

        return render(request, 'FYP/signInPage.html', errMsg)
    
    
def signUpPage(request):
    idStatus = 'd-none'
    if request.method == 'POST':
        if (request.POST['userpw1'] == request.POST['userpw2']) and len(request.POST['userpw1'])>=8 and len(request.POST['userpw1'])<=16:
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
                if(int(request.POST['consecutiveHigh']) > updateSession.consecutiveHighR):
                    updateSession.consecutiveHighR = request.POST['consecutiveHigh']
            elif(request.POST['learningMethod'] == 'w'):
                if(int(request.POST['consecutiveHigh']) > updateSession.consecutiveHighW):
                    updateSession.consecutiveHighW = request.POST['consecutiveHigh']
        except State.DoesNotExist:
            pass

        updateSession.save()

        json_data = json.dumps({'status': 'success'})
        return HttpResponse(json_data, content_type="application/json")



    