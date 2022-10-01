# Generated by Django 4.0.4 on 2022-10-01 21:43

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProductsDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(blank=True, max_length=255, null=True)),
                ('url', models.CharField(max_length=2048, null=True)),
                ('image_url', models.CharField(max_length=2048, null=True)),
                ('cost', models.FloatField(blank=True, default=0.0, null=True)),
                ('shipping_price', models.FloatField(blank=True, default=0.0, null=True)),
                ('total_price', models.FloatField(blank=True, default=0.0, null=True)),
                ('shipping_method', models.CharField(blank=True, max_length=20, null=True)),
                ('shipping_speed', models.CharField(blank=True, max_length=255, null=True)),
                ('arrive_by', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
