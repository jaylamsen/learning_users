from django.conf.urls import url
from basic_app import views

app_name = 'basic_app'

urlpatterns = [
    url('register/', views.register_views, name = 'register'),
    url('user_login', views.user_login_views, name = 'user_login'),
    url('logout/', views.logout_views, name = 'logout')
]
