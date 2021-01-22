from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
class Test(models.Model):
    test_name = models.CharField(max_length=100)

    test_status_new = models.ManyToManyField('StudentProfile', related_name='test_status_new')
    test_status_good = models.ManyToManyField('StudentProfile', related_name='test_status_good')

    test_status_repeat = models.ManyToManyField('StudentProfile', related_name='test_status_repeat')
    test_repeat_due = models.IntegerField(default=6)

    test_status_due = models.BooleanField(default=False)

class StudentProfile(models.Model):
    username = models.CharField(max_length=100, blank=False)
    email = models.EmailField()
    
    avg_score = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f'{self.username} - Student Profile'
    
    def __repr__(self) -> str:
        return f'<StudentProfile: {self.username} - {self.email}>'


class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    
    question = models.CharField(max_length=200)
    answer = models.CharField(max_length=200)

    def __str__(self) -> str:
        return f'{self.question} - Test: {self.test}'

    def __repr__(self) -> str:
        return f'<{self.question} - {self.test}>'