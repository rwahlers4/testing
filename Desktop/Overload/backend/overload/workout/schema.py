from turtle import window_height
from sympy import sequence
import graphene

from graphene_django import DjangoObjectType, DjangoListField
from .models import ExerciseInstance, ExerciseClass, Workout, BodyPart

class WorkoutType(DjangoObjectType):
    class Meta:
        model = Workout
        fields = ['Exercises', 'date', 'name']

class ExerciseInstanceType(DjangoObjectType):
    class Meta:
        model = ExerciseInstance
        fields = '__all__'

class ExerciseClassType(DjangoObjectType):
    class Meta:
        model = ExerciseClass
        fields = '__all__'


class BodyPartType(DjangoObjectType):
    class Meta:
        model = BodyPart
        fields = '__all__'

class Query(graphene.ObjectType):
    #Workouts
    all_workouts = graphene.List(WorkoutType)
    workout = graphene.Field(WorkoutType, workout_id = graphene.Int())

    def resolve_all_workouts(self, info, **kwargs):
        return Workout.objects.all()

    def resolve_workout(self, info, workout_id):
        return Workout.objects.get(pk = workout_id)

    #Exercises
    all_exercises = graphene.List(ExerciseInstanceType)
    exercise_instance = graphene.Field(ExerciseInstanceType, exercise_instance_id=graphene.Int())

    def resolve_all_exercises(self, info, **kwargs):
        return ExerciseInstance.objects.all()

    def resolve_exercise(self, info, exercise_instance_id):
        return ExerciseInstance.objects.get(pk=exercise_instance_id)

    #ExerciseClasses
    all_exercise_classes = graphene.List(ExerciseClassType)
    exercise_class = graphene.Field(ExerciseClassType, exercise_class_id=graphene.Int())

    def resolve_all_exercise_classes(self, info, **kwargs):
        return ExerciseClass.objects.all()

    def resolve_exercise_class(self, info, exercise_class_id):
        return ExerciseClass.objects.get(pk=exercise_class_id)

    #BodyParts
    all_bodyparts = graphene.List(BodyPartType)
    bodypart = graphene.Field(BodyPartType, bodypart_id=graphene.Int())

    def resolve_all_bodyparts(self, info, **kwargs):
        return BodyPart.objects.all()

    def resolve_workout(self, info, bodypart_id):
        return BodyPart.objects.get(pk=bodypart_id)


#Mutation Inputs
class BodyPartInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String(required=True)


class ExerciseClassInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String(required=True)
    position = graphene.String(required=True)
    body_part = graphene.Field(BodyPartInput)


class WorkoutInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String(required=True)
    date = graphene.String(required=True)


class ExerciseInstanceInput(graphene.InputObjectType):
    id = graphene.ID()
    exercise_class = graphene.Field(ExerciseClassInput)
    date = graphene.String(required=True)
    sequence = graphene.Int()
    weight = graphene.Int()
    reps = graphene.Int()
    workout = graphene.Field(WorkoutInput)


#### Mutations ####

#Workouts
class CreateWorkout(graphene.Mutation):
    class Arguments:
        workout_data = WorkoutInput(required=True)
    workout = graphene.Field(WorkoutType)

    @staticmethod
    def mutate(root, info, workout_data=None):
        workout_inst = Workout.objects.create(**workout_data)
        return workout_inst

class UpdateWorkout(graphene.Mutation):
    class Arguments:
        workout_data = WorkoutInput(required=True)
    workout = graphene.Field(WorkoutType)

    @staticmethod
    def mutate(root, info, workout_data=None):
        workout_object = Workout.objects.get(pk=workout_data.id)
        
        if workout_object:
            workout_object.name = workout_data.name
            workout_object.date = workout_data.date

            workout_object.save()
            return UpdateWorkout(workout = workout_object)
        return UpdateWorkout(workout=None)

class DeleteWorkout(graphene.Mutation):
    class Arguments:
        workout_id = graphene.ID()
    workout = graphene.Field(WorkoutType)

    @staticmethod
    def mutate(root, info, workout_id=None):
        workout_object = Workout.objects.get(pk = workout_id)
        
        workout_object.delete()
        return None


#ExerciseInstances
class CreateExerciseInstance(graphene.Mutation):
    class Arguments:
        exercise_instance_data = ExerciseInstanceInput(required=True)
    exercise_instance = graphene.Field(ExerciseInstanceType)

    @staticmethod
    def mutate(root, info, exercise_instance_data=None):
        exercise_instance_inst = ExerciseInstance.objects.create(**exercise_instance_data)
        return exercise_instance_inst

