# Generated by Django 3.0.7 on 2020-06-14 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mapper', '0003_auto_20200614_2359'),
    ]

    operations = [
        migrations.AlterField(
            model_name='difficulty',
            name='code',
            field=models.IntegerField(choices=[(0, 'Easy'), (1, 'Normal'), (2, 'Hard'), (3, 'Expert'), (4, 'ExpertPlus')], verbose_name='難易度'),
        ),
        migrations.AlterField(
            model_name='difficulty',
            name='speed',
            field=models.IntegerField(verbose_name='スピード'),
        ),
    ]
