# Generated by Django 3.2.9 on 2022-01-12 04:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CST_SPMS', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposals',
            name='status',
            field=models.TextField(default='', null=True),
        ),
    ]
