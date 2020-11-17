# Generated by Django 3.1.3 on 2020-11-18 00:10

import django.core.validators
from django.db import migrations, models
import re


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0005_auto_20201118_0006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='BookID',
            field=models.CharField(help_text='The format is one character and 2 to 9 digits', max_length=64, primary_key=True, serialize=False, validators=[django.core.validators.RegexValidator(regex=re.compile('[A-Z]\\d{2,9}'))]),
        ),
    ]
