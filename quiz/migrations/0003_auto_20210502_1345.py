# Generated by Django 3.2 on 2021-05-02 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0002_auto_20210502_1105'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='level',
            field=models.CharField(default='Easy', max_length=50),
        ),
        migrations.AddField(
            model_name='question',
            name='score',
            field=models.IntegerField(default=10),
        ),
    ]
