from django.db import models

# Create your models here.
class Question(models.Model):
    test = models.ForeignKey('tests.Test', on_delete=models.CASCADE)
    
    question = models.CharField(max_length=200)
    answer = models.CharField(max_length=200)

    review_question = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'{self.question} - Test: {self.test}'

    def __repr__(self) -> str:
        return f'<{self.question} - {self.test}>'