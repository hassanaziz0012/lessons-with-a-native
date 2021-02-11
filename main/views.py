from django.shortcuts import render

# Create your views here.
from django.shortcuts import redirect, render
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import HttpResponse

from .forms import (AddQuestionForm, StudentProfileForm, UpdateStudentProfileForm, CreateTestForm,
    UpdateTestForm, UpdateQuestionForm, EmailStudentForm, ImportDataForm, CreateCategoryForm, UpdateCategoryForm)
from .models import EmailPreset, StudentProfile, Test, Question, Category

from email.message import EmailMessage
import smtplib
import csv
import pandas

def write_to_file(content):
    '''Used mostly for debugging purposes.

    We write some data to a text file to see what that data contains. Using print() statements could work
    as well, but is not very neat, especially when you consider how cluttered the Terminal gets when the
    Django server is running.
    '''
    with open('sample_log.txt', 'a') as file:
        file.write(content)


# Create your views here.
def home(request):
    if request.method == 'POST':
        tests_form = ImportDataForm(request.POST, request.FILES)
        questions_form = ImportDataForm(request.POST, request.FILES)

        if tests_form.is_valid():
            tests_form.save(commit=False)
        
        if questions_form.is_valid():
            questions_form.save(commit=False)

    else:
        tests_form = ImportDataForm()
        questions_form = ImportDataForm()

    context = {
        'title': 'Home',
        'tests_form': tests_form,
        'questions_form': questions_form
    }
    return render(request, 'main/home.html', context=context)

def about(request):
    context = {
        'title': 'About'
    }
    return render(request, 'main/about.html', context=context)

def create_profile(request):
    '''Create a Student Profile.'''
    tests = Test.objects.all()
    if request.method == 'POST':
        form = StudentProfileForm(request.POST)
        if form.is_valid():
            form.save(commit=False)

            username = form.cleaned_data['username']
            email = form.cleaned_data['email']

            profile = StudentProfile.objects.create(username=username, email=email)
            profile.save()

            for test in tests:
                test.test_status_new.add(profile)
                test.save()

            messages.success(request, f'A new student profile was created for {username}.', extra_tags='alert alert-success')
            return redirect('manage-profile')
    else:
        form = StudentProfileForm()

    context = {
        'title': 'Create Student Profile',
        'form': form,
    }
    return render(request, 'main/create_profile.html', context=context)

def manage_profile(request):
    '''Manage your student profiles.'''
    context = {
        'title': 'Create Student Profile',
        'profiles': StudentProfile.objects.all(),
    }
    return render(request, 'main/manage_profile.html', context=context)

def update_profile(request, profile_id):
    profile = StudentProfile.objects.filter(pk=profile_id).first()

    if request.method == 'POST':
        form = UpdateStudentProfileForm(request.POST, initial={'username': profile.username, 'email': profile.email})
        if form.is_valid():
            profile.username = form.cleaned_data['username']
            profile.email = form.cleaned_data['email']
            profile.save()

            messages.success(request, 'This profile has been updated!')
            return redirect('manage-profile')
    else:
        form = UpdateStudentProfileForm(initial={'username': profile.username, 'email': profile.email})

    context = {
        'title': 'Update Profile',
        'form': form,
    }
    return render(request, 'main/update_profile.html', context=context)

def delete_profile(request, profile_id):
    profile = StudentProfile.objects.filter(pk=profile_id).first()
    context = {
        'title': 'Update Profile',
        'profile': profile,
    }
    profile.delete()
    return render(request, 'main/delete_profile.html', context=context)


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
                profile.test_status_new.add(test)
                profile.save()

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

def update_question(request, test_id, question_id):
    question = Question.objects.filter(pk=question_id).first()
    if request.method == 'POST':
        form = UpdateQuestionForm(request.POST)
        if form.is_valid():
            form.save(commit=False)

            # Update values.
            # If statements, to check if the user entered a new value. Otherwise, it is set to an empty string and we don't want that. So we avoid it.
            if request.POST['question']:
                question.question = form.cleaned_data['question']
            if request.POST['answer']:
                question.answer = form.cleaned_data['answer']

            question.save() # Save changes.

            return redirect('test', test_id)
    else:
        form = UpdateQuestionForm()

    context = {
        'title': 'Update Question',
        'form': form,
    }
    return render(request, 'main/update_question.html', context=context)


