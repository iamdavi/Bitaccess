# Generated by Django 2.1.5 on 2019-01-28 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_auto_20190128_1830'),
    ]

    operations = [
        migrations.AddField(
            model_name='zona',
            name='dentro',
            field=models.BooleanField(default=False),
        ),
    ]