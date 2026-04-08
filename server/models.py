from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy import CheckConstraint

db = SQLAlchemy()


class Exercise(db.Model):
    __tablename__ = 'exercises'
    __table_args__ = (
        CheckConstraint('LENGTH(name) > 0', name='check_name_not_empty'),
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    equipment_needed = db.Column(db.Boolean, default=False)

    workout_exercises = db.relationship('WorkoutExercise', back_populates='exercise', cascade='all, delete-orphan', overlaps='workouts,exercises,workout_exercises')
    workouts = db.relationship('Workout', secondary='workout_exercises', back_populates='exercises', overlaps='workout_exercises,exercises')

    @validates('name')
    def validate_name(self, key, name):
        if not name or not name.strip():
            raise ValueError('Exercise name cannot be empty')
        return name.strip()

    @validates('category')
    def validate_category(self, key, category):
        if not category or not category.strip():
            raise ValueError('Category cannot be empty')
        return category.strip()


class Workout(db.Model):
    __tablename__ = 'workouts'
    __table_args__ = (
        CheckConstraint('duration_minutes > 0', name='check_duration_positive'),
    )

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)

    workout_exercises = db.relationship('WorkoutExercise', back_populates='workout', cascade='all, delete-orphan', overlaps='workouts,exercises,workout_exercises')
    exercises = db.relationship('Exercise', secondary='workout_exercises', back_populates='workouts', overlaps='workout_exercises,workouts')

    @validates('duration_minutes')
    def validate_duration(self, key, duration):
        if duration is None or duration <= 0:
            raise ValueError('Duration must be greater than 0')
        return duration

    @validates('date')
    def validate_date(self, key, date):
        if date is None:
            raise ValueError('Date is required')
        return date


class WorkoutExercise(db.Model):
    __tablename__ = 'workout_exercises'
    __table_args__ = (
        CheckConstraint(
            '(reps IS NOT NULL AND sets IS NOT NULL) OR duration_seconds IS NOT NULL',
            name='check_reps_sets_or_duration'
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

    workout = db.relationship('Workout', back_populates='workout_exercises', overlaps='workouts,exercises,workout_exercises')
    exercise = db.relationship('Exercise', back_populates='workout_exercises', overlaps='workouts,exercises,workout_exercises')

    @validates('reps', 'sets')
    def validate_reps_sets(self, key, value):
        if value is not None and value <= 0:
            raise ValueError(f'{key} must be greater than 0')
        return value

    @validates('duration_seconds')
    def validate_duration_seconds(self, key, value):
        if value is not None and value <= 0:
            raise ValueError('Duration seconds must be greater than 0')
        return value
