AI-Assisted Workflow Drill
Round 1: Vague Prompt

For the first round, I used the vague prompt: “Add a diet plan settings form to my project with validation.” I did not give the AI many details because the point of this round was to see what it would do on its own.

The main problem was that the AI generated React/JSX code even though my project is written in Python using CustomTkinter. So the code could not just be added to my project and run. It was also not really connected to my existing inference engine. This was the biggest mistake I noticed from the AI in Round 1.

I kept the generated code in round1_output.jsx so I could compare it with the second round instead of deleting it.

Round 2: Precise Prompt

For Round 2, I gave the AI a much more detailed prompt. I told it to use my existing Python/CustomTkinter setup, which files to work with, what the new settings should do, and what I wanted it to check after making the changes.

This time, the AI changed main_gui.py and inference_engine.py instead of trying to use React. It added a Diet Plan Settings section where the user can select 3, 4, or 5 meals per day and enter an optional calorie target.

I tested the changes myself. The application opened normally, and 3, 4, and 5 meals produced the correct number of meal entries. I also entered abc as the calorie target and the program showed an error instead of crashing. When the calorie field was empty, the program still used the automatically calculated target.

Edge Cases and Review

One edge case I noticed is that the calorie validation accepts any positive number, even if the number is unrealistic. I did not change this because the prompt only asked for a positive number.

The precise prompt also made the code easier to review because I already knew what behavior I was expecting. The vague prompt required more checking because the AI made assumptions about the project's technology.