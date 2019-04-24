# Generated by Django 2.1.7 on 2019-04-24 09:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('halloffame', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Battle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_looser_dead', models.BooleanField(default=False)),
                ('date', models.DateTimeField()),
                ('attendees', models.ManyToManyField(related_name='battles', to='halloffame.Hero')),
                ('looser', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='lost_battles', to='halloffame.Hero')),
            ],
        ),
        migrations.CreateModel(
            name='Round',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hp_dealt', models.PositiveSmallIntegerField()),
                ('attacker', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='battle_log_attacker', to='halloffame.Hero')),
                ('battle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='round', to='battles.Battle')),
                ('defender', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='battle_log_defender', to='halloffame.Hero')),
            ],
        ),
    ]
