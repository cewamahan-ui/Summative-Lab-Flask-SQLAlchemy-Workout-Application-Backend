from flask import Flask, request, make_response
from flask_migrate import Migrate
from datetime import datetime

from server.models import db, Exercise, Workout, WorkoutExercise
from server.schemas import (
    ExerciseSchema, WorkoutSchema, WorkoutWithExercisesSchema,
    ExerciseWithWorkoutsSchema, WorkoutExerciseSchema
)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)


# Exercises

@app.route('/exercises', methods=['GET'])
def get_exercises():
    exercises = Exercise.query.all()
    return make_response(ExerciseSchema(many=True).dump(exercises), 200)


@app.route('/exercises/<int:id>', methods=['GET'])
def get_exercise(id):
    exercise = Exercise.query.get(id)
    if not exercise:
        return make_response({'error': 'Exercise not found'}, 404)
    return make_response(ExerciseWithWorkoutsSchema().dump(exercise), 200)


@app.route('/exercises', methods=['POST'])
def create_exercise():
    data = request.get_json()
    errors = ExerciseSchema().validate(data)
    if errors:
        return make_response({'errors': errors}, 422)
    
    try:
        exercise = Exercise(
            name=data['name'],
            category=data['category'],
            equipment_needed=data.get('equipment_needed', False)
        )
        db.session.add(exercise)
        db.session.commit()
        return make_response(ExerciseSchema().dump(exercise), 201)
    except ValueError as e:
        return make_response({'error': str(e)}, 422)


@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    exercise = Exercise.query.get(id)
    if not exercise:
        return make_response({'error': 'Exercise not found'}, 404)
    db.session.delete(exercise)
    db.session.commit()
    return make_response('', 204)


# Workouts

@app.route('/workouts', methods=['GET'])
def get_workouts():
    workouts = Workout.query.all()
    return make_response(WorkoutSchema(many=True).dump(workouts), 200)


@app.route('/workouts/<int:id>', methods=['GET'])
def get_workout(id):
    workout = Workout.query.get(id)
    if not workout:
        return make_response({'error': 'Workout not found'}, 404)
    return make_response(WorkoutWithExercisesSchema().dump(workout), 200)


@app.route('/workouts', methods=['POST'])
def create_workout():
    data = request.get_json()
    errors = WorkoutSchema().validate(data)
    if errors:
        return make_response({'errors': errors}, 422)
    
    try:
        parsed_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        workout = Workout(
            date=parsed_date,
            duration_minutes=data['duration_minutes'],
            notes=data.get('notes')
        )
        db.session.add(workout)
        db.session.commit()
        return make_response(WorkoutSchema().dump(workout), 201)
    except ValueError as e:
        if 'time data' in str(e):
            return make_response({'error': 'Invalid date format. Use YYYY-MM-DD'}, 422)
        return make_response({'error': str(e)}, 422)


@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    workout = Workout.query.get(id)
    if not workout:
        return make_response({'error': 'Workout not found'}, 404)
    db.session.delete(workout)
    db.session.commit()
    return make_response('', 204)


# Workout Exercises

@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):
    workout = Workout.query.get(workout_id)
    if not workout:
        return make_response({'error': 'Workout not found'}, 404)
    
    exercise = Exercise.query.get(exercise_id)
    if not exercise:
        return make_response({'error': 'Exercise not found'}, 404)
    
    data = request.get_json()
    if not data:
        return make_response({'error': 'Request body required'}, 400)
    
    errors = WorkoutExerciseSchema().validate(data)
    if errors:
        return make_response({'errors': errors}, 422)
    
    try:
        workout_exercise = WorkoutExercise(
            workout_id=workout_id,
            exercise_id=exercise_id,
            reps=data.get('reps'),
            sets=data.get('sets'),
            duration_seconds=data.get('duration_seconds')
        )
        db.session.add(workout_exercise)
        db.session.commit()
        return make_response(WorkoutExerciseSchema().dump(workout_exercise), 201)
    except ValueError as e:
        return make_response({'error': str(e)}, 422)


if __name__ == '__main__':
    app.run(port=5555, debug=True)
