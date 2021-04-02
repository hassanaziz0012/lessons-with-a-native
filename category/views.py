from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import CreateCategoryForm, UpdateCategoryForm
from .models import Category
from tests.models import Test
from question.models import Question
from users.models import StudentProfile


# Create your views here.
def categories(request):
    if request.method == 'POST':
        form = CreateCategoryForm(request.POST)
        u_form = UpdateCategoryForm(request.POST)
        if form.is_valid():
            form.save()

        if u_form.is_valid():
            pass
    else:
        form = CreateCategoryForm()
        u_form = UpdateCategoryForm()

    context = {
        'title': 'Categories',
        'form': form,
        'u_form': u_form,
        'tests': Test.objects.all(),
        'categories': Category.objects.all(),
    }
    return render(request, 'main/categories.html', context=context)

def category(request, category_id):
    category = Category.objects.filter(pk=category_id).first()
    tests = Test.objects.filter(category=category)
    questions = Question.objects.all()

    context = {
        'title': str(category.category_name),
        'category': category,
        'tests': tests,
        'questions': questions,
    }
    return render(request, 'main/category.html', context=context)

def delete_category(request, category_id):
    category = Category.objects.filter(pk=category_id).first()
    category.delete()

    messages.success(request, 'The category has successfully been deleted!', extra_tags='alert alert-success')
    return redirect('categories')

def update_category(request, category_id):
    category = Category.objects.filter(pk=category_id).first()
    if request.method == 'POST':
        if request.POST['category_name']:
            category.category_name = request.POST['category_name']
        category.save()
        
        messages.success(request, 'The category was successfully updated.', extra_tags='alert alert-success')
        return redirect('categories')
            
def add_to_category(request, test_id, category_id):
    test = Test.objects.filter(pk=test_id).first()
    category = Category.objects.filter(pk=category_id).first()

    test.category = category
    test.save()
    
    messages.success(request, f'{test.test_name} was added to the category {category.category_name}.', extra_tags='alert alert-success')
    return redirect('category', category.id)
    
def remove_from_category(request, test_id, category_id):
    test = Test.objects.filter(pk=test_id).first()
    category = Category.objects.filter(pk=category_id).first()

    test.category = Category.objects.filter(category_name='Default').first()
    test.save()

    messages.success(request, f'{test.test_name} was removed from the category {category.category_name}.', extra_tags='alert alert-success')
    return redirect('category', category.id)

def take_category_test(request, category_id, profile_id):
    category = Category.objects.filter(pk=category_id).first()
    profile = StudentProfile.objects.filter(pk=profile_id).first()
    tests = Test.objects.filter(category=category)
    questions = Question.objects.all()
    
    # category.taking_category_test_bool = True
    # category.save()

    review_questions_bool = False
    for question in Question.objects.all():
        if question.review_question == True:
            review_questions_bool = True
            break
        else:
            review_questions_bool = False

    context = {
        'title': str(category.category_name) + ' - Take Test',
        'category': category,
        'tests': tests,
        'profile': profile,
        'questions': questions,
        'review_questions_bool': review_questions_bool,

        'taking_individual_test': False,
    }
    return render(request, 'main/take_category_test.html', context=context)