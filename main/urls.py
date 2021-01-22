from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),

    path('create-profile/', views.create_profile, name='create-profile'),
    path('manage-profile/', views.manage_profile, name='manage-profile'),
    path('update-profile/<int:profile_id>', views.update_profile, name='update-profile'),
    path('delete-profile/<int:profile_id>', views.delete_profile, name='delete-profile'),

    path('tests/', views.tests, name='tests'),
    path('tests/create-test/', views.create_test, name='create-test'),
    path('tests/<int:test_id>/', views.test, name='test'),

]