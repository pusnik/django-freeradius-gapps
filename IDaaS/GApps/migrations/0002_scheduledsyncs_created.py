# Generated by Django 2.0.2 on 2018-02-26 21:34

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('GApps', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='scheduledsyncs',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]