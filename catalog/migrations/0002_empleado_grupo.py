# Generated by Django 2.1.5 on 2019-02-06 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='empleado',
            name='grupo',
            field=models.ManyToManyField(to='auth.Group'),
        ),
    ]