# Generated by Django 3.2.15 on 2022-10-24 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("product_stat_apis", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="role",
            field=models.CharField(
                choices=[("Admin", "Admin"), ("User", "User")], max_length=10
            ),
        ),
    ]
