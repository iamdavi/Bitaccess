# Generated by Django 2.1.5 on 2019-01-28 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0006_auto_20190128_1859'),
    ]

    operations = [
        migrations.AlterField(
            model_name='zona',
            name='num_zona',
            field=models.IntegerField(blank=True, help_text='Numero de aula (identificador).', null=True, unique=True),
        ),
    ]
