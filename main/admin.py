from django.contrib import admin
from question.models import Question
from tests.models import Test
from category.models import Category
from users.models import StudentProfile, EmailPreset


# Register your models here.
admin.site.register(StudentProfile)
admin.site.register(Test)
admin.site.register(Question)
admin.site.register(EmailPreset)
admin.site.register(Category)
