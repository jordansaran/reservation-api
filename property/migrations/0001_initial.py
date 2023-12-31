# Generated by Django 3.2.21 on 2023-09-23 18:14

import datetime
import django.core.validators
from django.db import migrations, models
import uuid
import vendor.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Property',
            fields=[
                ('uuid', models.CharField(default=uuid.uuid4, editable=False, max_length=36, primary_key=True, serialize=False, verbose_name='uuid')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Data de criação')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Data de atualização')),
                ('guest_limit', models.SmallIntegerField(default=1, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(1)], verbose_name='Limite de hóspedes')),
                ('number_bathrooms', models.SmallIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(0)], verbose_name='Quantidade de banheiros')),
                ('pets_allowed', models.BooleanField(default=False, verbose_name='Animais de estimação é permitido?')),
                ('cleaning_cost', models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0.0)], verbose_name='Valor da limpeza')),
                ('activation_date', models.DateField(default=datetime.date.today, validators=[vendor.validators.not_date_past], verbose_name='Data de ativação do imóvel')),
            ],
            options={
                'verbose_name': 'property',
                'verbose_name_plural': 'properties',
                'ordering': ['activation_date', 'guest_limit', 'pets_allowed', 'cleaning_cost'],
            },
        ),
    ]
