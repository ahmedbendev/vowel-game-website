from django.urls import path
from . import views
from .views import home
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.home,name='home'),
    path("question/<int:quiz>/<int:qst>/<int:cor>",views.getquestion,name="getquestion"),
    path("checkanswer",views.checkanswer,name="checkanswer"),
    path("nextquestion",views.nextquestion,name="nextquestion"),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('profile/', views.profile, name='profile'),
]