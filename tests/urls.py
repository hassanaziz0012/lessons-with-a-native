from django.urls import path
from . import views


urlpatterns = [
    path('tests/', views.tests, name='tests'),
    path('tests/take/<int:test_id>/profile/<int:profile_id>', views.take_test, name='take-test'),
    path('tests/create-test/', views.create_test, name='create-test'),
    path('tests/update-test/<int:test_id>', views.update_test, name='update-test'),
    path('tests/delete-test/<int:test_id>', views.delete_test, name='delete-test'),
    path('tests/<int:test_id>/', views.test, name='test'),

    path('tests/take/<int:test_id>/profile/<int:profile_id>/category/<int:category_id>/results/good', views.test_score_good, name='test-score-good'),
    path('tests/take/<int:test_id>/profile/<int:profile_id>/category/<int:category_id>/results/needs-work', views.test_score_needs_work, name='test-score-needs-work'),

    path('tests/<int:test_id>/move/up', views.test_move_up, name='test-move-up'),
    path('tests/<int:test_id>/move/down', views.test_move_down, name='test-move-down'),
    
    path('import/tests', views.import_all_tests, name='import-all-tests'),
    path('export/tests', views.export_all_tests, name='export-all-tests'),
]