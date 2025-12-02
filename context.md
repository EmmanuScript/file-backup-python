Project Information
Welcome!
Welcome to the Ambiguous Coding Task project. This initiative focuses on enhancing AI’s capacity for multi-turn reasoning within real-world codebases; improving its ability to interpret context, synthesize evidence, and execute complex software engineering tasks accurately.

Before completing any tasks, you’re required to read this full instructions document to understand the project and your role.

This data will be instrumental in training and improving a model that is used by millions around the world. For this reason, all experts on this project will be held to high quality standards at all times.

Once you work through the onboarding, training, and instructions tabs, you’ll receive access to project tooling and can start working!

If you are new to Mercor, read through the linked page below to gain a better understanding of who we are and what we do:
What is Mercor?
Expectations
AI usage: If you plan to use an LLM as part of your workflow, you must exclusively use Claude. Any time spent using other LLMs will be deducted from your time worked. Furthermore, you should write prompts on your own and you should be creating the instructions and conducting the evaluations yourself as well.
Work hours: We expect a minimum of 10-15 hours of work per week. However, you can work up to 40+ hours per week if you (1) do high-quality work and (2) have the time!
Confidentiality: You are not allowed to publicly disclose the work you are doing on this project. Please see Mercor’s FAQs to see what you are allowed to share now that you’ve signed your confidentiality agreement

Project Onboarding
These are general instructions on how to access everything that’s needed for the project.

Step 1: Setup Insightful
Look out for an email with instructions to set up Insightful
Any time spent working on the project should be logged on Insightful.
If you forget to enable Insightful while working on this project at any point, we will be unable to manually add your hours to insightful.
Log only active project work hours; idle time and non-project work will be reviewed and adjusted on a weekly basis. Training is included, so activate Insightful as you work through your project training
If you are not sharing the window on Insightful that you are actively contributing through and there is not clear proof of work during that period we will assume non-project work is being logged and adjust accordingly

Step 2: Join Slack
Join our project’s Slack workspace by email invitation. Ensure that your slack name is {First Name} {Last Name} - SWE.
E.g., Charlie Brown would become “Charlie Brown - SWE”

Step 3: Complete Project Training
Please read through this entire document in detail before beginning any work.

Step 4: Attend Onboarding Meeting
After fully reading through the instructions document, you are required to attend a project onboarding meeting before you may begin working on this project. This is where you can ask any questions, get support for issues, and let us know how we can support you (e.g. improving the clarity of the onboarding process)

Step 5: Begin Working!
Once you’ve completed the training, you will receive access to the model interface and can begin working on your first task. Then you can start contributing to the Ambiguous Coding Task project!

Main Objectives
In this project, annotators will present the model with coding tasks that contain various levels and types of ambiguity. The goal is to evaluate and train the model’s ability to:
Detect ambiguity in requirements
Ask good clarifying questions
Make reasonable assumptions when appropriate
Refuse or push back on impossible/unreasonable requests
Unlike straightforward coding tasks, the ideal response involves the model making a reasonable attempt at interpretation while explicitly stating assumptions and asking specific clarifying questions, rather than blindly implementing something that may be wrong.

Project Overview
Expected time per task: 60-120 minutes*
Task creation ~40-60mins
Task review ~10-30mins
*These are rough estimates - through this pilot, we can refine these numbers; if it takes way longer, please break down exact estimates of each stage and notify Angela Qu on Slack

Codebase Selection
Provide minimal but realistic codebases that contain:
Small projects: 3-50 files, 200-10000 lines total
Clear structure: Standard project layout (src/, tests/, etc.)
Intentional gaps: Missing error handling, incomplete features, TODO comments
Subtle inconsistencies: Different patterns in different files (to create interpretation ambiguity)
Documentation: README with partial info, some docstrings
Sources:
Do not select a repo from this ban list
Open-source projects (with appropriate licensing)
Sanitized/anonymized internal codebases
Synthetic but realistic codebases created for training
Mix of mature (well-structured) and startup (messy) code styles
Make sure you really take time to understand the codebase.

