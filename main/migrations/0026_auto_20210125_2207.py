# Generated by Django 3.1.1 on 2021-01-25 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0025_reviewquestion'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='review_question',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='ReviewQuestion',
        ),
    ]