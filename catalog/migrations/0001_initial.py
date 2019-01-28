# Generated by Django 2.1.5 on 2019-01-28 11:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Empleados',
            fields=[
                ('rfid', models.CharField(help_text='Introduce el RFID del empleado', max_length=30, primary_key=True, serialize=False)),
                ('dentro', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['user', 'rfid'],
            },
        ),
        migrations.CreateModel(
            name='PermisosAula',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grupo', models.ForeignKey(help_text='Grupo al que quieres dar permiso.', on_delete=django.db.models.deletion.DO_NOTHING, to='auth.Group')),
            ],
        ),
        migrations.CreateModel(
            name='PermisosPuerto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grupo', models.ForeignKey(help_text='Grupo al que quieres dar permiso.', on_delete=django.db.models.deletion.DO_NOTHING, to='auth.Group')),
            ],
        ),
        migrations.CreateModel(
            name='Puerto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_puerto', models.IntegerField(help_text='Número de puerto del arduino')),
                ('descripcion', models.CharField(help_text='Acción que realiza dicho puerto', max_length=35)),
            ],
            options={
                'ordering': ['ip', 'num_puerto'],
            },
        ),
        migrations.CreateModel(
            name='RegistroAula',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=30)),
                ('f_entrada', models.DateTimeField(auto_now_add=True)),
                ('f_salida', models.DateTimeField(auto_now=True)),
                ('dentro', models.BooleanField(default=False)),
                ('rfid', models.ForeignKey(max_length=30, on_delete=django.db.models.deletion.DO_NOTHING, to='catalog.Empleados')),
            ],
            options={
                'ordering': ['rfid', 'ip'],
            },
        ),
        migrations.CreateModel(
            name='Zona',
            fields=[
                ('num_aula', models.IntegerField(blank=True, help_text='Numero de aula (identificador).', null=True)),
                ('ip', models.CharField(help_text='Ip del dispositivo asociado a esta aula', max_length=25, primary_key=True, serialize=False)),
                ('modelo', models.CharField(help_text='Introduce el modelo del arduino (p. ej. Uno, Mega, etc.)', max_length=25)),
                ('tipo', models.CharField(blank=True, help_text='Tipo de aula (p. ej. Clase, C.P.D...)', max_length=25, null=True)),
                ('descripcion', models.TextField(help_text='Introduce una descripción de la zona.', max_length=1000)),
            ],
            options={
                'ordering': ['num_aula', 'ip'],
            },
        ),
        migrations.AddField(
            model_name='puerto',
            name='ip',
            field=models.ForeignKey(help_text='Ip de la zona', on_delete=django.db.models.deletion.CASCADE, to='catalog.Zona'),
        ),
        migrations.AddField(
            model_name='permisospuerto',
            name='puerto',
            field=models.ForeignKey(help_text='Puerto al que tiene permiso.', on_delete=django.db.models.deletion.DO_NOTHING, to='catalog.Puerto'),
        ),
        migrations.AddField(
            model_name='permisosaula',
            name='zona',
            field=models.ForeignKey(help_text='Zona a la que tiene acceso el grupo.', on_delete=django.db.models.deletion.DO_NOTHING, to='catalog.Zona'),
        ),
        migrations.AlterUniqueTogether(
            name='puerto',
            unique_together={('ip', 'num_puerto')},
        ),
    ]
