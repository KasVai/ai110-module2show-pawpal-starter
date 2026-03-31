from dataclasses import dataclass, field
from typing import List, Optional, Dict


@dataclass
class Task:
    """Represents a pet care task."""
    description: str
    time: int
    frequency: str 
    completion_status: bool = False
    
    def update_time(self, minutes: int) -> None:
        """Update the task time."""
        self.time = minutes
    
    def mark_completed(self) -> None:
        """Mark the task as completed."""
        self.completion_status = True


@dataclass
class Pet:
    """Represents a pet owned by an owner."""
    name: str
    species: str
    tasks: List[Task] = field(default_factory=list)  
    owner: Optional['Owner'] = None
    
    def add_task(self, task: Task) -> None:
        """Add a task to the pet's task list."""
        self.tasks.append(task)
    
    def remove_task(self, task_id: int) -> None:
        """Remove a task by index."""
        if 0 <= task_id < len(self.tasks):
            self.tasks.pop(task_id)
    
    def get_tasks(self) -> List[Task]:
        """Get all tasks for this pet."""
        return self.tasks
    
    def get_active_tasks(self) -> List[Task]:
        """Get only incomplete tasks."""
        return [task for task in self.tasks if not task.completion_status]


class Owner:
    """Represents a pet owner."""
    
    def get_all_tasks(self) -> List[Task]:
        """Get all tasks across all owned pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks

    def __init__(self, name: str, contact_info: str = "", preferences: Dict = None):
        """Initialize an owner with name, contact info, and preferences."""
        self.name = name
        self.contact_info = contact_info
        self.preferences = preferences or {}
        self.pets: List[Pet] = []
    
    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's collection."""
        self.pets.append(pet)
        pet.owner = self
    
    def remove_pet(self, pet_id: int) -> None:
        """Remove a pet by index."""
        if 0 <= pet_id < len(self.pets):
            pet = self.pets.pop(pet_id)
            pet.owner = None
    
    def get_pets(self) -> List[Pet]:
        """Get all pets owned by this owner."""
        return self.pets


class Scheduler:
    """Handles scheduling logic for pet care tasks."""
    
    def __init__(self, owner: Owner, available_time_minutes: int = 480):
        """Initialize scheduler with an owner and available daily time in minutes."""
        self.owner = owner
        self.available_time_minutes = available_time_minutes
    
    def retrieve_all_tasks(self) -> List[Task]:
        """Retrieve all tasks from all owner's pets."""
        all_tasks = []
        for pet in self.owner.pets:
            all_tasks.extend(pet.get_active_tasks())
        return all_tasks
    def generate_schedule(self, tasks: List[Task]) -> List[Task]:
        """Generate a daily schedule by prioritizing and fitting tasks."""
        pass
    
    def rank_tasks_by_priority(self, tasks: List[Task]) -> List[Task]:
        """Rank tasks by priority level."""
        pass
    
    def explain_schedule(self, scheduled_tasks: List[Task]) -> str:
        """Generate an explanation for why tasks were scheduled."""
        pass
    
    def fit_tasks_in_time(self, tasks: List[Task]) -> List[Task]:
        """Fit tasks within available time constraints."""
        pass
