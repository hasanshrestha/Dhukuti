# Generated by Django 4.1.1 on 2022-10-16 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("PdfSearchApp", "0003_wordfile"),
    ]

    operations = [
        migrations.AddField(
            model_name="files",
            name="filetype",
            field=models.CharField(default="", max_length=50),
        ),
    ]