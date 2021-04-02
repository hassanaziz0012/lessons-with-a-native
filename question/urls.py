from django.urls import path
from . import views


urlpatterns = [
    path('tests/<int:test_id>/question/<int:question_id>/update', views.update_question, name='update-question'),
    path('tests/<int:test_id>/question/<int:question_id>/delete', views.delete_question, name='delete-question'),

    path('tests/take/p/<int:profile_id>/q/<int:question_id>/c/<int:category_id>/add-to-review/<taking_individual_test>', views.add_to_review, name='add-to-review'),
    path('tests/take/p/<int:profile_id>/q/<int:question_id>/c/<int:category_id>/remove-from-review/<taking_individual_test>', views.remove_from_review, name='remove-from-review'),

    path('import/questions', views.import_all_questions, name='import-all-questions'),
    path('export/questions', views.export_all_questions, name='export-all-questions'),
]