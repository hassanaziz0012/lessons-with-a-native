from django.urls import path
from . import views

urlpatterns = [
    path('create-profile/', views.create_profile, name='create-profile'),
    path('manage-profile/', views.manage_profile, name='manage-profile'),
    path('profile/<str:profile_username>', views.profile, name='profile'),
    path('update-profile/<int:profile_id>', views.update_profile, name='update-profile'),
    path('delete-profile/<int:profile_id>', views.delete_profile, name='delete-profile'),

    path('tests/<int:test_id>/save-email-preset', views.save_email_preset, name='save-email-preset'),
    path('tests/<int:test_id>/<int:preset_id>/send-mail', views.send_student_email, name='send-student-email'),
]