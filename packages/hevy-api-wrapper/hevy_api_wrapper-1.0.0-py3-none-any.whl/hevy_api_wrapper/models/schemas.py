from __future__ import annotations

from enum import Enum
from typing import Annotated, List, Literal, Optional, Union

from pydantic import BaseModel, Field, field_validator

# ===== Enums =====


class CustomExerciseType(str, Enum):
    weight_reps = "weight_reps"
    reps_only = "reps_only"
    bodyweight_reps = "bodyweight_reps"
    bodyweight_assisted_reps = "bodyweight_assisted_reps"
    duration = "duration"
    weight_duration = "weight_duration"
    distance_duration = "distance_duration"
    short_distance_weight = "short_distance_weight"


class MuscleGroup(str, Enum):
    abdominals = "abdominals"
    shoulders = "shoulders"
    biceps = "biceps"
    triceps = "triceps"
    forearms = "forearms"
    quadriceps = "quadriceps"
    hamstrings = "hamstrings"
    calves = "calves"
    glutes = "glutes"
    abductors = "abductors"
    adductors = "adductors"
    lats = "lats"
    upper_back = "upper_back"
    traps = "traps"
    lower_back = "lower_back"
    chest = "chest"
    cardio = "cardio"
    neck = "neck"
    full_body = "full_body"
    other = "other"


class EquipmentCategory(str, Enum):
    none = "none"
    barbell = "barbell"
    dumbbell = "dumbbell"
    kettlebell = "kettlebell"
    machine = "machine"
    plate = "plate"
    resistance_band = "resistance_band"
    suspension = "suspension"
    other = "other"


# ===== Shared nested models =====


class RepRange(BaseModel):
    start: Optional[float] = None
    end: Optional[float] = None


class Set(BaseModel):
    index: int
    type: Literal["normal", "warmup", "dropset", "failure"]
    weight_kg: Optional[float] = None
    reps: Optional[int] = None
    distance_meters: Optional[float] = None
    duration_seconds: Optional[float] = None
    rpe: Optional[float] = None
    custom_metric: Optional[float] = None


class Exercise(BaseModel):
    index: int
    title: str
    notes: Optional[str] = None
    exercise_template_id: str
    supersets_id: Optional[int] = None
    sets: List[Set]


class ExerciseHistoryEntry(BaseModel):
    workout_id: str
    workout_title: str
    workout_start_time: str
    workout_end_time: str
    exercise_template_id: str
    weight_kg: Optional[float] = None
    reps: Optional[int] = None
    distance_meters: Optional[int] = None
    duration_seconds: Optional[int] = None
    rpe: Optional[float] = None
    custom_metric: Optional[float] = None
    set_type: Literal["warmup", "normal", "failure", "dropset"]


class ExerciseTemplate(BaseModel):
    id: str
    title: str
    type: CustomExerciseType
    primary_muscle_group: MuscleGroup
    secondary_muscle_groups: List[str] = Field(default_factory=list)
    is_custom: bool


# ===== Create Custom Exercise =====


class CreateCustomExercise(BaseModel):
    title: str
    exercise_type: CustomExerciseType
    equipment_category: EquipmentCategory
    muscle_group: MuscleGroup
    other_muscles: List[MuscleGroup] = Field(default_factory=list)


class CreateCustomExerciseRequestBody(BaseModel):
    exercise: CreateCustomExercise


# ===== Routines (POST/PUT and entities) =====


class PostRoutinesRequestSet(BaseModel):
    type: Literal["warmup", "normal", "failure", "dropset"]
    weight_kg: Optional[float] = None
    reps: Optional[int] = None
    distance_meters: Optional[int] = None
    duration_seconds: Optional[int] = None
    custom_metric: Optional[float] = None
    rep_range: Optional[RepRange] = None


class PostRoutinesRequestExercise(BaseModel):
    exercise_template_id: str
    superset_id: Optional[int] = None
    rest_seconds: Optional[int] = None
    notes: Optional[str] = None
    sets: List[PostRoutinesRequestSet]


class PostRoutinesRequestBodyRoutine(BaseModel):
    title: str
    folder_id: Optional[int] = None
    notes: Optional[str] = None
    exercises: List[PostRoutinesRequestExercise]


class PostRoutinesRequestBody(BaseModel):
    routine: PostRoutinesRequestBodyRoutine


class PutRoutinesRequestSet(BaseModel):
    type: Literal["warmup", "normal", "failure", "dropset"]
    weight_kg: Optional[float] = None
    reps: Optional[int] = None
    distance_meters: Optional[int] = None
    duration_seconds: Optional[int] = None
    custom_metric: Optional[float] = None
    rep_range: Optional[RepRange] = None


