# Generated by Django 4.2.2 on 2023-08-07 20:46

import administracion.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Carrera',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('duracion', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Materia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('dia', models.CharField(max_length=12)),
                ('desde', models.TimeField()),
                ('hasta', models.TimeField()),
                ('carrera', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administracion.carrera')),
                ('docente', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Nota',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nota', models.FloatField()),
                ('tipo', models.CharField(max_length=20)),
                ('dia', models.DateField()),
                ('observacion', models.TextField()),
                ('alumno', models.ForeignKey(blank=True, null=True, on_delete=models.SET(administracion.models.usuario_alumno), to=settings.AUTH_USER_MODEL)),
                ('materia', models.ForeignKey(blank=True, null=True, on_delete=models.SET(administracion.models.nombre_materia), to='administracion.materia')),
            ],
        ),
        migrations.CreateModel(
            name='Correlativa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('correlativa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Materia_correlativa', to='administracion.materia')),
                ('materia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Materia_materia', to='administracion.materia')),
            ],
        ),
        migrations.CreateModel(
            name='Alumno_Materia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.CharField(max_length=50)),
                ('estudiante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('materia', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='administracion.materia')),
            ],
        ),
        migrations.CreateModel(
            name='Alumno_Carrera',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('carrera', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='administracion.carrera')),
                ('estudiante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='customuser',
            name='carreras',
            field=models.ManyToManyField(through='administracion.Alumno_Carrera', to='administracion.carrera'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='materias',
            field=models.ManyToManyField(through='administracion.Alumno_Materia', to='administracion.materia'),
        ),
    ]
