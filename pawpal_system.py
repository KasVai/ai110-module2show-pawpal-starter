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
        self.time = minutes
    
    def mark_completed(self) -> None:
        self.completion_status = True
        
    def reset_status(self) -> None:
        """Resets the task for recurring schedules."""
        self.completion_status = False

@dataclass
class Pet:
    """Represents a pet owned by an owner."""
    name: str
    species: str
    tasks: List[Task] = field(default_factory=list)  
    owner: Optional['Owner'] = None
    
    def add_task(self, task: Task) -> None:
        self.tasks.append(task)
    
    def get_tasks(self) -> List[Task]:
        return self.tasks
    
    def get_active_tasks(self) -> List[Task]:
        return [task for task in self.tasks if not task.completion_status]

class Owner:
    """Represents a pet owner."""
    def __init__(self, name: str, contact_info: str = "", preferences: Dict = None):
        self.name = name
        self.contact_info = contact_info
        self.preferences = preferences or {}
        self.pets: List[Pet] = []
    
    def add_pet(self, pet: Pet) -> None:
        self.pets.append(pet)
        pet.owner = self
        
    def get_pets(self) -> List[Pet]:
        return self.pets

class Scheduler:
    """Handles scheduling logic, sorting, and filtering."""
    def __init__(self, owner: Owner, available_time_minutes: int = 480):
        self.owner = owner
        self.available_time_minutes = available_time_minutes

    def retrieve_all_tasks(self) -> List[Task]:
        """Gathers all active tasks from all pets."""
        all_tasks = []
        for pet in self.owner.pets:
            all_tasks.extend(pet.get_active_tasks())
        return all_tasks

    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        """Sorts tasks by duration (shortest first)."""
        return sorted(tasks, key=lambda x: x.time)

    def filter_by_pet(self, pet_name: str) -> List[Task]:
        """Filters tasks for a specific pet."""
        for pet in self.owner.pets:
            if pet.name.lower() == pet_name.lower():
                return pet.get_tasks()
        return []

    def fit_tasks_in_time(self, tasks: List[Task]) -> List[Task]:
        """Greedy algorithm to fit tasks into the available time window."""
        scheduled = []
        used_time = 0
        for task in tasks:
            if used_time + task.time <= self.available_time_minutes:
                scheduled.append(task)
                used_time += task.time
        return scheduled

    def explain_schedule(self, scheduled_tasks: List[Task]) -> str:
        """Explains the scheduling logic used."""
        if not scheduled_tasks:
            return "No tasks could be scheduled within the time limit."
        
        total_tasks = len(self.retrieve_all_tasks())
        scheduled_count = len(scheduled_tasks)
        
        explanation = f"I prioritized the shortest tasks first to maximize your productivity. "
        explanation += f"Out of {total_tasks} total tasks, I successfully fit {scheduled_count} "
        explanation += f"into your {self.available_time_minutes}-minute window."
        return explanation