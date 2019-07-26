from django.contrib import admin
from .models import Contest, ContestQuestionMapping, UserContest


admin.site.register(Contest)
admin.site.register(UserContest)
admin.site.register(ContestQuestionMapping)
