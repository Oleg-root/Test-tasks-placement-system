# Generated by Django 3.2 on 2021-05-05 20:13

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('test_app', '0004_alter_solution_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solution',
            name='file',
            field=models.FileField(default='NULL', upload_to='solutions'),
        ),
        migrations.AlterField(
            model_name='solution',
            name='receiver',
            field=models.CharField(max_length=100, verbose_name=django.contrib.auth.models.User),
        ),
    ]
