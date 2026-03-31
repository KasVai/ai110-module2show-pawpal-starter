# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
Classes: 
    - Task: Represents each pet care task, where user can update task priority, update the task duration, and mark task as completed. 

    - Pet: Represents a pet owned by an owner, where user can add task to list, remove a task by index, get all tasks for pet. 

    - Owner: Represents pet owner where user can add pet to owner's collection, remove pet by index, and get all pets by by this owner. 

    - Scheduler: Handles schedulign logic for pet care tasks including generating daily schedule. 


It will have classes, attributes, methods, and relationships. 

Attributes: The information it needs to hold are owner information, pet information, specific pet tasks. 

Methods: The actions that it can perform are produce a daily plan/schedule + explaination, let a user add or delete pet care tasks, and be able to track pet care tasks. 

Relationships: 
- owner has pets
- pets have tasks 

Natural Language: 
Three Core Actions User Should Be Able to Perform: 
1) Enter basic owner and pet information 
2) Add or delete tasks at their own will, specifically the duration and the priority. 
3) Track pet care tasks such as walks, feeding, meds, enrichment, grooming, etc.

- What classes did you include, and what responsibilities did you assign to each?

1) Owner: 
2) Pet: 
3) Task: 
4) Scheduler: 

**b. Design changes**

- Did your design change during implementation?

Yes, my design did change during implmentation as per the AI suggestion. 

- If yes, describe at least one change and why you made it.

I changed the biodirectional linking in Owner so whe nyou add a pet to the an owner, it sets the that pet's owner field back to the owner. There was an issue where the owner thinks they have the pet, but the pet doesn't know who owns it. So now printing owner.pets will print the pet name while pet.owner will print the owner name. 

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

Some contraints that my scheduler considered included time and frequency and I decided the time would be the most important. It is important for owner to follow the specific time limits for each task without going beyond bounds. Frequency is also important because tasks like feeding cannot only occur once. 

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

One tradeoff my scheudler makes is showing warnings instead of stopping the whole program. This allows any problems to show at once and it also allows to make decisions on their own terms. Another tradeoff the the specific scheduling which is reasonable because enables for beyyer speed and clairty. 
---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
