from django.contrib import admin
from django.urls import path
from user.views import login,Logout,create_user
from user import views
from django.conf.urls import url 

urlpatterns = [
    path('login/', login),
    path('create_user/', create_user),
    path('logout/', Logout.as_view()),
    path('movie/(<movie_id>[0-9]+)',views.MovieView.as_view()),
	path('movie/',views.MovieView.as_view()),
]