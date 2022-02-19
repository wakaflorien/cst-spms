# Generated by Django 3.2.9 on 2022-01-12 15:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CST_SPMS', '0002_proposals_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='supervisors',
            name='group',
        ),
        migrations.AddField(
            model_name='studentgroups',
            name='supervisor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='CST_SPMS.supervisors'),
        ),
    ]