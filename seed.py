#!/usr/bin/env python3
from datetime import date
from server.app import app
from server.models import db, Exercise, Workout, WorkoutExercise

with app.app_context():
    # Clear tables
    WorkoutExercise.query.delete()
    Exercise.query.delete()
    Workout.query.delete()
    db.session.commit()

    # Create exercises
    exercises = [
        Exercise(name='Push-ups', category='Chest', equipment_needed=False),
        Exercise(name='Squats', category='Legs', equipment_needed=False),
        Exercise(name='Bench Press', category='Chest', equipment_needed=True),
        Exercise(name='Deadlift', category='Back', equipment_needed=True),
        Exercise(name='Pull-ups', category='Back', equipment_needed=True),
        Exercise(name='Plank', category='Core', equipment_needed=False),
        Exercise(name='Lunges', category='Legs', equipment_needed=False),
        Exercise(name='Shoulder Press', category='Shoulders', equipment_needed=True),
    ]
    db.session.add_all(exercises)
    db.session.commit()

    # Create workouts
    workouts = [
        Workout(date=date(2026, 4, 6), duration_minutes=45, notes='Morning strength training'),
        Workout(date=date(2026, 4, 7), duration_minutes=30, notes='Quick cardio session'),
        Workout(date=date(2026, 4, 8), duration_minutes=60, notes='Full body workout'),
    ]
    db.session.add_all(workouts)
    db.session.commit()

    # Link exercises to workouts
    workout_exercises = [
        WorkoutExercise(workout_id=workouts[0].id, exercise_id=exercises[0].id, reps=15, sets=3),
        WorkoutExercise(workout_id=workouts[0].id, exercise_id=exercises[2].id, reps=10, sets=4),
        WorkoutExercise(workout_id=workouts[0].id, exercise_id=exercises[7].id, reps=12, sets=3),
        WorkoutExercise(workout_id=workouts[1].id, exercise_id=exercises[1].id, reps=20, sets=3),
        WorkoutExercise(workout_id=workouts[1].id, exercise_id=exercises[6].id, reps=15, sets=3),
        WorkoutExercise(workout_id=workouts[1].id, exercise_id=exercises[5].id, duration_seconds=60, sets=3),
        WorkoutExercise(workout_id=workouts[2].id, exercise_id=exercises[3].id, reps=8, sets=5),
        WorkoutExercise(workout_id=workouts[2].id, exercise_id=exercises[4].id, reps=10, sets=4),
        WorkoutExercise(workout_id=workouts[2].id, exercise_id=exercises[1].id, reps=12, sets=4),
        WorkoutExercise(workout_id=workouts[2].id, exercise_id=exercises[5].id, duration_seconds=90, sets=3),
    ]
    db.session.add_all(workout_exercises)
    db.session.commit()

    print(f'Seeded: {Exercise.query.count()} exercises, {Workout.query.count()} workouts, {WorkoutExercise.query.count()} workout exercises')
