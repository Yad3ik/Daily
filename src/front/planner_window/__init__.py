__all__ = ["PlannerWindow"]


def __getattr__(name: str):
    if name == "PlannerWindow":
        from .planner_window import PlannerWindow

        return PlannerWindow
    raise AttributeError(name)
