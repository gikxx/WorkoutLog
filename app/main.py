from fastapi import FastAPI

from app.api.endpoints import exercises, stats, workouts

app = FastAPI(title="Workout Log API")

app.include_router(workouts.router, prefix="/workouts", tags=["workouts"])
app.include_router(exercises.router, prefix="/exercises", tags=["exercises"])
app.include_router(stats.router, prefix="/stats", tags=["stats"])


@app.get("/")
def root():
    return {"message": "Workout Log API is running"}
