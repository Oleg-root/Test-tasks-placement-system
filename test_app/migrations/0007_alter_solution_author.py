# Generated by Django 3.2 on 2021-05-05 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_app', '0006_alter_solution_receiver'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solution',
            name='author',
            field=models.CharField(max_length=100),
        ),
    ]