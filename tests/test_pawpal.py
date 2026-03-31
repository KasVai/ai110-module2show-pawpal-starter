import pytest
from datetime import datetime, timedelta
from pawpal_system import Task, Pet, Owner, Scheduler


class TestTaskCompletion:
    """Test Task completion functionality."""
    
    def test_mark_completed_changes_status(self):
        """Verify that calling mark_completed() actually changes the task's status."""
        # Arrange: Create a task with incomplete status
        task = Task(
            description="Morning walk",
            time=30,
            frequency="daily"
        )
        assert task.completion_status == False  # Initially incomplete
        
        # Act: Mark the task as completed
        task.mark_completed()
        
        # Assert: Verify the status changed
        assert task.completion_status == True


class TestTaskAddition:
    """Test Task addition to Pet functionality."""
    
    def test_add_task_increases_pet_task_count(self):
        """Verify that adding a task to a Pet increases that pet's task count."""
        # Arrange: Create a pet with no tasks
        pet = Pet(name="Mochi", species="dog")
        assert len(pet.get_tasks()) == 0  # Initially no tasks
        
        # Act: Add a task to the pet
        task = Task(
            description="Feeding",
            time=10,
            frequency="daily"
        )
        pet.add_task(task)
        
        # Assert: Verify task was added
        assert len(pet.get_tasks()) == 1
        assert pet.get_tasks()[0] == task


class TestSortingCorrectness:
    """Test Task sorting by duration."""
    
    def test_sort_by_time_ascending(self):
        """Verify tasks are sorted in ascending order by duration (shortest first)."""
        # Arrange: Create tasks with different durations in random order
        task1 = Task(description="Long task", time=50, frequency="daily")
        task2 = Task(description="Short task", time=10, frequency="daily")
        task3 = Task(description="Medium task", time=30, frequency="daily")
        tasks = [task1, task2, task3]
        
        owner = Owner(name="Alice")
        scheduler = Scheduler(owner)
        
        # Act: Sort tasks in ascending order
        sorted_tasks = scheduler.sort_by_time(tasks, reverse=False)
        
        # Assert: Verify tasks are in ascending order by time
        assert sorted_tasks[0].time == 10
        assert sorted_tasks[1].time == 30
        assert sorted_tasks[2].time == 50
    
    def test_sort_by_time_descending(self):
        """Verify tasks are sorted in descending order by duration (longest first)."""
        # Arrange: Create tasks with different durations
        task1 = Task(description="Long task", time=50, frequency="daily")
        task2 = Task(description="Short task", time=10, frequency="daily")
        task3 = Task(description="Medium task", time=30, frequency="daily")
        tasks = [task1, task2, task3]
        
        owner = Owner(name="Alice")
        scheduler = Scheduler(owner)
        
        # Act: Sort tasks in descending order
        sorted_tasks = scheduler.sort_by_time(tasks, reverse=True)
        
        # Assert: Verify tasks are in descending order by time
        assert sorted_tasks[0].time == 50
        assert sorted_tasks[1].time == 30
        assert sorted_tasks[2].time == 10


class TestRecurrenceLogic:
    """Test Task recurrence auto-generation on completion."""
    
    def test_daily_task_recurrence(self):
        """Confirm that marking a daily task complete creates a new task for the following day."""
        # Arrange: Create a pet and add a daily task with a specific due date
        pet = Pet(name="Mochi", species="dog")
        today = datetime(2026, 3, 31, 10, 0)  # March 31, 2026 at 10:00 AM
        
        task = Task(
            description="Morning walk",
            time=30,
            frequency="daily",
            priority="high",
            due_date=today
        )
        pet.add_task(task)
        initial_task_count = len(pet.get_tasks())
        
        # Act: Mark the task as completed
        task.mark_completed()
        
        # Assert: Verify original task is marked complete
        assert task.completion_status == True
        
        # Assert: Verify a new task was created
        assert len(pet.get_tasks()) == initial_task_count + 1
        
        # Assert: Verify the new task has correct properties
        new_task = pet.get_tasks()[-1]
        assert new_task.description == "Morning walk"
        assert new_task.time == 30
        assert new_task.frequency == "daily"
        assert new_task.priority == "high"
        
        # Assert: Verify the new task has tomorrow's due date
        expected_next_date = today + timedelta(days=1)
        assert new_task.due_date == expected_next_date
    
    def test_weekly_task_recurrence(self):
        """Confirm that marking a weekly task complete creates a new task 7 days later."""
        # Arrange: Create a pet and add a weekly task
        pet = Pet(name="Whiskers", species="cat")
        today = datetime(2026, 3, 31, 14, 0)  # March 31, 2026 at 2:00 PM
        
        task = Task(
            description="Grooming",
            time=45,
            frequency="weekly",
            priority="medium",
            due_date=today
        )
        pet.add_task(task)
        
        # Act: Mark the task as completed
        task.mark_completed()
        
        # Assert: Verify new task was created with due date 7 days later
        new_task = pet.get_tasks()[-1]
        expected_next_date = today + timedelta(days=7)
        assert new_task.due_date == expected_next_date
        assert new_task.frequency == "weekly"


class TestConflictDetection:
    """Test Scheduler conflict detection for overlapping tasks."""
    
    def test_detect_same_time_conflicts(self):
        """Verify that the Scheduler flags tasks scheduled at duplicate times."""
        # Arrange: Create owner, pets, and tasks at overlapping times
        owner = Owner(name="Alice")
        dog = Pet(name="Mochi", species="dog")
        cat = Pet(name="Whiskers", species="cat")
        owner.add_pet(dog)
        owner.add_pet(cat)
        
        # Same time for both pets
        same_time = datetime(2026, 3, 31, 10, 0)  # 10:00 AM
        
        dog_task = Task(
            description="Playtime",
            time=20,
            frequency="daily",
            due_date=same_time
        )
        cat_task = Task(
            description="Feeding",
            time=10,
            frequency="daily",
            due_date=same_time
        )
        
        dog.add_task(dog_task)
        cat.add_task(cat_task)
        
        scheduler = Scheduler(owner)
        all_tasks = [dog_task, cat_task]
        
        # Act: Detect conflicts
        conflicts = scheduler.detect_time_conflicts(all_tasks)
        
        # Assert: Verify conflicts are detected
        assert conflicts["has_conflicts"] == True
        assert conflicts["count"] == 1  # One overlap pair
        assert len(conflicts["warnings"]) == 1
        assert "OVERLAP" in conflicts["warnings"][0]
    
    def test_detect_no_conflicts(self):
        """Verify that the Scheduler returns no conflicts for non-overlapping tasks."""
        # Arrange: Create tasks at different times on the same day
        owner = Owner(name="Alice")
        pet = Pet(name="Mochi", species="dog")
        owner.add_pet(pet)
        
        task1 = Task(
            description="Morning walk",
            time=30,
            frequency="daily",
            due_date=datetime(2026, 3, 31, 9, 0)  # 9:00 AM
        )
        task2 = Task(
            description="Feeding",
            time=15,
            frequency="daily",
            due_date=datetime(2026, 3, 31, 12, 0)  # 12:00 PM
        )
        
        pet.add_task(task1)
        pet.add_task(task2)
        
        scheduler = Scheduler(owner)
        all_tasks = [task1, task2]
        
        # Act: Detect conflicts
        conflicts = scheduler.detect_time_conflicts(all_tasks)
        
        # Assert: Verify no conflicts are detected
        assert conflicts["has_conflicts"] == False
        assert conflicts["count"] == 0
        assert len(conflicts["warnings"]) == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
