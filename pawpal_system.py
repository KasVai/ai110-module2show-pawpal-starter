from dataclasses import dataclass, field
from typing import List, Optional, Dict
from datetime import datetime, timedelta


@dataclass
class Task:
    """Represents a pet care task."""
    description: str
    time: int
    frequency: str 
    completion_status: bool = False
    priority: str = "medium"
    preferred_time: str = "anytime"
    pet: Optional['Pet'] = None
    due_date: Optional[datetime] = None
    
    def __post_init__(self):
        """Initialize due_date to today if not provided."""
        if self.due_date is None:
            self.due_date = datetime.now()
    
    def update_time(self, minutes: int) -> None:
        """Update the task time."""
        self.time = minutes
    
    def mark_completed(self) -> None:
        """Mark task complete and auto-create next occurrence with updated due date."""
        self.completion_status = True
        if self.pet and self.frequency.lower() in ["daily", "weekly"]:
            # Calculate next due date
            days_offset = 1 if self.frequency.lower() == "daily" else 7
            next_due = self.due_date + timedelta(days=days_offset)
            # Create next task with updated due date
            next_task = Task(
                description=self.description,
                time=self.time,
                frequency=self.frequency,
                priority=self.priority,
                preferred_time=self.preferred_time,
                due_date=next_due
            )
            self.pet.add_task(next_task)


@dataclass
class Pet:
    """Represents a pet owned by an owner."""
    name: str
    species: str
    tasks: List[Task] = field(default_factory=list)  
    owner: Optional['Owner'] = None
    
    def add_task(self, task: Task) -> None:
        """Add a task to the pet's task list and set pet reference."""
        self.tasks.append(task)
        task.pet = self
    
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
    
    def sort_by_time(self, tasks: List[Task], reverse: bool = False) -> List[Task]:
        """
        Sorts tasks based on the 'time' attribute.
        Default is ascending (shortest tasks first).
        Set reverse=True for descending (longest tasks first).
        """
        return sorted(tasks, key=lambda task: task.time, reverse=reverse)
    
    def filter_by_pet(self, pet_name: str) -> List[Task]:
        """Returns all tasks belonging to a specific pet by name."""
        all_tasks = []
        for pet in self.owner.pets:
            if pet.name.lower() == pet_name.lower():
                all_tasks.extend(pet.get_tasks())
        return all_tasks
    
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
        """Rank tasks by priority level (high to low)."""
        priority_map = {"low": 1, "medium": 2, "high": 3}
        return sorted(tasks, key=lambda t: priority_map.get(t.priority, 2), reverse=True)
    
    def detect_conflicts(self, tasks: List[Task]) -> dict:
        """Detect if tasks exceed available time."""
        total = sum(t.time for t in tasks)
        return {"total_time": total, "exceeds": total > self.available_time_minutes, "overflow": max(0, total - self.available_time_minutes)}
    
    def detect_time_conflicts(self, tasks: List[Task]) -> dict:
        """Lightweight detection: find overlapping tasks by comparing due_date + duration."""
        conflicts = {"has_conflicts": False, "warnings": [], "count": 0}
        
        for i, task1 in enumerate(tasks):
            for task2 in tasks[i+1:]:
                # Check if tasks are on same day
                if task1.due_date.date() == task2.due_date.date():
                    # Calculate start and end times in minutes from midnight
                    t1_start_min = task1.due_date.hour * 60 + task1.due_date.minute
                    t1_end_min = t1_start_min + task1.time
                    t2_start_min = task2.due_date.hour * 60 + task2.due_date.minute
                    t2_end_min = t2_start_min + task2.time
                    
                    # Check for time overlap
                    if t1_start_min < t2_end_min and t2_start_min < t1_end_min:
                        conflicts["has_conflicts"] = True
                        conflicts["count"] += 1
                        pet1_name = task1.pet.name if task1.pet else "Unknown"
                        pet2_name = task2.pet.name if task2.pet else "Unknown"
                        t1_time_str = task1.due_date.strftime('%H:%M')
                        t2_time_str = task2.due_date.strftime('%H:%M')
                        warning = f"⚠️ OVERLAP: {pet1_name} '{task1.description}' ({t1_time_str}) ↔ {pet2_name} '{task2.description}' ({t2_time_str})"
                        conflicts["warnings"].append(warning)
        
        return conflicts
    
    def generate_schedule(self, tasks: List[Task]) -> List[Task]:
        """Generate optimized schedule by priority, fitting within time."""
        ranked = self.rank_tasks_by_priority(tasks)
        scheduled, total = [], 0
        for task in ranked:
            if total + task.time <= self.available_time_minutes:
                scheduled.append(task)
                total += task.time
        return scheduled
    
    def explain_schedule(self, scheduled_tasks: List[Task]) -> str:
        """Generate an explanation for the schedule."""
        total = sum(t.time for t in scheduled_tasks)
        lines = ["📅 Generated Schedule:"] + [f"  {i}. {t.description} ({t.time}m - {t.priority})" for i, t in enumerate(scheduled_tasks, 1)]
        lines.append(f"\nTotal Time: {total}m / Available: {self.available_time_minutes}m")
        if total > self.available_time_minutes:
            lines.append(f"⚠️  Overbooked by {total - self.available_time_minutes}m")
        else:
            lines.append(f"✓ Free time: {self.available_time_minutes - total}m")
        return "\n".join(lines)
    
    def fit_tasks_in_time(self, tasks: List[Task]) -> List[Task]:
        """Fit tasks within available time constraints."""
        return self.generate_schedule(tasks)
