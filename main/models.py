from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
class StudentProfile(models.Model):
    username = models.CharField(max_length=100, blank=False)
    email = models.EmailField()

    avg_score = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f'{self.username} - Student Profile'
    
    def __repr__(self) -> str:
        return f'<StudentProfile: {self.username} - {self.email}>'

class Test(models.Model):
    test_name = models.CharField(max_length=100)

class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)

    question = models.CharField(max_length=200)
    answer = models.CharField(max_length=200)

    def __str__(self) -> str:
        return f'{self.question} - Test: {self.test}'

    def __repr__(self) -> str:
        return f'<{self.question} - {self.test}>'