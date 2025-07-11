# Generated by Django 5.2 on 2025-06-27 03:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokedex', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pokemon',
            name='pkmn_sprite',
            field=models.ImageField(blank=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='pokemon',
            name='pkmn_sprite_shiny',
            field=models.ImageField(blank=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='pokemon',
            name='pkmn_height',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='pokemon',
            name='pkmn_weight',
            field=models.IntegerField(),
        ),
    ]
