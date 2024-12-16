# Generated by Django 4.2 on 2024-11-09 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_channelsubmission_problem_statement_comment_author_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roomrequestjoin',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected'), ('removed', 'Removed')], default='pending', max_length=10),
        ),
    ]
