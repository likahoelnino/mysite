# Generated by Django 3.1.2 on 2020-11-16 17:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0005_auto_20201116_1715'),
    ]

    operations = [
        migrations.RenameField(
            model_name='borrowrecord',
            old_name='username',
            new_name='Username',
        ),
        migrations.RenameField(
            model_name='reserve',
            old_name='username',
            new_name='Username',
        ),
    ]