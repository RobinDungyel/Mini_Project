# Generated by Django 5.0.4 on 2024-05-26 12:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('votingapp', '0002_alter_candidate_position'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='no_votes',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='candidate',
            name='yes_votes',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='position',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='votingapp.position'),
        ),
    ]
