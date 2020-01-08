from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('', views.mainpage, name='mainpage'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('upload', views.upload, name='upload'),
    path('playvideo/<int:video_id>', views.playvideo, name='playvideo'),
    path('category/<category>', views.category, name='category'),
]
