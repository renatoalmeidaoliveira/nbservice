# Generated by Django 4.2.11 on 2024-03-18 10:44

from django.db import migrations
import taggit.managers


class Migration(migrations.Migration):
    dependencies = [
        ("extras", "0060_customlink_button_class"),
        (
            "nb_service",
            "0002_application_custom_field_data_ic_custom_field_data_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="service",
            name="tags",
            field=taggit.managers.TaggableManager(
                through="extras.TaggedItem", to="extras.Tag"
            ),
        ),
    ]
