from django.urls import path
from . import views


urlpatterns = [
    path('categories/', views.categories, name='categories'),
    path('category/<int:category_id>', views.category, name='category'),
    path('categories/<int:category_id>/update', views.update_category, name='update-category'),
    path('categories/<int:category_id>/delete', views.delete_category, name='delete-category'),

    path('test/<int:test_id>/add-to-category/<int:category_id>', views.add_to_category, name='add-to-category'),
    path('test/<int:test_id>/remove-from-category/<int:category_id>', views.remove_from_category, name='remove-from-category'),

    path('category/<int:category_id>/profile/<int:profile_id>/take-test', views.take_category_test, name='take-category-test'),
]