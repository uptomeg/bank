from django.urls import path
from . import views

app_name="accounts"
urlpatterns = [ 
    path('register/', views.SignupView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name="login"),
    path('logout/', views.logout, name="logout"),
    path('profile/view/', views.profileview, name="view"),
    path('profile/edit/', views.edit_profile, name="edit"),
]
