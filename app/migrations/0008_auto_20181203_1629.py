# Generated by Django 2.1.3 on 2018-12-03 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_blogarticle'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogarticle',
            name='audio_amount',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='blogarticle',
            name='img_amount',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='blogarticle',
            name='publish_date',
            field=models.DateTimeField(default='2018-12-03 16:29:48'),
        ),
        migrations.AlterField(
            model_name='blogarticle',
            name='video_amount',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='blogarticle',
            name='word_amount',
            field=models.IntegerField(default=0),
        ),
    ]