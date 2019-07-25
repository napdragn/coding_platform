from django.conf.urls import url
from judge import views
app_name = 'judge'

urlpatterns = [
    url(r'^compile/$', views.compile, name='compile'),
]