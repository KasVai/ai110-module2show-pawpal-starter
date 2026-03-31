import pytest
from pawpal_system import Task, Pet, Owner


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


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
