# Generated by Django 5.0 on 2024-02-14 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="audioresource",
            name="date_created",
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
