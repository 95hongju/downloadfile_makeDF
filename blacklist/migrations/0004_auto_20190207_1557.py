# Generated by Django 2.1.3 on 2019-02-07 23:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blacklist', '0003_auto_20190206_1612'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blacks',
            name='rsid',
            field=models.CharField(default='N/A', max_length=30),
        ),
    ]
