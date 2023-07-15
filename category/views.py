from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.views import View

from .forms import CreateCategoryForm, UpdateCategoryForm
from .models import Category
from tests.models import Test
from question.models import Question
from users.models import StudentProfile


# Create your views here.
class CategoriesView(View):
    operation = ""
    
    def get(self, request):
        if self.operation == "LIST":
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

        elif self.operation == "GET":
            category_id = request.GET.get('category_id')
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

        elif self.operation == "DELETE":
            category_id = request.GET.get('category_id')
            category = Category.objects.get(pk=category_id)
            category.delete()

            messages.success(request, 'The category has successfully been deleted!', extra_tags='alert alert-success')
            return redirect('categories')


    def post(self, request):
        if self.operation == "CREATE":
            form = CreateCategoryForm(request.POST)
            u_form = UpdateCategoryForm(request.POST)
            if form.is_valid():
                form.save()

            if u_form.is_valid():
                pass

            return redirect('categories')

        elif self.operation == "UPDATE":
            category_id = request.GET.get('category_id')
            category_name = request.POST.get('category_name')
            category = Category.objects.get(pk=category_id)
            
            if category_name:
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
    return redirect(reverse('get-category') + f"?category_id={category.pk}")
    
def remove_from_category(request, test_id, category_id):
    test = Test.objects.filter(pk=test_id).first()
    category = Category.objects.filter(pk=category_id).first()

    test.category = Category.objects.filter(category_name='Default').first()
    test.save()

    messages.success(request, f'{test.test_name} was removed from the category {category.category_name}.', extra_tags='alert alert-success')
    return redirect(reverse('get-category') + f"?category_id={category.pk}")

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