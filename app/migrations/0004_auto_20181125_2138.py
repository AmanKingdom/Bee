# Generated by Django 2.1.2 on 2018-11-25 21:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20181125_2042'),
    ]

    operations = [
        migrations.CreateModel(
            name='Carousel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('alt', models.TextField(blank=True, null=True)),
                ('img_url', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.WeChatArticle')),
            ],
        ),
        migrations.AlterField(
            model_name='blogarticle',
            name='publish_date',
            field=models.DateTimeField(default='2018-11-25 21:37:59'),
        ),
    ]