from django.urls import path
from . import views


urlpatterns = [
    path('categories/', views.CategoriesView.as_view(operation="LIST"), name='categories'),
    path('categories/get', views.CategoriesView.as_view(operation="GET"), name='get-category'),
    path('categories/create', views.CategoriesView.as_view(operation="CREATE"), name='create-category'),
    path('categories/update', views.CategoriesView.as_view(operation="UPDATE"), name='update-category'),
    path('categories/delete', views.CategoriesView.as_view(operation="DELETE"), name='delete-category'),


    path('test/<int:test_id>/add-to-category/<int:category_id>', views.add_to_category, name='add-to-category'),
    path('test/<int:test_id>/remove-from-category/<int:category_id>', views.remove_from_category, name='remove-from-category'),

    path('category/<int:category_id>/profile/<int:profile_id>/take-test', views.take_category_test, name='take-category-test'),
]