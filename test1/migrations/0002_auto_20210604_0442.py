# Generated by Django 3.2.4 on 2021-06-03 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test1', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='state',
            name='session_no',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='users',
            name='user_id',
            field=models.IntegerField(),
        ),
    ]
