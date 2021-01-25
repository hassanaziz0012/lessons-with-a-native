# Generated by Django 3.1.1 on 2021-01-25 14:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0022_test_supporting_material'),
    ]

    operations = [
        migrations.AddField(
            model_name='test',
            name='review_questions',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='review_questions', to='main.question'),
        ),
    ]