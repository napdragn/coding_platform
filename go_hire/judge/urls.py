from django.conf.urls import url
from judge import views
app_name = 'judge'

urlpatterns = [
    url(r'^compile/$', views.compile, name='compile'),
    url(r'^get_submission_result/$', views.get_submission_result, name = 'get_submission_result')
]