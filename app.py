import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="wide")

# Persistent Session State
if "owner" not in st.session_state:
    st.session_state.owner = Owner("User", contact_info="user@email.com")

st.title("🐾 PawPal+ Care Planner")

# --- SIDEBAR: ADD PETS ---
with st.sidebar:
    st.header("🐶 Add a Pet")
    p_name = st.text_input("Name", placeholder="Mochi")
    p_species = st.selectbox("Species", ["Dog", "Cat", "Bird", "Other"])
    if st.button("Add Pet"):
        if p_name:
            new_pet = Pet(name=p_name, species=p_species)
            st.session_state.owner.add_pet(new_pet)
            st.success(f"Added {p_name}!")
        else:
            st.error("Please enter a name.")

# --- MAIN UI: ADD TASKS ---
owner_pets = st.session_state.owner.get_pets()

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📝 Add a Task")
    if owner_pets:
        target_pet_name = st.selectbox("Assign to:", [p.name for p in owner_pets])
        t_desc = st.text_input("What needs to be done?", placeholder="Feeding")
        t_time = st.number_input("Minutes", min_value=5, max_value=300, step=5, value=20)
        t_freq = st.selectbox("Frequency", ["Daily", "Weekly", "Once"])
        
        if st.button("Add Task"):
            target_pet = next(p for p in owner_pets if p.name == target_pet_name)
            target_pet.add_task(Task(description=t_desc, time=t_time, frequency=t_freq))
            st.toast(f"Task added for {target_pet_name}!")
    else:
        st.info("Add a pet in the sidebar first!")

with col2:
    st.subheader("📋 Current Pet List")
    for pet in owner_pets:
        st.write(f"**{pet.name}** ({pet.species}): {len(pet.get_tasks())} tasks")

st.divider()

# --- SCHEDULING ENGINE ---
st.subheader("📅 Generate Today's Schedule")
available_time = st.slider("Available time today (minutes)", 30, 720, 480)

if st.button("Build Optimized Plan"):
    if not owner_pets:
        st.error("No pets found.")
    else:
        scheduler = Scheduler(st.session_state.owner, available_time_minutes=available_time)
        all_tasks = scheduler.retrieve_all_tasks()
        
        if not all_tasks:
            st.warning("No active tasks found. Please add some above.")
        else:
            # The Logic Pipeline: Sort -> Fit
            sorted_tasks = scheduler.sort_by_time(all_tasks)
            final_plan = scheduler.fit_tasks_in_time(sorted_tasks)
            
            # Display results in a table
            st.success("Plan Generated!")
            display_data = [{"Task": t.description, "Duration": f"{t.time}m", "Freq": t.frequency} for t in final_plan]
            st.table(display_data)
            
            # Explanation Logic
            with st.expander("🔍 Why this schedule?"):
                st.write(scheduler.explain_schedule(final_plan))