# Generated by Django 3.1.1 on 2021-01-22 17:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentprofile',
            name='test_status_good',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='test_status_good', to='main.test'),
        ),
        migrations.AddField(
            model_name='studentprofile',
            name='test_status_new',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='test_status_new', to='main.test'),
        ),
        migrations.AddField(
            model_name='studentprofile',
            name='test_status_repeat',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='test_status_repeat', to='main.test'),
        ),
    ]
