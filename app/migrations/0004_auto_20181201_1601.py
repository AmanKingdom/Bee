# Generated by Django 2.1.3 on 2018-12-01 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20181201_1555'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogarticle',
            name='publish_date',
            field=models.DateTimeField(default='2018-12-01 16:01:38'),
        ),
        migrations.AlterField(
            model_name='carousel',
            name='number',
            field=models.IntegerField(default=0),
        ),
    ]