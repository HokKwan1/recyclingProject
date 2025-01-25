# Generated by Django 4.2.17 on 2025-01-20 23:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=256)),
                ('last_name', models.CharField(max_length=256)),
                ('email', models.CharField(max_length=256)),
                ('phone', models.CharField(max_length=20)),
                ('address', models.CharField(max_length=256)),
                ('city', models.CharField(max_length=64)),
                ('state', models.CharField(max_length=64)),
                ('country', models.CharField(max_length=64)),
                ('postal_code', models.CharField(max_length=64)),
                ('status', models.CharField(max_length=32)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_completed', models.DateTimeField(blank=True, null=True)),
                ('token', models.CharField(max_length=512)),
                ('claimed_by', models.CharField(blank=True, max_length=12, null=True)),
            ],
        ),
    ]