Task Creation
Select ambiguity type(s): Choose 1-2 categories below:

Prepare codebase: Create or select a small project with intentional gaps/inconsistencies
Craft ambiguous request: Write a task that requires clarification
Document ground truth: Note what the "ideal" answer to the prompt would be

Interface Interaction Process
Present task: Give the model the codebase and ambiguous request
Evaluate initial response:
Did the model attempt a reasonable interpretation?
Did the model identify and state assumptions?
Did the model ask specific, relevant questions?
Did the model identify impossibilities or conflicts?
Optional: Continue dialogue:
Answer clarifying questions (honestly or with further ambiguity)
Provide additional conflicting information
Request modifications based on the model's assumptions
Test implementation (if code was produced):
Does it run without errors?
Does it match a reasonable interpretation?
Are edge cases handled?

Main Task Distribution
Codebase Selection:
Small projects: 3-50 files, 200-10000 lines total
Ambiguity Type Distribution:
Underspecified requirements: 15%
Interpretation ambiguity: 15%
Technical impossibilities: 10%
Contextual ambiguity: 10%
Conflicting requirements: 10%
False Ambiguity: 40%
Language Distribution:
Python: 40%
JavaScript/TypeScript: 30%
Java: 10%
Go: 10%
Other (Rust, C++, Ruby, etc.): 10%
Domain Distribution:
Web APIs/backends: 40%
CLI tools: 20%
Data processing: 15%
Frontend: 15%
DevOps/Infrastructure: 10%

Step 1: Select and understand codebase in depth
Provide minimal but realistic codebases that contain:
Small projects: 3-50 files, 200-10000 lines total
Clear structure: Standard project layout (src/, tests/, etc.)
Intentional gaps: Missing error handling, incomplete features, TODO comments
Subtle inconsistencies: Different patterns in different files (to create interpretation ambiguity)
Documentation: README with partial info, some docstrings
Sources:
Do not select a repo from this ban list
Open-source projects (with appropriate licensing)
Sanitized/anonymized internal codebases
Synthetic but realistic codebases created for training
Mix of mature (well-structured) and startup (messy) code styles
Make sure you really take time to understand the codebase.

Step 2: Upload repo onto interface
Before starting, ensure:
Codebase: 3-50 files, realistic structure with intentional gaps
Ambiguity type selected and genuinely present (or clearly resolvable from docs for "False Ambiguity")
Ground truth solution documented
You would need clarification for this task yourself
Select folder, make sure it has a github link associated with it or you can concisely describe the source of the codebase (e.g. something you worked on before and you can provide a brief description of what the codebase is doing)
.

NOTE DOWN THE TASK ID NUMBER BEFORE YOU MOVE ON IN CASE YOU RUN INTO ISSUES LATER SO WE CAN HELP YOU DEBUG:

Step 3: Select interaction variation(s) for this task
To ensure the model learns to handle diverse real-world scenarios, you must vary how you structure each task prompt. For every task prompt you create, use options from categories below. Do not repeat the same combination across consecutive tasks.

1. Context Variations (amount/type of code provided)
   Minimal context: Single file + vague request
   Contradictory context: README says one thing, code does another
   Missing context: Reference to files/features that don't exist
   Overwhelming context: Large codebase where finding relevant parts is part of the challenge
2. Request Style Variations (how you phrase the request)
   Terse requests: "add auth"
   Verbose but vague: Long description without technical specifics
   Stakeholder language: Business requirements without technical details ("users should be able to recover their accounts easily")
   Technical jargon: Overuse of buzzwords without clear meaning ("leverage a microservices architecture for the singleton factory")
3. Clarification Interaction (conversation structure)
   Single turn: Rate initial response only
   Multi-turn dialogue: Answer Claude's questions (1-2 rounds), see if it asks the right things
   Partial answers: Answer some questions but leave others ambiguous
   Contradictory answers: Provide information that conflicts with earlier statements
