# Generated by Django 3.2.7 on 2023-06-13 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=127, verbose_name='название проекта')),
                ('mail', models.EmailField(max_length=254, unique=True, verbose_name='почта')),
                ('message', models.TextField(verbose_name='сообщение')),
            ],
        ),
        migrations.AlterModelOptions(
            name='project',
            options={'verbose_name': 'Проект', 'verbose_name_plural': 'Проекты'},
        ),
        migrations.AlterField(
            model_name='project',
            name='is_aproved',
            field=models.BooleanField(default=False, verbose_name='отображаеть на сайте или нет'),
        ),
    ]
