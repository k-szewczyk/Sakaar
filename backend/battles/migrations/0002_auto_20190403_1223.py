# Generated by Django 2.1.7 on 2019-04-03 12:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('battles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='battle',
            name='attendees',
            field=models.ManyToManyField(related_name='battles', to='halloffame.Hero'),
        ),
        migrations.AlterField(
            model_name='battle',
            name='looser',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='loosed_battles', to='halloffame.Hero'),
        ),
    ]