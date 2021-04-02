from django.shortcuts import render, redirect
from email.message import EmailMessage
import smtplib
from django.contrib import messages
from .models import StudentProfile, EmailPreset
from .forms import StudentProfileForm, UpdateStudentProfileForm
from question.models import Question
from category.models import Category
from tests.models import Test


# Create your views here.
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