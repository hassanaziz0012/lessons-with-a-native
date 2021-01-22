# Generated by Django 3.1.1 on 2021-01-22 18:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20210122_2313'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='test_status_good',
        ),
        migrations.RemoveField(
            model_name='question',
            name='test_status_new',
        ),
        migrations.RemoveField(
            model_name='question',
            name='test_status_repeat',
        ),
        migrations.AddField(
            model_name='test',
            name='test_status_good',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='test_status_good', to='main.studentprofile'),
        ),
        migrations.AddField(
            model_name='test',
            name='test_status_new',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='test_status_new', to='main.studentprofile'),
        ),
        migrations.AddField(
            model_name='test',
            name='test_status_repeat',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='test_status_repeat', to='main.studentprofile'),
        ),
    ]
