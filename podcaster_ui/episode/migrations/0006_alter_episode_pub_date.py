# Generated by Django 5.1.1 on 2024-09-30 08:28

import podcaster_ui.episode.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("episode", "0005_alter_episode_external_guid"),
    ]

    operations = [
        migrations.AlterField(
            model_name="episode",
            name="pub_date",
            field=podcaster_ui.episode.models.CustomDateTimeField(),
        ),
    ]
