from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .forms import ImportDataForm


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






