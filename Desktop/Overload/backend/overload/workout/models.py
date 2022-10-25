from django.db import models

# Create your models here.

class BodyPart(models.Model):
    name = models.CharField(max_length=32, default="BodyPart")

class ExerciseClass(models.Model):
    name = models.CharField(max_length = 40, default = "exercise")
    position = models.CharField(max_length = 32, default = "")
    body_part = models.ForeignKey(BodyPart, related_name = "ExerciseOptions", on_delete= models.PROTECT, null=True)

class Workout(models.Model):
    name = models.CharField(max_length = 64, default = "Workout")
    date = models.CharField(max_length=8, default="00000000")

class ExerciseInstance(models.Model):
    exercise_class = models.ForeignKey(ExerciseClass, related_name="ExerciseInstances", on_delete=models.PROTECT)
    sequence = models.IntegerField(default = -1)
    weight = models.IntegerField(default = 0)
    reps = models.IntegerField(default = 0)
    workout = models.ForeignKey(Workout, related_name='Exercises', on_delete=models.PROTECT, null=True)



