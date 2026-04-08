# Flask SQLAlchemy Workout Application Backend

REST API for tracking workouts and exercises. Built with Flask, SQLAlchemy, and Marshmallow.

## Setup

```bash
pip install flask flask-migrate flask-sqlalchemy werkzeug marshmallow
python -m flask --app server.app db upgrade
python seed.py
```

## Run

```bash
python server/app.py
```

Server runs at `http://localhost:5555`

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/exercises` | List all exercises |
| GET | `/exercises/<id>` | Get exercise with workouts |
| POST | `/exercises` | Create exercise |
| DELETE | `/exercises/<id>` | Delete exercise |
| GET | `/workouts` | List all workouts |
| GET | `/workouts/<id>` | Get workout with exercises |
| POST | `/workouts` | Create workout |
| DELETE | `/workouts/<id>` | Delete workout |
| POST | `/workouts/<workout_id>/exercises/<exercise_id>/workout_exercises` | Add exercise to workout |

### Example Requests

**Create exercise:**
```json
POST /exercises
{"name": "Push-ups", "category": "Chest", "equipment_needed": false}
```

**Create workout:**
```json
POST /workouts
{"date": "2026-04-10", "duration_minutes": 45, "notes": "Morning session"}
```

**Add exercise to workout:**
```json
POST /workouts/1/exercises/1/workout_exercises
{"reps": 15, "sets": 3}
```

## Models

- **Exercise**: name, category, equipment_needed
- **Workout**: date, duration_minutes, notes
- **WorkoutExercise**: workout_id, exercise_id, reps, sets, duration_seconds

Many-to-many: Workout ↔ Exercise through WorkoutExercise.

## Validations

- Table: CheckConstraints on name length, duration > 0, reps/sets or duration required
- Model: @validates on name, category, duration, date, reps, sets
- Schema: Mirrors model validations for request integrity
