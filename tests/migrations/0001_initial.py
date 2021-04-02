# Generated by Django 3.1.7 on 2021-03-24 07:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        ('main', '0003_auto_20210324_1253'),
    ]

    operations = [
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test_name', models.CharField(max_length=100)),
                ('test_directions', models.TextField(null=True)),
                ('test_repeat_due', models.IntegerField(default=6)),
                ('test_order', models.IntegerField(default=0)),
                ('supporting_material', models.CharField(blank=True, max_length=500, null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.category')),
                ('test_status_due', models.ManyToManyField(blank=True, related_name='test_status_due', to='users.StudentProfile')),
                ('test_status_good', models.ManyToManyField(blank=True, related_name='test_status_good', to='users.StudentProfile')),
                ('test_status_new', models.ManyToManyField(related_name='test_status_new', to='users.StudentProfile')),
                ('test_status_repeat', models.ManyToManyField(blank=True, related_name='test_status_repeat', to='users.StudentProfile')),
            ],
        ),
    ]