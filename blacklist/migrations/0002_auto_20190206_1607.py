# Generated by Django 2.1.3 on 2019-02-07 00:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blacklist', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blacks',
            name='rsid',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
