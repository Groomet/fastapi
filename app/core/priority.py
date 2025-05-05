"""Алгоритм расчета приоритета задач."""

from datetime import datetime
from typing import List

from app.models.task import Task

def calculate_time_factor(created_at: datetime) -> float:
    """
    Рассчитывает срочность на основе времени с момента создания.
    Задачи становятся более срочными со временем.
    """
    hours_since_creation = (datetime.utcnow() - created_at).total_seconds() / 3600
    
    # Экспоненциальный рост: срочность увеличивается со временем
    # После 24 часов: фактор срочности = 0.5
    # После 48 часов: фактор срочности = 0.75
    time_factor = 1 - (2 ** (-hours_since_creation / 24))
    
    return time_factor

def calculate_due_date_factor(task: Task) -> float:
    """
    Рассчитывает срочность на основе срока выполнения.
    Задачи становятся более срочными по мере приближения дедлайна.
    """
    if not task.due_date:
        return 0.0  # Отсутствие срока означает отсутствие срочности
    
    now = datetime.utcnow()
    due_datetime = datetime.combine(task.due_date, datetime.min.time())
    hours_until_due = (due_datetime - now).total_seconds() / 3600
    
    if hours_until_due <= 0:
        return 1.0  # Просроченные задачи получают максимальную срочность
    
    # Экспоненциальный рост: срочность увеличивается по мере приближения дедлайна
    # После 24 часов: фактор срочности = 0.5
    # После 48 часов: фактор срочности = 0.25
    due_date_factor = 2 ** (-hours_until_due / 24)
    
    return due_date_factor

def calculate_duration_factor(task: Task) -> float:
    """
    Рассчитывает фактор на основе предполагаемой длительности.
    Более длительные задачи получают небольшой бонус к приоритету.
    """
    if not task.estimated_duration or task.estimated_duration <= 0:
        return 1.0  # Отсутствие длительности означает нейтральный фактор
    
    # Нормализация длительности к 24 часам
    duration_factor = 1.0 + (task.estimated_duration / 24.0) * 0.2  # Максимальный бонус 20%
    
    return duration_factor

def get_status_factor(status: str) -> float:
    """
    Получает множитель приоритета на основе статуса задачи.
    """
    status_factors = {
        "pending": 1.0,      # Ожидающие задачи
        "in_progress": 1.2,  # В процессе (повышенный приоритет)
        "blocked": 0.3,      # Заблокированные (значительно пониженный приоритет)
        "completed": 0.0     # Завершенные (исключаются)
    }
    return status_factors.get(status.lower(), 1.0)

def calculate_priority(task: Task) -> float:
    """
    Рассчитывает приоритет задачи на основе различных факторов:
    - Время с момента создания (срочность)
    - Срок выполнения (срочность дедлайна)
    - Предполагаемая длительность
    - Текущий статус
    - Пользовательский приоритет
    """
    # Базовый приоритет от пользователя (1-5)
    base_priority = task.priority

    # Временные факторы
    time_factor = calculate_time_factor(task.created_at)
    due_date_factor = calculate_due_date_factor(task)
    duration_factor = calculate_duration_factor(task)
    
    # Фактор статуса
    status_factor = get_status_factor(task.status)
    
    # Комбинируем все факторы
    # Используем умножение для time_factor и due_date_factor
    final_priority = base_priority * (1 + time_factor) * (1 + due_date_factor) * status_factor * duration_factor
    
    return final_priority

def sort_tasks_by_priority(tasks: List[Task]) -> List[Task]:
    """
    Сортирует задачи по их рассчитанному приоритету.
    """
    return sorted(
        tasks,
        key=lambda task: calculate_priority(task),
        reverse=True
    )