from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('registration/', views.registration, name='registration'),
    path('contact_us/', views.contact_us, name='contact_us'),
    path('courses/', views.courses, name='courses'),
    path('placement/', views.placement, name='placement'),
    path('course_detail/<str:name>', views.course_detail, name='course_detail'),
    path('edit/', views.edit, name='edit'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', views.login, name='login'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('otp/', views.code, name='otp'),
    path('new_password/', views.new_password, name='new_password'),
    path('enroll/', views.enroll, name='enroll'),
    path('search/', views.Search.as_view(), name='Search'),
    path('delete', views.delete, name='delete'),
    path("logout",views.logout,name="logout")
]
