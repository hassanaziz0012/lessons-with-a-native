from django.db import models
from users.models import StudentProfile
from category.models import Category


# Create your models here.
class Test(models.Model):
    test_name = models.CharField(max_length=100)
    test_directions = models.TextField(null=True)

    test_status_new = models.ManyToManyField(StudentProfile, related_name='test_status_new')
    test_status_good = models.ManyToManyField(StudentProfile, related_name='test_status_good', blank=True)

    test_status_repeat = models.ManyToManyField(StudentProfile, related_name='test_status_repeat', blank=True)
    test_repeat_due = models.IntegerField(default=6)

    test_status_due = models.ManyToManyField(StudentProfile, related_name='test_status_due', blank=True)

    test_order = models.IntegerField(default=0)

    supporting_material = models.CharField(max_length=500, null=True, blank=True)

    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.test_name}"

    def __repr__(self) -> str:
        return f"<{self.test_name}>"