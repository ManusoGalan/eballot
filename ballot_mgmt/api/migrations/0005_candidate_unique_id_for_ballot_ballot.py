# Generated by Django 4.0 on 2022-08-20 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_candidate_id_for_ballot'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='candidate',
            constraint=models.UniqueConstraint(fields=('id_for_ballot', 'ballot_parent'), name='unique_id_for_ballot_ballot'),
        ),
    ]
