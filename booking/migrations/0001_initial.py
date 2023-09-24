# Generated by Django 3.2.21 on 2023-09-23 18:15

import booking.models
import datetime
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import vendor.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ad', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Data de criação')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Data de atualização')),
                ('code', models.CharField(default=booking.models.random_string, editable=False, max_length=16, primary_key=True, serialize=False, verbose_name='código do Booking')),
                ('check_in', models.DateField(default=datetime.date.today, validators=[vendor.validators.not_date_past], verbose_name='CheckIn')),
                ('check_out', models.DateField(default=datetime.date.today, validators=[vendor.validators.not_date_past], verbose_name='CheckOut')),
                ('total_price', models.FloatField(default=0.0, editable=False, verbose_name='Preço total')),
                ('comment', models.TextField(null=True, verbose_name='Comentário')),
                ('number_guests', models.IntegerField(default=1, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(1)], verbose_name='Número de hóspedes')),
                ('ad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ad.ads', verbose_name='Anúncio')),
            ],
            options={
                'verbose_name': 'booking',
                'verbose_name_plural': 'booking',
                'ordering': ['code', 'check_in', 'check_out', 'ad', 'number_guests', 'total_price'],
            },
        ),
    ]