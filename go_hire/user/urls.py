# user/urls.py
from django.conf.urls import url
from user import views
# SET THE NAMESPACE!
app_name = 'user'

# Be careful setting the name to just /login use user-login instead!
urlpatterns = [
    url(r'^register/$', views.register,name='register'),
    url(r'^user_login/$', views.user_login, name='user_login'),
    url(r'^profile/$', views.profile_save, name='profile_save'),
]