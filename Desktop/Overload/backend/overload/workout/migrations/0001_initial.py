# Generated by Django 4.1.2 on 2022-10-25 03:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BodyPart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='BodyPart', max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='ExerciseClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='exercise', max_length=40)),
                ('position', models.CharField(default='', max_length=32)),
                ('body_part', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='ExerciseOptions', to='workout.bodypart')),
            ],
        ),
        migrations.CreateModel(
            name='Workout',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Workout', max_length=64)),
                ('date', models.CharField(max_length=8)),
            ],
        ),
        migrations.CreateModel(
            name='ExerciseInstance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(default='', max_length=24)),
                ('sequence', models.IntegerField(default=-1)),
                ('weight', models.IntegerField(default=0)),
                ('reps', models.IntegerField(default=0)),
                ('exercise_class', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='ExerciseInstances', to='workout.exerciseclass')),
                ('workout', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='Exercises', to='workout.workout')),
            ],
        ),
    ]
