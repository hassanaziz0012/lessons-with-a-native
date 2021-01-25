from django.contrib import admin
from .models import EmailPreset, Question, StudentProfile, Test

# Register your models here.
admin.site.register(StudentProfile)
admin.site.register(Test)
admin.site.register(Question)
admin.site.register(EmailPreset)
