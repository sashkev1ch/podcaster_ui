# Generated by Django 5.1.1 on 2024-10-05 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("channel", "0002_alter_channel_name_alter_channel_url"),
    ]

    operations = [
        migrations.AlterField(
            model_name="channel",
            name="name",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