class PutRoutinesRequestExercise(BaseModel):
    exercise_template_id: str
    superset_id: Optional[int] = None
    rest_seconds: Optional[int] = None
    notes: Optional[str] = None
    sets: List[PutRoutinesRequestSet]


class PutRoutinesRequestBodyRoutine(BaseModel):
    title: str
    notes: Optional[str] = None
    exercises: List[PutRoutinesRequestExercise]


class PutRoutinesRequestBody(BaseModel):
    routine: PutRoutinesRequestBodyRoutine


class RoutineFolder(BaseModel):
    id: int
    index: int
    title: str
    updated_at: str
    created_at: str


class RoutineSet(BaseModel):
    index: int
    type: Literal["normal", "warmup", "dropset", "failure"]
    weight_kg: Optional[float] = None
    reps: Optional[int] = None
    rep_range: Optional[RepRange] = None
    distance_meters: Optional[float] = None
    duration_seconds: Optional[float] = None
    rpe: Optional[float] = None
    custom_metric: Optional[float] = None


class RoutineExercise(BaseModel):
    index: int
    title: str
    rest_seconds: Optional[int] = None
    notes: Optional[str] = None
    exercise_template_id: str
    supersets_id: Optional[int] = None
    sets: List[RoutineSet]


class Routine(BaseModel):
    id: str
    title: str
    folder_id: Optional[int] = None
    updated_at: str
    created_at: str
    exercises: List[RoutineExercise]


# ===== Workouts (POST body and entities) =====


class PostWorkoutsRequestSet(BaseModel):
    type: Literal["warmup", "normal", "failure", "dropset"]
    weight_kg: Optional[float] = None
    reps: Optional[int] = None
    distance_meters: Optional[int] = None
    duration_seconds: Optional[int] = None
    custom_metric: Optional[float] = None
    rpe: Optional[float] = None

    @field_validator("rpe")
    @classmethod
    def validate_rpe_enum(cls, v: Optional[float]) -> Optional[float]:
        if v is None:
            return v
        allowed = {6, 7, 7.5, 8, 8.5, 9, 9.5, 10}
        if v not in allowed:
            raise ValueError("rpe must be one of 6,7,7.5,8,8.5,9,9.5,10")
        return v


class PostWorkoutsRequestExercise(BaseModel):
    exercise_template_id: str
    superset_id: Optional[int] = None
    notes: Optional[str] = None
    sets: List[PostWorkoutsRequestSet]


class PostWorkoutsRequestBodyWorkout(BaseModel):
    title: str
    description: Optional[str] = None
    start_time: str
    routine_id: str
    end_time: str
    is_private: bool
    exercises: List[PostWorkoutsRequestExercise]


class PostWorkoutsRequestBody(BaseModel):
    workout: PostWorkoutsRequestBodyWorkout


class WorkoutSet(BaseModel):
    index: int
    type: Literal["normal", "warmup", "dropset", "failure"]
    weight_kg: Optional[float] = None
    reps: Optional[int] = None
    distance_meters: Optional[float] = None
    duration_seconds: Optional[float] = None
    rpe: Optional[float] = None
    custom_metric: Optional[float] = None


class WorkoutExercise(BaseModel):
    index: int
    title: str
    notes: Optional[str] = None
    exercise_template_id: str
    supersets_id: Optional[int] = None
    sets: List[WorkoutSet]


class Workout(BaseModel):
    id: str
    title: str
    routine_id: str
    description: str
    start_time: str
    end_time: str
    updated_at: str
    created_at: str
    exercises: List[WorkoutExercise]


class UpdatedWorkout(BaseModel):
    type: Literal["updated"]
    workout: Workout


class DeletedWorkout(BaseModel):
    type: Literal["deleted"]
    id: str
    deleted_at: str


Event = Annotated[Union[UpdatedWorkout, DeletedWorkout], Field(discriminator="type")]


class PaginatedWorkoutEvents(BaseModel):
    page: int
    page_count: int
    events: List[Event]


class PostRoutineFolder(BaseModel):
    title: str


class PostRoutineFolderRequestBody(BaseModel):
    routine_folder: PostRoutineFolder


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
    "RoutineSet",
    "RoutineExercise",
    "Routine",
    # Workouts request/response
    "PostWorkoutsRequestSet",
    "PostWorkoutsRequestExercise",
    "PostWorkoutsRequestBodyWorkout",
    "PostWorkoutsRequestBody",
    "WorkoutSet",
    "WorkoutExercise",
    "Workout",
    # Events
    "UpdatedWorkout",
    "DeletedWorkout",
    "Event",
    "PaginatedWorkoutEvents",
    # Routine folder create
    "PostRoutineFolder",
    "PostRoutineFolderRequestBody",
]
