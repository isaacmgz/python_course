# Generated by Django 5.2.3 on 2025-06-20 18:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bienvenida', '0002_owner_alter_mascota_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cita',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('time', models.TimeField(auto_now=True)),
                ('description', models.TextField()),
                ('mascota', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='citas', to='bienvenida.mascota')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='citas', to='bienvenida.owner')),
            ],
        ),
    ]
