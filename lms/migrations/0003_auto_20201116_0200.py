# Generated by Django 3.1.2 on 2020-11-16 02:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0002_auto_20201116_0152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookinstance',
            name='BookID',
            field=models.ForeignKey(db_column='BookID', on_delete=django.db.models.deletion.PROTECT, to='lms.book'),
        ),
    ]