def delete_question(request, test_id, question_id):
    question = Question.objects.filter(pk=question_id).first()
    question.delete()

    messages.success(request, 'That question was deleted!', extra_tags='alert alert-success')
    return redirect('test', test_id)

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
    }
    return render(request, 'main/take_test.html', context=context)

def profile(request, profile_username):
    profile = StudentProfile.objects.filter(username=profile_username).first()

    tests = Test.objects.all()
    questions = Question.objects.all()
    categories = Category.objects.all()

    context = {
        'title': profile.username + ' - Profile',
        'profile': profile,
        'tests': tests,
        'questions': questions,
        'categories': categories,
    }
    return render(request, 'main/profile.html', context=context)


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

def save_email_preset(request, test_id):
    test = Test.objects.filter(pk=test_id).first()
        
    recipient = request.POST.get('recipient')
    subject = request.POST.get('subject')
    body = request.POST.get('body')

    preset = EmailPreset(recipient=recipient, subject=subject, body=body)
    preset.save()

    return redirect('test', test_id)

def send_student_email(request, test_id, preset_id):
    preset = EmailPreset.objects.filter(pk=preset_id).first()
    message = EmailMessage()

    message['From'] = 'lessonswithanative@gmail.com'
    message['To'] = preset.recipient
    message['Subject'] = preset.subject
    message.set_content(preset.body)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login('lessonswithanative@gmail.com', 'Noki@7250i')
        smtp.send_message(message)

    return redirect('test', test_id)

def add_to_review(request, profile_id, question_id,  category_id):
    question = Question.objects.filter(pk=question_id).first()
    question.review_question = True
    question.save()

    return redirect('take-category-test', category_id, profile_id)

def remove_from_review(request, question_id, profile_id, category_id):
    question = Question.objects.filter(pk=question_id).first()
    question.review_question = False
    question.save()

    return redirect('take-category-test', category_id, profile_id)

def import_all_tests(request):
    csv_file = request.FILES['csv_file'] # The uploaded file.

    # Create a new 'export.csv' file based on the data in the file that the user uploaded.
    with open('export_tests.csv', 'wb+') as file:
        file.write(csv_file.read())

    with open('export_tests.csv', 'r+') as file:
        reader = pandas.read_csv(file) # Read CSV file with the Pandas library.

        for test_name, test_directions, test_repeat_due, test_order in zip(reader['test_name'], reader['test_directions'], reader['test_repeat_due'], reader['test_order']):
            test = Test.objects.create(
                test_name = test_name,
                test_directions = test_directions,
                test_repeat_due = test_repeat_due, 
                test_order = test_order,
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

def import_all_questions(request):
    csv_file = request.FILES['csv_file'] # The uploaded file.

    # Create a new 'export.csv' file based on the data in the file that the user uploaded.
    with open('export_questions.csv', 'wb+') as file:
        file.write(csv_file.read())

    with open('export_questions.csv', 'r+') as file:
        reader = pandas.read_csv(file) # Read CSV file with the Pandas library.

        for test_name, question, answer, review_question in zip(reader['test'], reader['question'], reader['answer'], reader['review_question']):
            test = Test.objects.filter(test_name=test_name).first()
            question = Question.objects.create(
                test=test,
                question=question,
                answer=answer,
                review_question=review_question,
            )
            question.save()
    
    return redirect('home')

def export_all_questions(request):
    queryset = Question.objects.all()

    opts = queryset.model._meta
    write_to_file(str(opts))
    model = queryset.model
    response = HttpResponse(content_type='text/csv')
    # force download.
    response['Content-Disposition'] = 'attachment;filename=export_questions.csv'
    # the csv writer
    writer = csv.writer(response)
    field_names = [field.name for field in opts.fields]
    # Write a first row with header information
    writer.writerow(field_names)
    # Write data rows
    for obj in queryset:
        writer.writerow([getattr(obj, field) for field in field_names])

    return response


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
    }
    return render(request, 'main/take_category_test.html', context=context)


