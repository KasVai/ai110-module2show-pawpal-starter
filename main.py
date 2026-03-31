from pawpal_system import Owner, Pet, Task, Scheduler


def main():
    # Create an Owner
    owner = Owner("Alice Johnson", contact_info="alice@email.com")
    
    # Create Pets and add them to the Owner
    dog = Pet("Mochi", "dog")
    cat = Pet("Whiskers", "cat")
    
    owner.add_pet(dog)
    owner.add_pet(cat)
    
    # Create base date/time for tasks
    from datetime import datetime, timedelta
    today = datetime.now()
    morning_9am = today.replace(hour=9, minute=0, second=0, microsecond=0)
    morning_9_15am = today.replace(hour=9, minute=15, second=0, microsecond=0)  # Overlaps with walk
    morning_10am = today.replace(hour=10, minute=0, second=0, microsecond=0)
    afternoon_2pm = today.replace(hour=14, minute=0, second=0, microsecond=0)
    afternoon_3pm = today.replace(hour=15, minute=0, second=0, microsecond=0)
    
    # Add tasks with specific times - some intentionally overlap to demonstrate conflict detection
    dog.add_task(Task("Morning walk", 30, "daily", priority="high", due_date=morning_9am))
    dog.add_task(Task("Feeding", 15, "daily", priority="high", due_date=morning_9_15am))  # OVERLAPS!
    dog.add_task(Task("Playtime", 20, "daily", priority="medium", due_date=morning_10am))
    
    # TWO TASKS AT EXACT SAME TIME - this will definitely trigger conflict warning!
    cat.add_task(Task("Feeding", 10, "daily", priority="medium", due_date=morning_10am))  # SAME TIME as Playtime!
    cat.add_task(Task("Stretching", 5, "daily", priority="low", due_date=morning_10am))  # ALSO SAME TIME!
    
    cat.add_task(Task("Clean litter box", 10, "daily", priority="high", due_date=afternoon_2pm))
    cat.add_task(Task("Grooming", 15, "weekly", priority="low", due_date=afternoon_3pm))
    
    scheduler = Scheduler(owner, available_time_minutes=480)
    all_tasks = scheduler.retrieve_all_tasks()
    
    print("=" * 70)
    print("🐾 PawPal+ SCHEDULING DEMO - Sorting & Filtering Tests")
    print("=" * 70)
    
    # 1. Show original order (OUT OF ORDER)
    print("\n📋 TASKS IN ORIGINAL ORDER (Added out of order):")
    print("-" * 70)
    for pet in owner.get_pets():
        print(f"\n{pet.name.upper()} tasks:")
        for task in pet.get_active_tasks():
            print(f"  • {task.description}: {task.time}m")
    
    # 2. Sort by time (shortest to longest)
    print("\n" + "=" * 70)
    print("⏱️  SORTED BY TIME (Shortest to Longest):")
    print("-" * 70)
    sorted_short = scheduler.sort_by_time(all_tasks, reverse=False)
    for task in sorted_short:
        print(f"  • {task.description}: {task.time}m")
    
    # 3. Sort by time (longest to shortest)
    print("\n" + "=" * 70)
    print("⏱️  SORTED BY TIME (Longest to Shortest):")
    print("-" * 70)
    sorted_long = scheduler.sort_by_time(all_tasks, reverse=True)
    for task in sorted_long:
        print(f"  • {task.description}: {task.time}m")
    
    # 4. Rank by priority
    print("\n" + "=" * 70)
    print("⭐ RANKED BY PRIORITY (High → Medium → Low):")
    print("-" * 70)
    ranked = scheduler.rank_tasks_by_priority(all_tasks)
    for task in ranked:
        print(f"  • {task.description}: {task.priority.upper()}")
    
    # 5. Filter by pet
    print("\n" + "=" * 70)
    print("🐕 FILTER BY PET - Mochi's tasks:")
    print("-" * 70)
    dog_tasks = scheduler.filter_by_pet("Mochi")
    for task in dog_tasks:
        print(f"  • {task.description} ({task.time}m)")
    
    print("\n🐱 FILTER BY PET - Whiskers' tasks:")
    print("-" * 70)
    cat_tasks = scheduler.filter_by_pet("Whiskers")
    for task in cat_tasks:
        print(f"  • {task.description} ({task.time}m)")
    
    # 6. HIGHLIGHT: Tasks scheduled at the EXACT SAME TIME
    print("\n" + "=" * 70)
    print("⏰ SAME-TIME TASKS (Scheduled at exact same start time):")
    print("-" * 70)
    same_time_tasks = {}
    for task in all_tasks:
        time_key = task.due_date.strftime('%H:%M')
        if time_key not in same_time_tasks:
            same_time_tasks[time_key] = []
        same_time_tasks[time_key].append(task)
    
    for time_slot in sorted(same_time_tasks.keys()):
        tasks_at_time = same_time_tasks[time_slot]
        if len(tasks_at_time) > 1:
            print(f"\n⚠️  {time_slot} - {len(tasks_at_time)} tasks at exact same time:")
            for task in tasks_at_time:
                pet_name = task.pet.name if task.pet else "Unknown"
                print(f"    • {pet_name}: '{task.description}' ({task.time}m)")
    
    # 7. Time-based conflict detection
    print("\n" + "=" * 70)
    print("⚠️  TIME-BASED CONFLICT DETECTION:")
    print("-" * 70)
    time_conflicts = scheduler.detect_time_conflicts(all_tasks)
    if time_conflicts["has_conflicts"]:
        print(f"Found {time_conflicts['count']} time overlap(s)!\n")
        for warning in time_conflicts["warnings"]:
            print(f"  {warning}")
    else:
        print("✓ No time conflicts - all tasks have non-overlapping times!")
    
    # 8. Time allocation check
    print("\n" + "=" * 70)
    print("📊 TIME ALLOCATION ANALYSIS:")
    print("-" * 70)
    conflicts = scheduler.detect_conflicts(all_tasks)
    total_time = conflicts["total_time"]
    print(f"Total task time: {total_time}m")
    print(f"Available time: {scheduler.available_time_minutes}m")
    if conflicts["exceeds"]:
        print(f"❌ EXCEEDS by {conflicts['overflow']}m")
    else:
        print(f"✓ Fits! (Free: {scheduler.available_time_minutes - total_time}m)")
    
    # 9. Display tasks with times
    print("\n" + "=" * 70)
    print("📅 TASKS WITH SCHEDULED TIMES:")
    print("-" * 70)
    for task in sorted(all_tasks, key=lambda t: t.due_date):
        duration_end = (task.due_date + timedelta(minutes=task.time)).strftime('%H:%M')
        print(f"  • {task.due_date.strftime('%H:%M')}-{duration_end} ({task.time}m): {task.description} ({task.pet.name})")
    
    # 10. Generate optimized schedule
    print("\n" + "=" * 70)
    schedule = scheduler.generate_schedule(all_tasks)
    print(scheduler.explain_schedule(schedule))
    print("=" * 70)
    
    # 11. RECURRING TASK DEMO - Auto-create next occurrence with updated due date
    print("\n" + "=" * 70)
    print("🔄 RECURRING TASK DEMO - Auto-Create Next Occurrence with Due Date")
    print("=" * 70)
    
    # Find a daily task to mark as complete
    daily_feed = dog.get_active_tasks()[0]  # Get first task (Feeding)
    print(f"\nBEFORE marking '{daily_feed.description}' complete:")
    print(f"  Task count: {len(dog.get_tasks())}")
    print(f"  Due date: {daily_feed.due_date.strftime('%Y-%m-%d %I:%M %p')}")
    print(f"  Tasks: {[t.description for t in dog.get_tasks()]}")
    
    # Mark the daily task as complete - should auto-create next occurrence with tomorrow's date
    print(f"\n→ Marking '{daily_feed.description}' as complete...")
    daily_feed.mark_completed()
    
    print(f"\nAFTER marking complete:")
    print(f"  Task count: {len(dog.get_tasks())}")
    
    # Find the new task
    new_daily = [t for t in dog.get_tasks() if not t.completion_status and t.description == daily_feed.description][0]
    print(f"\n  Original task:")
    print(f"    • Description: {daily_feed.description}")
    print(f"    • Due date: {daily_feed.due_date.strftime('%Y-%m-%d')}")
    print(f"    • Status: ✓ Completed")
    print(f"\n  New auto-created task:")
    print(f"    • Description: {new_daily.description}")
    print(f"    • Due date: {new_daily.due_date.strftime('%Y-%m-%d')} (today + 1 day)")
    print(f"    • Status: ⏳ Pending")
    print(f"    • Frequency: {new_daily.frequency}")
    print(f"    • Priority: {new_daily.priority}")
    
    # Verify the date calculation
    from datetime import timedelta
    expected_date = daily_feed.due_date + timedelta(days=1)
    date_match = new_daily.due_date.date() == expected_date.date()
    print(f"\n  ✓ Date calculation verified: {date_match}")
    print("=" * 70)


if __name__ == "__main__":
    main()
