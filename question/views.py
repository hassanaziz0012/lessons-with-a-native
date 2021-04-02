from django.shortcuts import render, redirect
from django.contrib import messages

from .models import Question
from .forms import UpdateQuestionForm
import pandas
import csv
from tests.models import Test
from question.models import Question
from django.http import HttpResponse
from main.views import write_to_file


# Create your views here.
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


def add_to_review(request, profile_id, question_id,  category_id, taking_individual_test):
    question = Question.objects.filter(pk=question_id).first()
    question.review_question = True
    question.save()

    test = question.test
    test_id = test.id
    
    if taking_individual_test == True:
        return redirect('take-test', test_id, profile_id)
    else:
        return redirect('take-category-test', category_id, profile_id)

def remove_from_review(request, question_id, profile_id, category_id, taking_individual_test):
    question = Question.objects.filter(pk=question_id).first()
    question.review_question = False
    question.save()
    
    test = question.test
    test_id = test.id

    if taking_individual_test == True:
        return redirect('take-test', test_id, profile_id)
    else:
        return redirect('take-category-test', category_id, profile_id)

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