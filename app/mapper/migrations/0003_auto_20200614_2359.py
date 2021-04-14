# Generated by Django 3.0.7 on 2020-06-14 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mapper', '0002_map_downloaded'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='difficulty',
            name='level',
        ),
        migrations.AddField(
            model_name='difficulty',
            name='code',
            field=models.IntegerField(choices=[(0, 'Easy'), (1, 'Normal'), (2, 'Hard'), (3, 'Expert'), (4, 'ExpertPlus')], default=0, verbose_name='難易度'),
        ),
        migrations.AddField(
            model_name='difficulty',
            name='speed',
            field=models.IntegerField(default=0, verbose_name='スピード'),
        ),
    ]
