# Generated by Django 3.2 on 2021-05-09 22:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_app', '0017_response'),
    ]

    operations = [
        migrations.AddField(
            model_name='solution',
            name='responded',
            field=models.BooleanField(default=False),
        ),
    ]