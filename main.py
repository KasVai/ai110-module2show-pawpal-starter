from pawpal_system import Owner, Pet, Task


def main():
    # Create an Owner
    owner = Owner("Alice Johnson", contact_info="alice@email.com")
    
    # Create Pets and add them to the Owner
    dog = Pet("Mochi", "dog")
    cat = Pet("Whiskers", "cat")
    
    owner.add_pet(dog)
    owner.add_pet(cat)
    
    # Create Tasks for the dog
    dog_walk = Task(
        description="Morning walk",
        time=30,
        frequency="daily"
    )
    dog_feed = Task(
        description="Breakfast",
        time=10,
        frequency="daily"
    )
    dog_play = Task(
        description="Playtime",
        time=20,
        frequency="daily"
    )
    
    dog.add_task(dog_walk)
    dog.add_task(dog_feed)
    dog.add_task(dog_play)
    
    # Create Tasks for the cat
    cat_feed = Task(
        description="Breakfast",
        time=5,
        frequency="daily"
    )
    cat_litter = Task(
        description="Clean litter box",
        time=10,
        frequency="daily"
    )
    cat_groom = Task(
        description="Grooming",
        time=15,
        frequency="daily"
    )
    
    cat.add_task(cat_feed)
    cat.add_task(cat_litter)
    cat.add_task(cat_groom)
    
    # Print Today's Schedule
    print("=" * 60)
    print("🐾 TODAY'S SCHEDULE FOR", owner.name.upper())
    print("=" * 60)
    print()
    
    total_time = 0
    
    for pet in owner.get_pets():
        print(f"📋 {pet.name.upper()} ({pet.species.capitalize()})")
        print("-" * 60)
        
        tasks = pet.get_active_tasks()
        for i, task in enumerate(tasks, 1):
            print(f"  {i}. {task.description}")
            print(f"     ⏱️  Duration: {task.time} minutes")
            print(f"     🔄 Frequency: {task.frequency}")
            total_time += task.time
        
        print()
    
    print("=" * 60)
    print(f"📊 TOTAL TIME NEEDED: {total_time} minutes ({total_time // 60}h {total_time % 60}m)")
    print("=" * 60)


if __name__ == "__main__":
    main()
