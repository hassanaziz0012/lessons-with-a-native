from django.shortcuts import render, redirect
from django.http import HttpResponse
from tests.models import Test
from django.contrib import messages

from .models import Test
from .forms import CreateTestForm, UpdateTestForm
from question.models import Question
from category.models import Category
from users.models import StudentProfile, EmailPreset
from question.forms import AddQuestionForm
from users.forms import EmailStudentForm
from main.views import write_to_file

import pandas
import csv


# Create your views here.
def tests(request):
    tests = Test.objects.all().order_by('test_order')

    questions = Question.objects.all()
    profiles = StudentProfile.objects.all()

    if request.method == 'POST':
        c_form = CreateTestForm(request.POST)
        u_form = UpdateTestForm(request.POST)

        if c_form.is_valid():
            c_form.save(commit=False)
            test = Test(
                test_name = c_form.cleaned_data['test_name'],
                test_directions = c_form.cleaned_data['test_directions'],
                test_order = len(Test.objects.all()),
                )

            # All tests go into a "Default" category. If that doesn't exist, create it.
            if Category.objects.filter(category_name='Default').first() == None:
                c = Category.objects.create(category_name='Default')
                c.save()
            
            test.category = Category.objects.filter(category_name='Default').first()

            test.save()

            for profile in profiles:
                test.test_status_new.add(profile)
                test.save()

            messages.success(request, 'This test has been created.', extra_tags='alert alert-primary')
            return redirect('tests')

    else:
        c_form = CreateTestForm()
        u_form = UpdateTestForm()

    context = {
        'title': 'Tests',
        'tests': tests,
        'questions': questions,
        'form': c_form,
        'u_form': u_form,
        'last_test': len(Test.objects.all()) - 1,
    }
    return render(request, 'main/tests.html', context=context)

def create_test(request):
    context = {
        'title': 'Create Test'
    }

    return redirect('tests')

def test(request, test_id):
    test = Test.objects.filter(pk=test_id).first()
    questions = Question.objects.filter(test=test).order_by('id')

    if request.method == 'POST':
        form = AddQuestionForm(request.POST)
        e_form = EmailStudentForm(request.POST)

        if form.is_valid():
            form.save(commit=False)
            question = Question(
                test=test,
                question=form.cleaned_data['question'],
                answer=form.cleaned_data['answer'],
            )
            question.save()

    else:
        form = AddQuestionForm()
        e_form = EmailStudentForm()


    context = {
        'title': test.test_name,
        'test': test,
        'questions': questions,
        'form': form,
        'e_form': e_form,
        'categories': Category.objects.all(),
        'presets': EmailPreset.objects.all(),
    }
    return render(request, 'main/test.html', context=context)

def delete_test(request, test_id):
    test = Test.objects.filter(pk=test_id).first()
    test.delete()
    messages.success(request, 'This test has been deleted!', extra_tags='alert alert-success')

    return redirect('tests')

def update_test(request, test_id):
    test = Test.objects.filter(pk=test_id).first()

    if request.method == 'POST':
        if request.POST['test_name']:
            test.test_name = request.POST['test_name']
        if request.POST['test_directions']:
            test.test_directions = request.POST['test_directions']
        test.save()

        messages.success(request, 'The test was successfully updated.', extra_tags='alert alert-success')
        return redirect('tests')
    else:
        messages.error(request, "It didn't work", extra_tags='alert alert-danger')
        return redirect('tests')

def take_test(request, test_id, profile_id):
    test = Test.objects.filter(pk=test_id).first()
    questions = Question.objects.filter(test=test).order_by('id')

    for question in Question.objects.all():
        if question.review_question == True:
            review_questions_bool = True
            break
        else:
            review_questions_bool = False

    profile = StudentProfile.objects.filter(pk=profile_id).first()

    context = {
        'title': str(test.test_name) + ' - Test',
        'test': test,
        'category': test.category,
        'questions': questions,
        'profile': profile,
        'review_questions_bool': review_questions_bool,

        'taking_individual_test': True,
    }
    return render(request, 'main/take_test.html', context=context)




