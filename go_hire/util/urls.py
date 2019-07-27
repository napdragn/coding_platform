# user/urls.py
from django.conf.urls import url
from util import views

# SET THE NAMESPACE!
app_name = 'util'

# Be careful setting the name to just /login use user-login instead!
urlpatterns = [

    url(r'^send_email/$', views.send_email, name='send_email'),
]