class UpdateExerciseInstance(graphene.Mutation):
    class Arguments:
        exercise_instance_data = ExerciseInstanceInput(required=True)
    exercise_instance = graphene.Field(ExerciseInstanceType)

    @staticmethod
    def mutate(root, info, exercise_instance_data=None):
        exercise_instance_object = ExerciseInstance.objects.get(pk=exercise_instance_data.id)
        
        if exercise_instance_object:
            exercise_instance_object.exercise_class = exercise_instance_data.exercise_class
            exercise_instance_object.date = exercise_instance_data.date
            exercise_instance_object.sequence = exercise_instance_data.sequence
            exercise_instance_object.weight = exercise_instance_data.weight
            exercise_instance_object.reps = exercise_instance_data.reps
            exercise_instance_object.workout = exercise_instance_data.workout

            exercise_instance_object.save()
            return UpdateExerciseInstance(exercise_instance= exercise_instance_object)
        return UpdateExerciseInstance(exercise_instance=None)

class DeleteExerciseInstance(graphene.Mutation):
    class Arguments:
        exercise_instance_id = graphene.ID()
    exercise_instance = graphene.Field(ExerciseInstanceType)

    @staticmethod
    def mutate(root, info, exercise_instance_id=None):
        exercise_instance_object = ExerciseInstance.objects.get(
            pk=exercise_instance_id)
        
        exercise_instance_object.delete()
        return None

#ExerciseClasses
class CreateExerciseClass(graphene.Mutation):
    class Arguments:
        exercise_class_data = ExerciseClassInput(required=True)
    exercise_class = graphene.Field(ExerciseClassType)

    @staticmethod
    def mutate(root, info, exercise_class_data=None):
        exercise_class_inst = ExerciseClass.objects.create(**exercise_class_data)
        return exercise_class_inst


class UpdateExerciseClass(graphene.Mutation):
    class Arguments:
        exercise_class_data = ExerciseClassInput(required=True)
    exercise_class = graphene.Field(ExerciseClassType)

    @staticmethod
    def mutate(root, info, exercise_class_data=None):
        exercise_class_object = ExerciseClass.objects.get(pk=exercise_class_data.id)

        if exercise_class_object:
            exercise_class_object.name = exercise_class_data.name
            exercise_class_object.position = exercise_class_data.date
            exercise_class_object.body_part = exercise_class_data.body_part

            exercise_class_object.save()
            return UpdateExerciseClass(exercise_class=exercise_class_object)
        return UpdateExerciseClass(exercise_class=None)


class DeleteExerciseClass(graphene.Mutation):
    class Arguments:
        exercise_class_id = graphene.ID()
    exercise_class = graphene.Field(ExerciseClassType)

    @staticmethod
    def mutate(root, info, exercise_class_id=None):
        exercise_class_object = ExerciseClass.objects.get(pk=exercise_class_id)
        
        exercise_class_object.delete()
        return None


#BodyParts
class CreateBodyPart(graphene.Mutation):
    class Arguments:
        body_part_data = BodyPartInput(required=True)
    body_part = graphene.Field(BodyPartType)

    @staticmethod
    def mutate(root, info, body_part_data=None):
        body_part_inst = BodyPart.objects.create(**body_part_data)
        return body_part_inst


class UpdateBodyPart(graphene.Mutation):
    class Arguments:
        body_part_data = BodyPartInput(required=True)
    body_part = graphene.Field(BodyPartType)

    @staticmethod
    def mutate(root, info, body_part_data=None):
        body_part_object = BodyPart.objects.get(pk=body_part_data.id)

        if body_part_object:
            body_part_object.name = body_part_data.name
            
            body_part_object.save()
            return UpdateWorkout(body_part=body_part_object)
        return UpdateWorkout(body_part=None)


class DeleteBodyPart(graphene.Mutation):
    class Arguments:
        body_part_id = BodyPartInput(required=True)
    body_part = graphene.ID()

    @staticmethod
    def mutate(root, info, body_part_id=None):
        body_part_object = BodyPart.objects.get(pk=body_part_id)
        body_part_object.delete()
        
        return None

class Mutation(graphene.ObjectType):
    create_workout = CreateWorkout.Field()
    update_workout = UpdateWorkout.Field()
    delete_workout = DeleteWorkout.Field()

    create_bodypart = CreateBodyPart.Field()
    update_bodypart = UpdateBodyPart.Field()
    delete_bodypart = DeleteBodyPart.Field()

    create_exercise_class = CreateExerciseClass.Field()
    update_exercise_class = UpdateExerciseClass.Field()
    delete_exercise_class = DeleteExerciseClass.Field()

    create_exercise_instance = CreateExerciseInstance.Field()
    update_exercise_instance = UpdateExerciseInstance.Field()
    delete_exercise_instance = DeleteExerciseInstance.Field()



schema = graphene.Schema(query = Query, mutation = Mutation)
