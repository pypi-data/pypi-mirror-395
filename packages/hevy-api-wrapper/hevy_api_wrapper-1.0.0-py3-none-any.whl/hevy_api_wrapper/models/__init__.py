"""Pydantic models for Hevy API request and response schemas."""

from __future__ import annotations

# Create custom exercise
from .create_custom_exercise import CreateCustomExercise
from .create_custom_exercise_request_body import CreateCustomExerciseRequestBody
from .create_custom_exercise_response import CreateCustomExerciseResponse
from .custom_exercise_type import CustomExerciseType
from .deleted_workout import DeletedWorkout
from .equipment_category import EquipmentCategory
from .event import Event
from .exercise_history_entry import ExerciseHistoryEntry

# Exercise history response
from .exercise_history_response import ExerciseHistoryResponse
from .exercise_model import Exercise
from .exercise_template import ExerciseTemplate
from .muscle_group import MuscleGroup
from .paginated_exercise_templates import PaginatedExerciseTemplates
from .paginated_routine_folders import PaginatedRoutineFolders
from .paginated_routines import PaginatedRoutines
from .paginated_workout_events import PaginatedWorkoutEvents
from .paginated_workouts import PaginatedWorkouts

# Routine folder create
from .post_routine_folder import PostRoutineFolder
from .post_routine_folder_request_body import PostRoutineFolderRequestBody
from .post_routines_request_body import PostRoutinesRequestBody
from .post_routines_request_body_routine import PostRoutinesRequestBodyRoutine
from .post_routines_request_exercise import PostRoutinesRequestExercise

# Routines: requests (POST/PUT)
from .post_routines_request_set import PostRoutinesRequestSet
from .post_workouts_request_body import PostWorkoutsRequestBody
from .post_workouts_request_body_workout import PostWorkoutsRequestBodyWorkout
from .post_workouts_request_exercise import PostWorkoutsRequestExercise

# Workouts: requests and entities
from .post_workouts_request_set import PostWorkoutsRequestSet
from .put_routines_request_body import PutRoutinesRequestBody
from .put_routines_request_body_routine import PutRoutinesRequestBodyRoutine
from .put_routines_request_exercise import PutRoutinesRequestExercise
from .put_routines_request_set import PutRoutinesRequestSet

# Shared / exercise-related
from .rep_range import RepRange
from .routine import Routine
from .routine_array_response import RoutineArrayResponse
from .routine_exercise import RoutineExercise

# Routine entities
from .routine_folder import RoutineFolder
from .routine_folder_response import RoutineFolderResponse
from .routine_response import RoutineResponse
from .routine_set import RoutineSet
from .set_model import Set

# Events
from .updated_workout import UpdatedWorkout
from .workout import Workout
from .workout_exercise import WorkoutExercise
from .workout_set import WorkoutSet

__all__ = [
    # Enums
    "CustomExerciseType",
    "MuscleGroup",
    "EquipmentCategory",
    # Shared
    "RepRange",
    "Set",
    "Exercise",
    "ExerciseHistoryEntry",
    "ExerciseTemplate",
    # Create custom exercise
    "CreateCustomExercise",
    "CreateCustomExerciseRequestBody",
    "CreateCustomExerciseResponse",
    # Routines request bodies
    "PostRoutinesRequestSet",
    "PostRoutinesRequestExercise",
    "PostRoutinesRequestBodyRoutine",
    "PostRoutinesRequestBody",
    "PutRoutinesRequestSet",
    "PutRoutinesRequestExercise",
    "PutRoutinesRequestBodyRoutine",
    "PutRoutinesRequestBody",
    # Routine entities
    "RoutineFolder",
    "RoutineFolderResponse",
    "RoutineSet",
    "RoutineExercise",
    "Routine",
    "RoutineResponse",
    "RoutineArrayResponse",
    # Workouts request/response
    "PostWorkoutsRequestSet",
    "PostWorkoutsRequestExercise",
    "PostWorkoutsRequestBodyWorkout",
    "PostWorkoutsRequestBody",
    "WorkoutSet",
    "WorkoutExercise",
    "Workout",
    "PaginatedWorkouts",
    # Events
    "UpdatedWorkout",
    "DeletedWorkout",
    "Event",
    "PaginatedWorkoutEvents",
    # Routine folder create
    "PostRoutineFolder",
    "PostRoutineFolderRequestBody",
    "PaginatedRoutineFolders",
    "PaginatedExerciseTemplates",
    "PaginatedRoutines",
    # Exercise history response
    "ExerciseHistoryResponse",
]
