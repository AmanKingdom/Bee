# Generated by Django 2.1.3 on 2018-12-01 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20181130_2050'),
    ]

    operations = [
        migrations.AddField(
            model_name='carousel',
            name='number',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='blogarticle',
            name='publish_date',
            field=models.DateTimeField(default='2018-12-01 15:55:28'),
        ),
    ]
