from django.urls import path
from .import views

app_name='auth'

urlpatterns = [
    path('login',views.UserLoginView.as_view(),name='login'),
    path('register', views.UserRegisterView.as_view(), name='register'),
    path('users/<str:id>',views.UserView.as_view(),name='users'),
   
]
