from os import name
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),

    path('create-profile/', views.create_profile, name='create-profile'),
    path('manage-profile/', views.manage_profile, name='manage-profile'),
    path('profile/<str:profile_username>', views.profile, name='profile'),
    path('update-profile/<int:profile_id>', views.update_profile, name='update-profile'),
    path('delete-profile/<int:profile_id>', views.delete_profile, name='delete-profile'),

    path('tests/', views.tests, name='tests'),
    path('tests/take/<int:test_id>/profile/<int:profile_id>', views.take_test, name='take-test'),
    path('tests/create-test/', views.create_test, name='create-test'),
    path('tests/update-test/<int:test_id>', views.update_test, name='update-test'),
    path('tests/delete-test/<int:test_id>', views.delete_test, name='delete-test'),
    path('tests/<int:test_id>/', views.test, name='test'),

    path('tests/<int:test_id>/question/<int:question_id>/update', views.update_question, name='update-question'),
    path('tests/<int:test_id>/question/<int:question_id>/delete', views.delete_question, name='delete-question'),

    path('tests/take/<int:test_id>/profile/<int:profile_id>/category/<int:category_id>/results/good', views.test_score_good, name='test-score-good'),
    path('tests/take/<int:test_id>/profile/<int:profile_id>/category/<int:category_id>/results/needs-work', views.test_score_needs_work, name='test-score-needs-work'),

    path('tests/<int:test_id>/move/up', views.test_move_up, name='test-move-up'),
    path('tests/<int:test_id>/move/down', views.test_move_down, name='test-move-down'),

    path('tests/<int:test_id>/save-email-preset', views.save_email_preset, name='save-email-preset'),
    path('tests/<int:test_id>/<int:preset_id>/send-mail', views.send_student_email, name='send-student-email'),

    path('tests/take/p/<int:profile_id>/q/<int:question_id>/c/<int:category_id>/add-to-review/<taking_individual_test>', views.add_to_review, name='add-to-review'),
    path('tests/take/p/<int:profile_id>/q/<int:question_id>/c/<int:category_id>/remove-from-review/<taking_individual_test>', views.remove_from_review, name='remove-from-review'),

    path('import/tests', views.import_all_tests, name='import-all-tests'),
    path('export/tests', views.export_all_tests, name='export-all-tests'),

    path('import/questions', views.import_all_questions, name='import-all-questions'),
    path('export/questions', views.export_all_questions, name='export-all-questions'),

    path('categories/', views.categories, name='categories'),
    path('category/<int:category_id>', views.category, name='category'),
    path('categories/<int:category_id>/update', views.update_category, name='update-category'),
    path('categories/<int:category_id>/delete', views.delete_category, name='delete-category'),

    path('test/<int:test_id>/add-to-category/<int:category_id>', views.add_to_category, name='add-to-category'),
    path('test/<int:test_id>/remove-from-category/<int:category_id>', views.remove_from_category, name='remove-from-category'),

    path('category/<int:category_id>/profile/<int:profile_id>/take-test', views.take_category_test, name='take-category-test'),


]