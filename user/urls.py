from django.urls import path

from . import views

urlpatterns = [
    path('userregistration/', views.UserRegistration.as_view(), name='user_registration'),
    path('login/', views.UserLogin.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),

]
