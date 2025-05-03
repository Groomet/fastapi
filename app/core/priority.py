from datetime import datetime, timedelta
from typing import List

from app.models.task import Task

def calculate_priority(task: Task) -> float:
    """
    Calculate task priority based on various factors:
    - Time since creation (urgency)
    - Current status
    - User-defined priority
    """
    # Base priority from user input
    base_priority = task.priority

    # Time-based urgency factor
    time_factor = calculate_time_factor(task.created_at)
    
    # Status factor
    status_factor = get_status_factor(task.status)
    
    # Combine factors
    final_priority = base_priority * (1 + time_factor) * status_factor
    
    # Ensure priority is between 0 and 1
    return max(0.0, min(1.0, final_priority))

def calculate_time_factor(created_at: datetime) -> float:
    """
    Calculate urgency based on time since creation.
    Tasks become more urgent as time passes.
    """
    hours_since_creation = (datetime.utcnow() - created_at).total_seconds() / 3600
    
    # Exponential decay: urgency increases with time
    # After 24 hours, urgency factor is 0.5
    # After 48 hours, urgency factor is 0.75
    time_factor = 1 - (2 ** (-hours_since_creation / 24))
    
    return time_factor

def get_status_factor(status: str) -> float:
    """
    Get priority multiplier based on task status.
    """
    status_factors = {
        "pending": 1.0,
        "in_progress": 1.2,
        "blocked": 0.8,
        "completed": 0.0
    }
    return status_factors.get(status.lower(), 1.0)

def sort_tasks_by_priority(tasks: List[Task]) -> List[Task]:
    """
    Sort tasks by their calculated priority.
    """
    return sorted(
        tasks,
        key=lambda task: calculate_priority(task),
        reverse=True
    ) 