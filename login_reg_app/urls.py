from django.urls import path
from . import views

urlpatterns = [
    path('', views.sign_in),
    path('log-in', views.log_in),
    path('get-email', views.get_email),
    path('<int:user_id>/reset-password', views.reset_password, name="reset_password"),
    path('register', views.register),
    path('reg-me', views.reg_me),
    path('email', views.email),
    path('logout', views.logout),
]