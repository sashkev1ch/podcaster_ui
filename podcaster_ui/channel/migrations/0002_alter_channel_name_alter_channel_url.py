# Generated by Django 5.1.1 on 2024-10-05 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("channel", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="channel",
            name="name",
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name="channel",
            name="url",
            field=models.CharField(max_length=200, unique=True),
        ),
    ]