"""
Syna Python Wrapper

A high-level Python interface for the Syna embedded database.

Example:
    >>> from Syna import SynaDB
    >>> with SynaDB("my.db") as db:
    ...     db.put_float("temperature", 23.5)
    ...     print(db.get_float("temperature"))
    23.5

For RL experience collection:
    >>> from Syna import ExperienceCollector
    >>> collector = ExperienceCollector("exp.db", machine_id="gpu_server_1")
    >>> collector.log_transition(state, action, reward, next_state)
"""

from .wrapper import SynaDB, SynaError
from .experience import ExperienceCollector, Transition, SessionContext

__version__ = "0.1.0"
__all__ = [
    "SynaDB",
    "SynaError",
    "ExperienceCollector",
    "Transition",
    "SessionContext",
]

