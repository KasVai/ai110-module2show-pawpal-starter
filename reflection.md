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

I used to AI to help me understand parts of the code and help me navigate through any errors I encountered. Additionally, I used it to help me brainstorm and come up with ways to best optimize the code. The prompts that were most the helpful were the ones that we really specific in what I wanted to get. 

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

One moment where I did not accept an AI suggestion as it was when there was too much complications in the code. For example, the AI made the code more complicated than it needed it to be which was not as human-readable compared to more simple ways to solving something. For example, in one particular case the AI recommended using a couple different python packages to make things seemingly faster than just using a helper method. 

I verified what the AI suggested by implementing its recommendations and seeing if I was able to read and understand the code as a human. If I didn't understand, I asked it to implement more human-understable solutions. 
---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?

Some behaviors I tested incuding to see how the methods ran and how fast everything outputted. Some methods took more time than other depending on how the code was implemented. Additionally, I had to test to make sure all the functions were running propetly for all the different user actions. 

- Why were these tests important?

These tests were important because if they did not output the right result, it meant that there was something wrong with the functionality of the app. This would be a hinderance if someone was actually trying to use this application for themselves. 

**b. Confidence**

- How confident are you that your scheduler works correctly?

I am fairly confident that much scheduler works correctly as it has both AI and human feedback to help optimize. 

- What edge cases would you test next if you had more time?

If I more time, some edge I would test would include Daylights Savings Time and how I would make the timings reflect that. 
Additionally, I would also like to be able to add multiple owners just as I added multiple pets. 

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I am satisfied with how the app looks and functions as it covers the basics of what a user with a pet would need and use. 

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

If I had another iteration, I would improve the timing aspects of the app. For example, I would add multiple time zones so that it reflects the time zone that user is in and not just Standard TIme. 

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

One important thing I learned designing systems includes the importance of having a well-thought out plan. Once the plan is in face, then it is much easier to implement everything since everything is accounted for. Additionally, I also learned that AI may not always give the best suggestions and it is important to filter through to see which one is the most optimal. 