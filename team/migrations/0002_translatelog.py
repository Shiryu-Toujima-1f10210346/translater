# Generated by Django 4.0.4 on 2022-05-19 14:58

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Translatelog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=100)),
                ('user_id', models.CharField(max_length=100)),
                ('origin_text', models.TextField()),
                ('deepl_text', models.TextField()),
                ('source_lang', models.CharField(max_length=20)),
                ('target_lang', models.CharField(max_length=20)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
