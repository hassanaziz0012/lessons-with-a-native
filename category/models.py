from django.db import models

# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=100)
    taking_category_test_bool = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.category_name}"

    def __repr__(self) -> str:
        return f"<{self.category_name}>"