def test_score_good(request, test_id, profile_id, category_id):
    test = Test.objects.filter(pk=test_id).first()
    profile = StudentProfile.objects.filter(pk=profile_id).first()
    category = Category.objects.filter(pk=category_id).first()

    test.test_status_good.add(profile) # Set the test to status(Good) for this profile.

    # Remove this test's New and Repeat statuses for this profile.
    test.test_status_new.remove(profile)
    test.test_status_repeat.remove(profile)
    test.test_status_due.remove(profile)

    test.save() # Save changes.

    prev_test = Test.objects.filter(test_order=test.test_order-1).first()
    next_test = Test.objects.filter(test_order=test.test_order+1).first()

    # Schedule the tests that are currently on repeat.
    for test_obj in Test.objects.all():
        if profile in test_obj.test_status_repeat.all():
            test_obj.test_repeat_due -= 1
            test_obj.test_status_due.remove(profile)

            test_obj.save()

        if test_obj.test_repeat_due == 0:
            test_obj.test_status_due.add(profile)
            test_obj.test_repeat_due = 6
            test_obj.test_status_repeat.remove(profile)

            test_obj.save()

    return redirect('take-category-test', category.id, profile.id)

    # context = {
    #     'title': f'{test.test_name} - Graded Good', 
    #     'profile': profile, 
    #     'tests': Test.objects.all(),
    #     'prev_test': prev_test,
    #     'next_test': next_test,
    #     }
    # return render(request, 'main/test_score_good.html', context=context)

def test_score_needs_work(request, test_id, profile_id, category_id):
    test = Test.objects.filter(pk=test_id).first()
    profile = StudentProfile.objects.filter(pk=profile_id).first()
    category = Category.objects.filter(pk=category_id).first()

    test.test_status_repeat.add(profile) # Set the test to status(Good) for this profile.
    test.test_repeat_due = 6

    # Remove this test's New and Repeat statuses for this profile.
    test.test_status_new.remove(profile)
    test.test_status_good.remove(profile)

    test.save() # Save changes.

    # Schedule the tests that are currently on repeat.
    for test_obj in Test.objects.all():
        if profile in test_obj.test_status_repeat.all():
            test_obj.test_repeat_due -= 1
            test_obj.test_status_due.remove(profile)

            test_obj.save()

        if test_obj.test_repeat_due == 0:
            test_obj.test_status_due.add(profile)
            test_obj.test_repeat_due = 6
            test_obj.test_status_repeat.remove(profile)

            test_obj.save()

    prev_test = Test.objects.filter(test_order=test.test_order-1).first()
    next_test = Test.objects.filter(test_order=test.test_order+1).first()

    return redirect('take-category-test', category.id, profile.id)

    # context = {
    #     'title': f'{test.test_name} - Graded Needs Work', 
    #     'profile': profile, 
    #     'tests': Test.objects.all(),
    #     'prev_test': prev_test,
    #     'next_test': next_test,
    #     }
    # return render(request, 'main/test_score_needs_work.html', context=context)


def test_move_up(request, test_id):
    test = Test.objects.filter(pk=test_id).first()

    # prev_test: The test in the previous row of the table, right below the selected test in the table.
    prev_test = Test.objects.filter(test_order=test.test_order-1).first()
    selected_test_order  = test.test_order

    test.test_order = prev_test.test_order
    prev_test.test_order = selected_test_order

    test.save()
    prev_test.save()

    return redirect('tests')

def test_move_down(request, test_id):
    test = Test.objects.filter(pk=test_id).first()

    # next_test: The test in the next row of the table, right below the selected test in the table.
    next_test = Test.objects.filter(test_order=test.test_order+1).first()
    selected_test_order  = test.test_order

    test.test_order = next_test.test_order
    next_test.test_order = selected_test_order

    test.save()
    next_test.save()

    return redirect('tests')

def import_all_tests(request):
    csv_file = request.FILES['csv_file'] # The uploaded file.

    # Create a new 'export.csv' file based on the data in the file that the user uploaded.
    with open('export_tests.csv', 'wb+') as file:
        file.write(csv_file.read())

    with open('export_tests.csv', 'r+') as file:
        reader = pandas.read_csv(file) # Read CSV file with the Pandas library.

        for test_name, test_directions, test_repeat_due, test_order, test_category in zip(
            reader['test_name'], 
            reader['test_directions'], 
            reader['test_repeat_due'], 
            reader['test_order'], 
            reader['category']):

            category = Category.objects.filter(category_name=str(test_category)).first()
            
            test = Test.objects.create(
                test_name = test_name,
                test_directions = test_directions,
                test_repeat_due = test_repeat_due, 
                test_order = test_order,
                category = category,
                    )
            test.save()

    return redirect('home')

def export_all_tests(request):
    queryset = Test.objects.all()

    opts = queryset.model._meta
    write_to_file(str(opts))
    model = queryset.model
    response = HttpResponse(content_type='text/csv')
    # force download.
    response['Content-Disposition'] = 'attachment;filename=export_tests.csv'
    # the csv writer
    writer = csv.writer(response)
    field_names = [field.name for field in opts.fields]
    # Write a first row with header information
    writer.writerow(field_names)
    # Write data rows
    for obj in queryset:
        writer.writerow([getattr(obj, field) for field in field_names])

    return response