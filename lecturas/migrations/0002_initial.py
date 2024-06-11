# Generated by Django 5.0.3 on 2024-04-13 01:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('lecturas', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Barrio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('barrio', models.CharField(max_length=20, verbose_name='Nombre del Barrio')),
                ('zona', models.CharField(choices=[('zona1', 'Norte'), ('zona2', 'Sur occidente'), ('zona3', 'En expansion')], max_length=50, null=True, verbose_name='zona  ')),
            ],
            options={
                'verbose_name': 'Barrio',
                'verbose_name_plural': 'Barrios',
            },
        ),
        migrations.CreateModel(
            name='Micromedidor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nuid', models.CharField(max_length=20, verbose_name='NUID')),
                ('medidor', models.CharField(max_length=20, verbose_name='Medidor')),
                ('fecha_instalacion', models.DateField(verbose_name='Fecha de Instalación')),
            ],
            options={
                'verbose_name': 'Micromedidor',
                'verbose_name_plural': 'Micromedidores',
            },
        ),
        migrations.CreateModel(
            name='Suscriptor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('primer_nombre', models.CharField(max_length=50, verbose_name='Primer Nombre')),
                ('segundo_nombre', models.CharField(max_length=59, verbose_name='Segundo Nombre')),
                ('primer_apellido', models.CharField(max_length=50, verbose_name='Primer Apellido')),
                ('segundo_apellido', models.CharField(max_length=50, verbose_name='Segundo Apellido')),
                ('direccion_IMAGEN', models.ImageField(upload_to='imagenes/', verbose_name='Dirección Imagen')),
                ('Estrato_socioeconomico', models.CharField(choices=[('Estrato1', 'Bajo Bajo'), ('Estrato2', 'Bajo'), ('Estrato3', 'Medio Bajo'), ('Estrato4', 'Medio ')], max_length=50, null=True, verbose_name='estrato socioeconimico  ')),
                ('Uso', models.CharField(choices=[('Uso1', 'Comercial'), ('Uso2', 'Residencial'), ('Uso3', 'Oficial')], max_length=50, null=True, verbose_name='Uso  ')),
                ('barrio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lecturas.barrio', verbose_name='Barrio')),
            ],
            options={
                'verbose_name': 'Suscriptor',
                'verbose_name_plural': 'Suscriptores',
            },
        ),
        migrations.CreateModel(
            name='SuscriptorMicromedidor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('micromedidor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lecturas.micromedidor', verbose_name='Micromedidor')),
                ('suscriptor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lecturas.suscriptor', verbose_name='Suscriptor')),
            ],
            options={
                'verbose_name': 'Relación Suscriptor-Micromedidor',
                'verbose_name_plural': 'Relaciones Suscriptor-Micromedidor',
            },
        ),
        migrations.CreateModel(
            name='Lectura',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registro_consumo', models.IntegerField(verbose_name='Registro de Consumo')),
                ('FechaLectura', models.DateTimeField(verbose_name='Fecha de Lectura')),
                ('Observaciones', models.CharField(max_length=100, verbose_name='Observaciones')),
                ('tipo_lectura', models.CharField(choices=[('tipo1', 'Lectura'), ('tipo2', 'Promedio')], max_length=50, null=True, verbose_name='')),
                ('estado_micromedidor', models.CharField(choices=[('estado1', 'Bueno'), ('estado2', 'Malo')], max_length=50, null=True, verbose_name='estado del micromedidor')),
                ('Mes_lectura', models.CharField(choices=[('mes1', 'Enero'), ('mes2', 'Febrero'), ('mes2', 'Marzo'), ('mes2', 'Abril'), ('mes2', 'Mayo'), ('mes2', 'Junio'), ('mes2', 'Julio'), ('mes2', 'Agosto'), ('mes2', 'Septiembre'), ('mes2', 'Octubre'), ('mes2', 'Noviembre'), ('mes2', 'Diciembre')], max_length=50, null=True, verbose_name='mes de lectura')),
                ('suscriptor_micromedidor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lecturas.suscriptormicromedidor', verbose_name='Relación Suscriptor-Micromedidor')),
            ],
            options={
                'verbose_name': 'Lectura',
                'verbose_name_plural': 'Lecturas',
            },
        ),
    ]