4. Setup Variations (what’s in the codebase)
   With tests: Existing tests that hint at expected behavior
   With docs: README or comments that partially or fully specify requirements
   With examples: Other parts of codebase showing similar patterns
   From scratch: No codebase, just a description (maximum ambiguity)

Step 4: Ask the model one of the following types of questions regarding the codebase

The following questions are only suggestions - please feel free to ask your own questions based on your knowledge of the codebase.

1. Underspecified Requirements
   Requirements missing critical details that affect implementation:
   "Add authentication to the app" (what type? OAuth, sessions, JWT? For which routes?)
   "Make the API faster" (which endpoints? What's the target?)
   "Improve error handling" (where? What specific scenarios? What's the current behavior?)
   "Add data validation" (which fields? What validation rules? Client-side, server-side, both?)
2. Technical Impossibilities
   Requests that violate technical constraints:
   "Make this Python 2.7 code use async/await" (async/await requires Python 3.5+)
   "Add this feature without modifying the database schema" (when schema change is necessary)
   "Make this O(n²) algorithm O(log n)" (when problem fundamentally requires O(n²))
   "Import this package" (when package doesn't exist or is incompatible)
3. Contextual Ambiguity
   Ambiguity arising from incomplete codebase context:
   "Fix the bug in the user service" (multiple bugs exist)
   "Use the existing email validation" (no such validation exists)
   "Follow the same pattern as the other endpoints" (endpoints use inconsistent patterns)
   "Update the config like we discussed" (no prior discussion in context)
4. Interpretation Ambiguity
   Multiple valid interpretations of the same request:
   "Sort the results by relevance" (relevance can mean recency, popularity, text match score, etc.)
   "Add pagination" (cursor-based? offset-based? what page size? return total count?)
   "Cache the API responses" (in-memory? Redis? for how long? cache key strategy?)
   "Add logging" (what level? which operations? what format? where?)
5. Conflicting or Contradictory Requirements
   Constraints that conflict with each other:
   "Add this feature but don't change any existing code" (feature requires modifications)
   "Make it secure but don't add any authentication" (contradictory goals)
   "Support IE11 and use modern ES2020 features" (incompatible)
   "Keep backward compatibility but change the API response format" (likely breaks compatibility)
6. False Ambiguity - Clear from Context
   Requirements that appear underspecified but are actually clear when examining README, comments, existing code, documentation, config, or previous conversation:
   "Fix the validation bug" (when README or comments specify exact validation rules that aren't being followed)
   "Make the endpoint return the correct status codes" (when API documentation clearly defines which status codes to use)
   "Implement the missing error case" (when code comments have TODO noting specific error condition to handle)
   "Add the required field to the response" (when API spec in README lists all required response fields)
   "Handle the edge case" (when inline comments explicitly describe the edge case that needs handling)
   "Make it work with the database schema" (when schema is defined in migration files or comments)

✅ What does a high-quality task look like?
This is an example "golden standard" of what a high-quality task looks like

Project: Ambiguous Task

Github repo link: https://github.com/tomimick/restpie3
Primary Language: Python
Size: 45 files, 3421 lines

Task Category: False Ambiguity

Task question/prompt: Ensure that only the appropriate users with the correct rights are allowed to create new movies.

Notes:
“Appropriate users” and “correct rights” is ambiguous
Details are clearly available on the README and codebase. All write functions are editor roles and above so it should recognize that.

Context: Based on the README and codebase, the agent should deduce that movie creation should require users with the role editor or higher, @login_required(role=’editor’). In this repo, API routes are defined using decorators and there is role-based access control imported from webutil. There is also a session based authentication set during login and signup. Movie CRUD subsystem is implemented to where GET does not require authentication, but POST, PUT, and DELETE require editor permissions. Some of the roles are readonly, editor, admin, superuser. The signup sets the role to ‘editor’ by default.

Ideal answer (from your perspective):
The model should detect the ambiguity with “appropriate users” and “correct rights”.
It should refer to api_movies.py and see that the movie_create function requires the ‘editor’ role.
It should note that all write endpoints follow this pattern, and that all role-based access control is already established and consistent for the editor role.
It should also state any assumptions clearly:
“Based on the role patterns in the current write endpoints with PUSH, PUT, or DELETE, movie creation should also require at least editor role permissions.”
It could ask clarifying questions about this but this is not required.
“Should the movie creation endpoint follow the same role requirement for editor or higher as the other PUSH, PUT, and DELETE options?”
The agent should be able to proceed even without this clarification.
Ensure that @login_required(role=’editor’) is present above movie_create
Correct behavior is that movie creation process should be restricted to editor roles
Unauthorized users should automatically receive an error (this is handled by the decorator) - should not regress this.
The decorator already exists in the code, and the model must validate it is accurate and consistent with the other write methods.

INCORRECT Model Behavior:
No new auth logic should be created
There should be no changes to signup/login/session implementations
No new roles system or database changes should be made
Should not modify other role restrictions for other methods
The focus is on def movie_create():

Feel free to use this task template to draft your task [NAME] Task xx -TEMPLATE [MAKE A COPY]
Free free to refer to previous task examples if you are having a hard time coming up with ideas: Example Task/Prompts

Step 5: Analyze output generated by model A AND model B related to codebase question (2 model answers to 1 prompt side by side)

![alt text](image.png)

💡What makes a good model response
A good response demonstrates:
Reasonable interpretation: Makes a sensible attempt based on available context
Explicit assumptions: States what was assumed and why
Specific questions: Asks targeted clarifying questions about ambiguous aspects
Appropriate pushback: Identifies impossible or unreasonable requests
A good response does NOT:
Blindly implement the first interpretation without acknowledging ambiguity
Ask excessive questions about obvious details
Refuse to attempt anything without complete specifications
Make major assumptions without flagging them
Hallucinates - referring to files/content that do not exist

Step 6: Tasker reviews model performance

![alt text](image-1.png)

💡 Best Practice: Write in a separate doc first
Draft your writeup in Google Docs, Notion, or a local text editor
Only paste it into the review interface when you're ready to submit
This protects your work from accidental loss due to:
Browser refresh
Computer crashes
Session timeouts
✅ Steps to complete:
Write your feedback in a separate document
Copy your completed writeup
Paste into the review interface
Don't lose your hard work on those thoughtful reviews! 🎯
Writing Model Feedback (Input Form and Preference Labels)
Ensure “Model A Response Summary” only contains details about MODEL A.
Ensure “Model A Response Feedback” only contains details about MODEL A.
Ensure “Model B Response Summary” only contains details about MODEL B.
Ensure “Model B Response Feedback” only contains details about MODEL B.
Ensure “Overall Preference Justification” compares the models directly. It should not just describe what each model did individually.
Good: “Model A performed better in X than Model B.”
Bad: “Model A did X. Model B did Y”.
Once you make a selection between Model A and Model B on the final question (“Choose the better answer…”), the form will auto-submit! In other words, you will not be able to change your preference ratings after that point. Make sure you are aligned with your preference ratings prior to making that final selection on the last section.
We CANNOT go back and edit ratings and you will have to start over.
When rating responses, prioritize:
Ambiguity detection: Did the model notice what was unclear?
Question quality: Were questions specific and actionable?
Attempt quality: Was the initial interpretation reasonable?
Assumption transparency: Were assumptions clearly stated?
Code quality: If implemented, is the code well-structured?
Weight ambiguity handling MORE than code perfection. A response that makes a good attempt with clear assumptions and good questions should beat a response that blindly implements a perfect solution to the wrong interpretation.
✅ Example of a good detailed answer [human-written answer, LLM usage on writing model feedback will be unusable and heavily penalized]:
![alt text](image-2.png)

Once you input all of your feedback and preference ratings you will see a green checkmark appear:

🟢 Green checkmark ≠ Submitted The green checkmark only means you've completed filling out the review fields. You still need to hit the Submit button to finalize!

Before submitting, ensure:
All 5 ratings completed: ambiguity detection, question quality, assumptions, implementation, overall
Rated ambiguity handling higher than code perfection
If code produced: tested and runs, linked in deliverable
Multi-turn (if applicable): 1-2 clarification rounds with honest/strategic answers

Red Flags - Don't Submit If:
⚠️ Ambiguity feels artificial/contrived
⚠️ Model blindly implemented without acknowledging ambiguity (should rate low, not skip)
⚠️ You didn't verify ground truth yourself
⚠️ Using same interaction pattern as recent tasks
⚠️ Your question is grep-able or has trivial detail
⚠️ You didn't trace through code yourself to verify ground truth
⚠️ Task requires model to check <5 files

Step 7: Submitting task through Airtable
After submitting your task on the Model Interface, Open the Project’s Airtable to see all of the submitted tasks.

Click the “Sort by email” button to find all of the tasks that you submitted through the Model Interface (you can only claim tasks that you submit)

Press the green “Claim” button to Claim your task

Input all of the required fields to submit your task
⚠️ Important! All of these fields are required to submit your task

Press the blue “Submit” button

Congratulations 🎉 You have successfully submitted a task!
🟢 Important! Your task is only truly submitted after you have completed all of the steps above.
⚠️ Remember that you are only writing 1 task for this round.

FAQs
Q: How do I access project resources like Slack? The Model Interface? Airtable?
Make sure to try using the personal email you originally applied to the Mercor listing with. A common issue is that you must use Okta SSO to access these resources. If this does not work, try to use your Mercor email. If you are still having trouble, see https://talent.docs.mercor.com/how-to/okta-access.

Q: How do I submit a task? Your task is not actually submitted until you 1) Read the instructions and gain a strong understanding of what a good task looks like 2) Write your task down in a word doc 3)

Q: Do we have an example task? Yes, please refer to the golden standard examples in the instructions doc found on this page → Go to page. There are 2 examples with green borders. Please read and understand both examples.

Q: My task disappeared from Airtable after I submitted, what do I do? Your task did not actually disappear. It was just sent off for review. You will receive feedback shortly. Be ready to implement the changes and improve your tasks.

Q: I submitted my first task, now what? You will receive feedback soon, and if you meet the quality expectations, you will be green lit for higher production.

Q: I got feedback that my task was good, but my hours are still capped. We’ll update the hours for those who are approved as fast as possible. Be sure to send a message in the main slack channel or the Support button in the slack channel if you need support.

Q: How do I know if my task has the right level of ambiguity? Test yourself: If you wouldn't need clarification, it's not ambiguous enough. Start with real scenarios where you've needed clarification from teammates. Keep ambiguity natural, not contrived

Q: What is "False Ambiguity"? Requirements that appear underspecified but are actually clear when examining README, comments, existing code, or documentation. Example: "Fix the validation bug" when README specifies exact validation rules. Good responses examine context and respond correctly or implement correctly without unnecessary questions.

Q: What should my codebase contain? 3-50 files, 200-10,000 lines total. Standard project layout (src/, tests/, etc.). Should include intentional gaps (missing error handling, incomplete features, TODOs) and subtle inconsistencies. README with partial info and some docstrings.

Q: Can we create multiple tasks on one codebase? Yes, as long as the question is in a different category. Don't repeat the same category of question on the same codebase.

Q: Are we doing multi-turn tasks? Not yet. We are currently only focusing on single-turn only. Multi-turn will come later.

Q: What is the difference between model summary feedback. This can be a challenging topic to grasp at first.You can think of the summary as "what" the model did and the feedback as the how/why it should do things differently or why it matters.

Quick Checks
Before Starting
Codebase: 3-50 files, realistic structure with intentional gaps
Ambiguity type selected and genuinely present (or clearly resolvable from docs for "False Ambiguity")
Ground truth solution documented
You would need clarification for this task yourself
After Model Responds
All 5 ratings completed (1-4 scale): ambiguity detection, question quality, assumptions, implementation, overall
Rated ambiguity handling higher than code perfection
If code produced: tested and runs, linked in deliverable
Multi-turn (if applicable): 1-2 clarification rounds with honest/strategic answers

Red Flags - Don't Submit If:
⚠️ Ambiguity feels artificial/contrived
⚠️ Model blindly implemented without acknowledging ambiguity (should rate low, not skip)
⚠️ You didn't verify ground truth yourself
⚠️ Using same interaction pattern as recent tasks
Expected time: 60-120 min per task

Level of Detail on Model Performance - expected level of detail for ALL written responses [human-written answer, LLM usage on writing model feedback will be unusable and heavily penalized]:

![alt text](image-3.png)

Tips for Taskers
Always think about these things when creating a task:
Creating Good Ambiguous Tasks
Start with real scenarios: Think of times you've needed clarification from teammates
Keep it realistic: Ambiguity should feel natural, not contrived
Scale appropriately: Don't make codebases too large or requests too complex
Test yourself: If you wouldn't need clarification, it's not ambiguous enough
Avoid trick questions: Goal is ambiguity, not deception
Evaluating Responses
Judge the balance: Best responses attempt + clarify, not one or the other
Be fair about impossibilities: The model can't know your intent, only what's stated
Reward good questions: Specific, actionable questions are valuable even if code isn't perfect
Penalize blind implementation: Worse than asking too many questions
Consider context: More clarification appropriate for complex/unfamiliar domains

Examples of Good vs. Bad Ambiguous Task Outputs
Example responses based on Question Category:

1. Underspecified Requirements
   Good response: Makes a reasonable attempt at interpretation based on what's clear from the request (e.g., implementing basic session auth if "add authentication" clearly implies starting with something simple), while explicitly stating assumptions and asking specific clarifying questions about ambiguous aspects (OAuth providers? Password requirements? Session duration?). The balance between attempting implementation versus asking questions first will vary based on context - trust your judgment as an annotator to prefer the response that handles the ambiguity most appropriately for the specific task.
   Bad response: Implements elaborate OAuth with Google/GitHub/Facebook without asking, or refuses to do anything until every detail is specified.
2. Technical Impossibilities
   Good response: Explains why the exact request is impossible, proposes closest alternative, asks if alternative is acceptable.
   Bad response: Silently does something different, or implements a broken/incorrect solution to "fulfill" the request.
3. Contextual Ambiguity
   Good response: Searches codebase, identifies the ambiguity (e.g., "I found 3 potential issues in user_service.py"), asks which to address.
   Bad response: Picks one arbitrarily without acknowledgment, or claims to have context that wasn't provided.
4. Interpretation Ambiguity
   Good response: Implements one reasonable interpretation, explains the choice, asks if a different approach is preferred.
   Bad response: Implements without acknowledging other valid interpretations, or over-engineers trying to support all possibilities.
5. Conflicting or Contradictory Requirements
   Good response: Identifies the conflict, explains the tradeoffs, proposes a resolution, asks for prioritization.
   Bad response: Silently prioritizes one constraint without acknowledging the conflict.
6. False Ambiguity - Clear from Context
   Good response: Examines README, comments, and existing code to understand conventions, implements consistently and correctly with documented/evident patterns, briefly confirms "Based on the README section on error handling, I'm using..." or "Following the pattern in user_controller.py where..." without over-questioning.
   Bad response: Either (1) asks unnecessary clarifying questions about things clearly documented in README or evident from consistent codebase, failing to check available context, or (2) ignores relevant documentation and code that contains useful information, implementing something wrong or inconsistent without examining the codebase.
