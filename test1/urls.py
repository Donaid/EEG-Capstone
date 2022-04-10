
from django.urls import include, path, re_path
from . import views
#All web pages created for http django pages.
urlpatterns = [
    path('', views.homePage, name='homePage'),
    path('homePage/', views.homePage, name='homePage'),
    path('signInPage/', views.signInPage, name='signInPage'),
    path('logout/', views.logout_view, name='logout'),
    path('signUpPage/', views.signUpPage, name='signUpPage'),
    path('profilePage/', views.profilePage, name='profilePage'),
    path('saveattention/', views.saveAttention, name='saveAttention'),
    path('updatelatestsession/', views.updateLatestSession, name='updateLatestSession'),
    path('updateprofiledata/', views.updateProfileData, name='updateProfileData'),
]

