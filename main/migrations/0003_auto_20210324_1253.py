# Generated by Django 3.1.7 on 2021-03-24 07:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20210324_1236'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='test',
            name='category',
        ),
        migrations.RemoveField(
            model_name='test',
            name='test_status_due',
        ),
        migrations.RemoveField(
            model_name='test',
            name='test_status_good',
        ),
        migrations.RemoveField(
            model_name='test',
            name='test_status_new',
        ),
        migrations.RemoveField(
            model_name='test',
            name='test_status_repeat',
        ),
    ]