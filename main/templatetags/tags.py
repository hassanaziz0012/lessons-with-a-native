from django import template

register = template.Library()

@register.simple_tag(name='filter_questions_per_test')
def filter_questions_per_test(questions, test_id):
    questions_per_test = questions.filter(test=test_id)
    length_of_questions = len(questions_per_test)
    
    return length_of_questions
