from django.shortcuts import render

# Create your views here.
from django.shortcuts import redirect, render
from django.contrib import messages

from .forms import (AddQuestionForm, StudentProfileForm, UpdateStudentProfileForm, CreateTestForm, 
    UpdateTestForm)
from .models import StudentProfile, Test, Question


# Create your views here.
def home(request):
    context = {
        'title': 'Home',
    }
    return render(request, 'main/home.html', context=context)

def about(request):
    context = {
        'title': 'About'
    }
    return render(request, 'main/about.html', context=context)
    
def create_profile(request):
    '''Create a Student Profile.'''
    if request.method == 'POST':
        form = StudentProfileForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            messages.success(request, f'A new student profile was created for {username}.', extra_tags='alert alert success')
            return redirect('home')
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
    tests = Test.objects.all()

    if request.method == 'POST':
        c_form = CreateTestForm(request.POST)
        u_form = UpdateTestForm(request.POST)

        if c_form.is_valid():
            c_form.save()
            messages.success(request, 'This test has been created.', extra_tags='alert alert-primary')

            return redirect('tests')

        # if u_form.is_valid():
        #     u_form.save(commit=False)
        #     messages.success(request, 'This test has been updated.', extra_tags='alert alert-primary')
    else:
        c_form = CreateTestForm()
        u_form = UpdateTestForm()

    context = {
        'title': 'Tests',
        'tests': tests,
        'form': c_form,
        'u_form': u_form,
    }
    return render(request, 'main/tests.html', context=context)

def create_test(request):
    context = {
        'title': 'Create Test'
    }

    return redirect('tests')

def test(request, test_id):
    test = Test.objects.filter(pk=test_id).first()
    questions = Question.objects.filter(test=test)
    
    if request.method == 'POST':
        form = AddQuestionForm(request.POST)
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

    context = {
        'title': test.test_name,
        'test': test,
        'questions': questions,
        'form': form,
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
        test.test_name = request.POST['test_name']
        test.save()

        messages.success(request, 'The test was successfully updated.', extra_tags='alert alert-success')
        return redirect('tests')
    else:
        messages.error(request, "It didn't work", extra_tags='alert alert-danger')
        return redirect('tests')

