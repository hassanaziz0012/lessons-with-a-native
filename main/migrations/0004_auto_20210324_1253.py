# Generated by Django 3.1.7 on 2021-03-24 07:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0001_initial'),
        ('main', '0003_auto_20210324_1253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='test',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tests.test'),
        ),
        migrations.DeleteModel(
            name='Test',
        ),
    ]
