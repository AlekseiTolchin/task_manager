from enum import Enum


class TaskStatus(str, Enum):
    CREATED = 'создана'
    IN_PROGRESS = 'в работе'
    COMPLETED = 'завершена'
