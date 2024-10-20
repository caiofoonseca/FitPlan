# Generated by Django 5.1.1 on 2024-10-20 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_fitplan', '0002_progresso_delete_medida'),
    ]

    operations = [
        migrations.CreateModel(
            name='Medida',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('peso', models.FloatField()),
                ('altura', models.FloatField()),
                ('cintura', models.FloatField()),
                ('quadril', models.FloatField()),
                ('data', models.DateField()),
            ],
        ),
    ]
