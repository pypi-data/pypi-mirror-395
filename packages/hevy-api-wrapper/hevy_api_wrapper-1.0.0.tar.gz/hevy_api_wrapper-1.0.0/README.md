# Hevy API Wrapper

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A fully-typed, comprehensive Python client for the [Hevy API](https://api.hevyapp.com/docs/) with both synchronous and
asynchronous support.

Built with modern Python best practices using `httpx` for HTTP transport and `pydantic` v2 for data validation and type
safety.

> **⚠️ Important:** This is an **unofficial** community project. We are not affiliated with, endorsed by, or employed by
> Hevy. API access requires a **Hevy Pro membership**.

---

## 📋 Table of Contents

- [Features](#-features)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [API Endpoints](#-api-endpoints)
    - [Workouts](#workouts)
    - [Routines](#routines)
    - [Exercise Templates](#exercise-templates)
    - [Routine Folders](#routine-folders)
    - [Exercise History](#exercise-history)
- [Configuration](#-configuration)
- [Error Handling](#-error-handling)
- [Examples](#-examples)
- [Testing](#-testing)
- [Project Structure](#-project-structure)
- [Contributing](#-contributing)
- [License](#-license)
- [Links](#-links)
- [Changelog](#-changelog)
- [Tips & Best Practices](#-tips--best-practices)

---

## ✨ Features

- 🔄 **Sync & Async Support** – Use `Client` for synchronous or `AsyncClient` for async/await patterns
- 🎯 **Fully Typed** – Complete type hints and Pydantic models for all API resources
- 📦 **All Endpoints Covered** – Workouts, routines, exercise templates, routine folders, exercise history
- 🔁 **Smart Retries** – Automatic exponential backoff for rate limits (429) and server errors (5xx)
- 📄 **Pagination Helpers** – Simple page/pageSize parameters with validation
- 🛡️ **Custom Exception Hierarchy** – Structured error handling with request IDs
- 🔐 **Environment Variable Support** – Use `.env` files via python-dotenv
- ✅ **100% Test Coverage** – Comprehensive test suite with mocked API responses

---

## 📦 Installation

### Using pip (No Poetry Required)

```bash
pip install hevy-api-wrapper
```

That's it! No need to install Poetry or any other build tools.

### Using Poetry

If you're already using Poetry in your project:

```bash
poetry add hevy-api-wrapper
```

### For Development

If you want to contribute or modify the code, you'll need Poetry:

```bash
# Install Poetry first (if not already installed)
pip install poetry

# Clone and setup
git clone https://github.com/dkuncik/hevy-api-wrapper.git
cd hevy-api-wrapper
poetry install
```

---

## 🚀 Quick Start

### Get Your API Key

> **Note:** API access requires a Hevy Pro membership and is only available through the web application.

1. Visit [https://hevy.com/settings?developer](https://hevy.com/settings?developer) (requires Hevy Pro)
2. Generate your API key
3. Store it securely in a `.env` file:

```bash
HEVY_API_TOKEN=your_api_key_here
```

> **Disclaimer:** This is an unofficial, community-built wrapper. We are not affiliated with, endorsed by, or employed
> by the Hevy team.

### Basic Usage (Sync)

```python
from hevy_api_wrapper import Client

# Load from environment variable HEVY_API_TOKEN
client = Client.from_env()

# List your workouts
workouts = client.workouts.get_workouts(page=1, page_size=10)
for workout in workouts.workouts:
    print(f"{workout.title} - {workout.start_time}")

# Get total workout count
total = client.workouts.get_count()
print(f"Total workouts: {total}")

# Don't forget to close
client.close()
```

### Using Context Manager (Recommended)

```python
from hevy_api_wrapper import Client

with Client.from_env() as client:
    workouts = client.workouts.get_workouts(page=1, page_size=5)
    print(f"Found {len(workouts.workouts)} workouts")
```

### Async Usage

```python
import asyncio
from hevy_api_wrapper import AsyncClient


async def main():
    async with AsyncClient.from_env() as client:
        # List exercise templates
        templates = await client.exercise_templates.get_exercise_templates(
            page=1,
            page_size=25
        )

        for template in templates.exercise_templates:
            print(f"{template.title} ({template.type})")


asyncio.run(main())
```

---

## 📚 API Endpoints

### Workouts

```python
client = Client.from_env()

# List workouts with pagination
workouts = client.workouts.get_workouts(page=1, page_size=10)

# Get a single workout by ID
workout = client.workouts.get_workout("workout-id")

# Create a new workout
from hevy_api_wrapper.models import (
    PostWorkoutsRequestBody,
    PostWorkoutsRequestBodyWorkout,
    PostWorkoutsRequestExercise,
    PostWorkoutsRequestSet,
)

body = PostWorkoutsRequestBody(
    workout=PostWorkoutsRequestBodyWorkout(
        title="Morning Workout",
        description="Chest and triceps",
        start_time="2024-12-02T08:00:00Z",
        end_time="2024-12-02T09:30:00Z",
        routine_id=None,  # Optional: set to None or omit to create workout without a routine
        exercises=[
            PostWorkoutsRequestExercise(
                exercise_template_id="05293BCA",
                sets=[
                    PostWorkoutsRequestSet(
                        type="normal",
                        weight_kg=80,
                        reps=10,
                        rpe=8.5
                    )
                ]
            )
        ]
    )
)
created = client.workouts.create_workout(body)

# Update an existing workout
updated = client.workouts.update_workout("workout-id", body)

# Get workout events (changes since a timestamp)
events = client.workouts.get_events(
    page=1,
    page_size=10,
    since="2024-01-01T00:00:00Z"  # Defaults to epoch time if not provided
)

# Get total workout count
count = client.workouts.get_count()
```

### Routines

```python
# List routines
routines = client.routines.get_routines(page=1, page_size=10)

# Get a single routine
routine = client.routines.get_routine("routine-id")

# Create a routine
from hevy_api_wrapper.models import (
    PostRoutinesRequestBody,
    PostRoutinesRequestBodyRoutine,
    PostRoutinesRequestExercise,
    PostRoutinesRequestSet,
)

body = PostRoutinesRequestBody(
    routine=PostRoutinesRequestBodyRoutine(
        title="Push Day",
        folder_id=None,
        exercises=[
            PostRoutinesRequestExercise(
                exercise_template_id="05293BCA",
                rest_seconds=90,
                sets=[
                    PostRoutinesRequestSet(
                        type="normal",
                        weight_kg=80,
                        reps=10
                    )
                ]
            )
        ]
    )
)
created = client.routines.create_routine(body)

# Update a routine
from hevy_api_wrapper.models import (
    PutRoutinesRequestBody,
    PutRoutinesRequestBodyRoutine,
)

update_body = PutRoutinesRequestBody(
    routine=PutRoutinesRequestBodyRoutine(
        title="Push Day (Updated)",
        exercises=[...]
    )
)
updated = client.routines.update_routine("routine-id", update_body)
```

### Exercise Templates

```python
# List all exercise templates (includes Hevy's library + your custom exercises)
templates = client.exercise_templates.get_exercise_templates(
    page=1,
    page_size=100  # Max 100 per page
)

# Get a single exercise template
template = client.exercise_templates.get_exercise_template("template-id")

# Create a custom exercise
from hevy_api_wrapper.models import (
    CreateCustomExerciseRequestBody,
    CreateCustomExercise,
    CustomExerciseType,
    MuscleGroup,
    EquipmentCategory,
)

body = CreateCustomExerciseRequestBody(
    exercise=CreateCustomExercise(
        title="My Custom Exercise",
        exercise_type=CustomExerciseType.weight_reps,
        equipment_category=EquipmentCategory.barbell,
        muscle_group=MuscleGroup.chest,
        other_muscles=[MuscleGroup.triceps]
    )
)
created = client.exercise_templates.create_custom_exercise(body)
```

### Routine Folders

```python
# List routine folders
folders = client.routine_folders.get_routine_folders(page=1, page_size=10)

# Get a single folder
folder = client.routine_folders.get_routine_folder(42)

# Create a new folder
from hevy_api_wrapper.models import (
    PostRoutineFolderRequestBody,
    PostRoutineFolder,
)

body = PostRoutineFolderRequestBody(
    routine_folder=PostRoutineFolder(title="My Programs")
)
created = client.routine_folders.create_routine_folder(body)
```

### Exercise History

```python
# Get exercise history for a specific exercise template
history = client.exercise_history.get_exercise_history(
    "exercise-template-id",
    start_date="2024-01-01T00:00:00Z",  # Optional
    end_date="2024-12-31T23:59:59Z"  # Optional
)

for entry in history.exercise_history:
    print(f"{entry.workout_title}: {entry.weight_kg}kg x {entry.reps}")
```

---

## 🎯 Configuration

### Client Options

```python
from hevy_api_wrapper import Client

client = Client(
    api_key="your-api-key",  # Or use from_env()
    base_url="https://api.hevyapp.com/",  # API base URL
    api_key_header="api-key",  # Header name for API key
    timeout=30.0,  # Request timeout in seconds
    max_retries=3,  # Max retry attempts for 429/5xx
    backoff_factor=0.5  # Exponential backoff multiplier
)
```

### Environment Variables

Create a `.env` file in your project root:

```env
HEVY_API_TOKEN=your_api_key_here
```

Then use `Client.from_env()` or `AsyncClient.from_env()` to automatically load it:

```python
from hevy_api_wrapper import Client

# Looks for HEVY_API_TOKEN by default
client = Client.from_env()

# Or specify a custom variable name
client = Client.from_env(env_var="MY_HEVY_KEY")
```

---

## 🔧 Error Handling

The wrapper provides structured exception classes for different error scenarios:

```python
from hevy_api_wrapper import Client
from hevy_api_wrapper.errors import (
    HevyApiError,  # Base exception
    AuthError,  # 401, 403
    NotFoundError,  # 404
    ValidationError,  # 400
    RateLimitError,  # 429
    ServerError,  # 5xx
)

try:
    workout = client.workouts.get_workout("invalid-id")
except NotFoundError as e:
    print(f"Workout not found: {e}")
    print(f"Status code: {e.status_code}")
    print(f"Request ID: {e.request_id}")
except AuthError as e:
    print(f"Authentication failed: {e}")
except HevyApiError as e:
    print(f"API error: {e}")
```

---

## 📖 Examples

Check out the [`examples/`](examples/) directory for complete working examples:

- **[workouts_example.py](examples/workouts_example.py)** – Comprehensive workout examples including list, create,
  update, get by ID, get events, and get count
- **[routines_example.py](examples/routines_example.py)** – Routine and routine folder examples including list, create,
  update, and get by ID
- **[exercise_templates_example.py](examples/exercise_templates_example.py)** – Exercise template examples including
  list, create custom exercise, and get by ID
- **[exercise_history_example.py](examples/exercise_history_example.py)** – Get exercise history for a specific template
  with optional date filtering

### Running Examples

```bash
# Set your API key
export HEVY_API_TOKEN=your_api_key_here  # Linux/macOS
$env:HEVY_API_TOKEN = "your_api_key_here"  # PowerShell

# Run an example
python examples/workouts_example.py
```

---

## 🧪 Testing

The project includes a comprehensive test suite with 100% endpoint coverage:

```bash
# Run all tests
poetry run pytest

# Run with coverage report
poetry run pytest --cov=hevy_api_wrapper --cov-report=html

# Run specific test file
poetry run pytest tests/test_endpoints_sync.py -v
```

Tests use `respx` to mock HTTP responses, ensuring fast and reliable testing without hitting the actual API.

---

## 🏗️ Project Structure

```
hevy-api-wrapper/
├── src/
│   └── hevy_api_wrapper/
│       ├── __init__.py           # Main exports
│       ├── client.py             # Client & AsyncClient
│       ├── errors.py             # Exception hierarchy
│       ├── version.py            # Version info
│       ├── endpoints/            # API endpoint groups
│       │   ├── workouts.py
│       │   ├── routines.py
│       │   ├── exercise_templates.py
│       │   ├── routine_folders.py
│       │   └── exercise_history.py
│       └── models/               # Pydantic models (one per file)
│           ├── workout.py
│           ├── routine.py
│           ├── exercise_template.py
│           ├── paginated_workouts.py
│           └── ... (50+ model files)
├── tests/
│   ├── test_endpoints_sync.py   # Sync endpoint tests
│   └── test_endpoints_async.py  # Async endpoint tests
├── examples/                     # Working example scripts
├── pyproject.toml               # Poetry configuration
└── README.md                    # This file
```

---

## 🤝 Contributing

Contributions are welcome! Here's how to get started:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes** and add tests
4. **Run tests**: `poetry run pytest`
5. **Commit your changes**: `git commit -m 'Add amazing feature'`
6. **Push to the branch**: `git push origin feature/amazing-feature`
7. **Open a Pull Request**

### Development Setup

```bash
# Clone your fork
git clone https://github.com/dkuncik/hevy-api-wrapper.git
cd hevy-api-wrapper

# Install dependencies
poetry install

# Run tests
poetry run pytest -v

# Run tests with coverage
poetry run pytest --cov=hevy_api_wrapper
```

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🔗 Links

- **Hevy App**: [https://www.hevyapp.com/](https://www.hevyapp.com/)
- **Hevy API Documentation**: [https://api.hevyapp.com/docs/](https://api.hevyapp.com/docs/)
- **Issues**: [GitHub Issues](https://github.com/dkuncik/hevy-api-wrapper/issues)

---

## 🧾 Changelog

### v1.0.0 — First public stable release (2025-12-03)

This is the first public stable release of `hevy-api-wrapper`.

Highlights:
- Sync and async clients (`Client`, `AsyncClient`)
- Typed models for workouts, routines, exercise templates, routine folders, and exercise history
- Robust pagination, retries, and structured error handling
- Examples for common operations and test suite for endpoints
- GitHub Actions for tests and code quality; pre-commit hooks for formatting

Install:
```bash
pip install hevy-api-wrapper==1.0.0
```

---

## 💡 Tips & Best Practices

### Use Context Managers

Always use context managers (`with` or `async with`) to ensure proper cleanup:

```python
# ✅ Good
with Client.from_env() as client:
    workouts = client.workouts.get_workouts()

# ❌ Bad
client = Client.from_env()
workouts = client.workouts.get_workouts()
# Forgot to call client.close()!
```

### Handle Rate Limits Gracefully

The client automatically retries on 429 (rate limit) errors, but you can catch them:

```python
from hevy_api_wrapper.errors import RateLimitError

try:
    workouts = client.workouts.get_workouts()
except RateLimitError as e:
    print(f"Rate limited. Try again later. Request ID: {e.request_id}")
```

### Pagination Best Practices

```python
# Fetch all workouts across multiple pages
all_workouts = []
page = 1

while True:
    response = client.workouts.get_workouts(page=page, page_size=10)
    all_workouts.extend(response.workouts)

    if page >= response.page_count:
        break
    page += 1

print(f"Total workouts fetched: {len(all_workouts)}")
```

### Type Hints for Better IDE Support

```python
from hevy_api_wrapper import Client
from hevy_api_wrapper.models import Workout, PaginatedWorkouts

client: Client = Client.from_env()
workouts: PaginatedWorkouts = client.workouts.get_workouts()
workout: Workout = workouts.workouts[0]
```

### Working with Workout Events

When using `get_events()`, the response contains lists of updated and deleted workouts:

```python
from datetime import datetime, timedelta

# Get events from the last 7 days
since = (datetime.now() - timedelta(days=7)).isoformat() + "Z"
events = client.workouts.get_events(page=1, page_size=100, since=since)

# Process updated workouts
for workout in events.updated:
    print(f"Updated: {workout.title} at {workout.updated_at}")

# Process deleted workouts
for deleted in events.deleted:
    print(f"Deleted workout ID: {deleted.id} at {deleted.deleted_at}")
```

### Understanding API Response Structures

Some API endpoints wrap responses in extra layers. The client automatically unwraps these:

```python
# When you call create_routine(), the API returns:
# { "routine": { "id": "...", "title": "...", ... } }
#
# The client automatically extracts and returns just the routine object
routine = client.routines.create_routine(body)
print(routine.title)  # Direct access to routine properties

# Same for workouts in the update endpoint:
# API returns: { "workout": [{ "id": "...", ... }] }
# Client returns: Workout object
workout = client.workouts.update_workout(workout_id, body)
```

---

**Made with ❤️ for the Hevy community**
