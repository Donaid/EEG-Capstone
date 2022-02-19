
from django.urls import include, path, re_path
from . import views
#All web pages created for http django pages.
urlpatterns = [
    # /test1/
    path('', views.homePage, name='homePage'),
    # /test1/1 
    re_path(r'^(?P<user_id>[0-9]+)/$', views.detail, name='detail'),
    path('homePage/', views.homePage, name='homePage'),
    path('signInPage/', views.signInPage, name='signInPage'),
    path('logout/', views.logout_view, name='logout'),
    path('signUpPage/', views.signUpPage, name='signUpPage'),
    path('profilePage/', views.profilePage, name='profilePage'),
    path('saveattention/', views.saveAttention, name='saveAttention'),
    path('updatelatestsession/', views.updateLatestSession, name='updateLatestSession'),
    path('updateprofiledata/', views.updateProfileData, name='updateProfileData')
    
]

