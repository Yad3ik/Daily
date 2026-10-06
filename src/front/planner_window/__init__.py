"""Главное окно планировщика."""

__all__ = ["PlannerWindow"]


def __getattr__(name: str):
    """Ленивый импорт PlannerWindow по имени из __all__."""
    if name == "PlannerWindow":
        from .planner_window import PlannerWindow

        return PlannerWindow
    raise AttributeError(name)
