import streamlit as st

from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

# Initialize session state for persistent data across reruns
if "owner" not in st.session_state:
    st.session_state.owner = Owner("Pet Owner", contact_info="owner@email.com")

if "pets" not in st.session_state:
    st.session_state.pets = []

if "tasks" not in st.session_state:
    st.session_state.tasks = []

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("🐾 Add a Pet")
col1, col2 = st.columns(2)
with col1:
    new_pet_name = st.text_input("Pet name", value="Mochi", key="pet_name_input")
with col2:
    new_pet_species = st.selectbox("Species", ["dog", "cat", "other"], key="pet_species_input")

if st.button("Add pet to owner"):
    # Create a new Pet and add it to the owner using Phase 2 methods
    new_pet = Pet(name=new_pet_name, species=new_pet_species)
    st.session_state.owner.add_pet(new_pet)
    st.success(f"✅ Added {new_pet_name} the {new_pet_species} to your pet collection!")

# Display current pets
owner_pets = st.session_state.owner.get_pets()
if owner_pets:
    st.subheader(f"Your Pets ({len(owner_pets)})")
    for i, pet in enumerate(owner_pets):
        st.write(f"• **{pet.name}** ({pet.species.capitalize()}) - {len(pet.get_tasks())} tasks")
else:
    st.info("No pets yet. Add one above!")

st.divider()

st.subheader("✅ Add a Task")
st.caption("Select a pet and add a task for it.")

if owner_pets:
    selected_pet_name = st.selectbox(
        "Select pet",
        [pet.name for pet in owner_pets],
        key="pet_select"
    )
    selected_pet = next(p for p in owner_pets if p.name == selected_pet_name)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        task_description = st.text_input("Task description", value="Morning walk", key="task_desc_input")
    with col2:
        task_time = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20, key="task_time_input")
    with col3:
        task_frequency = st.selectbox("Frequency", ["daily", "weekly", "as-needed", "once"], key="task_freq_input")
    
    if st.button("Add task"):
        # Create a new Task and add it to the selected pet using Phase 2 methods
        new_task = Task(
            description=task_description,
            time=task_time,
            frequency=task_frequency
        )
        selected_pet.add_task(new_task)
        st.success(f"✅ Added '{task_description}' to {selected_pet_name}'s tasks!")
    
    # Display tasks for selected pet
    active_tasks = selected_pet.get_active_tasks()
    if active_tasks:
        st.write(f"**{selected_pet_name}'s Tasks ({len(active_tasks)})**")
        for i, task in enumerate(active_tasks, 1):
            st.write(f"{i}. {task.description} ({task.time} min, {task.frequency})")
else:
    st.warning("Add a pet first before adding tasks!")

st.divider()

st.subheader("📋 Build Schedule")
st.caption("Generate a daily schedule based on your pet's tasks.")

available_time = st.slider(
    "Available time today (minutes)",
    min_value=60,
    max_value=1440,
    value=480,
    step=30
)

if st.button("Generate schedule"):
    owner_pets = st.session_state.owner.get_pets()
    
    if not owner_pets:
        st.error("❌ No pets added yet!")
    else:
        all_tasks = []
        for pet in owner_pets:
            all_tasks.extend(pet.get_active_tasks())
        
        if not all_tasks:
            st.warning("⚠️ No tasks to schedule. Add tasks to your pets first!")
        else:
            # Use the Scheduler to generate a schedule
            scheduler = Scheduler(st.session_state.owner, available_time_minutes=int(available_time))
            scheduled_tasks = scheduler.generate_schedule(all_tasks)
            
            st.success(f"✅ Schedule generated for {len(owner_pets)} pet(s)!")
            
            # Display the schedule
            st.subheader("📅 Today's Schedule")
            
            total_time = 0
            for i, task in enumerate(scheduled_tasks, 1):
                st.write(f"{i}. **{task.description}** ({task.time} min, {task.frequency})")
                total_time += task.time
            
            st.info(f"⏱️ **Total time needed: {total_time} minutes ({total_time // 60}h {total_time % 60}m)**")
            
            # Show explanation if available
            if hasattr(scheduler, 'explain_schedule'):
                explanation = scheduler.explain_schedule(scheduled_tasks)
                if explanation:
                    st.write(explanation)
