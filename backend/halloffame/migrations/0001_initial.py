# Generated by Django 2.1.7 on 2019-04-03 12:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Guild',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='Hero',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hit_points', models.PositiveIntegerField(default=100)),
                ('level', models.PositiveIntegerField(default=1)),
                ('exp', models.PositiveIntegerField(default=0)),
                ('atk_points', models.IntegerField(default=1)),
                ('def_points', models.PositiveIntegerField(default=1)),
                ('is_alive', models.BooleanField(default=True)),
                ('guild', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='halloffame.Guild')),
            ],
        ),
        migrations.CreateModel(
            name='Race',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('can_fight_with', models.ManyToManyField(blank=True, related_name='can_fight', to='halloffame.Race')),
            ],
        ),
        migrations.AddField(
            model_name='hero',
            name='race',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.SET_DEFAULT, to='halloffame.Race'),
        ),
        migrations.AddField(
            model_name='hero',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
