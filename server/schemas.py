from marshmallow import Schema, fields, validates, ValidationError


class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    category = fields.Str(required=True)
    equipment_needed = fields.Bool(load_default=False)

    @validates('name')
    def validate_name(self, value):
        if not value or not value.strip():
            raise ValidationError('Name cannot be empty')

    @validates('category')
    def validate_category(self, value):
        if not value or not value.strip():
            raise ValidationError('Category cannot be empty')


class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(required=True)
    exercise_id = fields.Int(required=True)
    reps = fields.Int(allow_none=True)
    sets = fields.Int(allow_none=True)
    duration_seconds = fields.Int(allow_none=True)

    @validates('reps')
    def validate_reps(self, value):
        if value is not None and value <= 0:
            raise ValidationError('Reps must be greater than 0')

    @validates('sets')
    def validate_sets(self, value):
        if value is not None and value <= 0:
            raise ValidationError('Sets must be greater than 0')

    @validates('duration_seconds')
    def validate_duration_seconds(self, value):
        if value is not None and value <= 0:
            raise ValidationError('Duration must be greater than 0')


class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Int(required=True)
    notes = fields.Str(allow_none=True)

    @validates('duration_minutes')
    def validate_duration_minutes(self, value):
        if value is None or value <= 0:
            raise ValidationError('Duration must be greater than 0')


class WorkoutWithExercisesSchema(WorkoutSchema):
    exercises = fields.Nested(ExerciseSchema, many=True, dump_only=True)
    workout_exercises = fields.Nested(WorkoutExerciseSchema, many=True, dump_only=True)


class ExerciseWithWorkoutsSchema(ExerciseSchema):
    workouts = fields.Nested(WorkoutSchema, many=True, dump_only=True)
