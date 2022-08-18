# Generated by Django 4.0 on 2022-08-10 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ballotbox',
            name='contractAddress',
            field=models.CharField(blank=True, max_length=44, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='ballotbox',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='motto',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='website',
            field=models.URLField(blank=True, null=True),
        ),
    ]
