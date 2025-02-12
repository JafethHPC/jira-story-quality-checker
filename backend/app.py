# Import FastAPI, a modern web framework for building APIs with Python
from fastapi import FastAPI

# Immport BaseModel from Pydantic, which is used for data validation and serialization
from pydantic import BaseModel

# Create a FastAPI instance (this is our web server)
app = FastAPI()

# Define a request model using Pydantic's BaseModel
# This model ensures that the incoming request contains a "description" field
class JiraStory(BaseModel):
    description: str

# Define an API endoing that listens for POST requests on the /evaluate path
@app.post("/evaluate")
def evaluate_story(story: JiraStory):
    """
    API endpoint to evaluate a Jira story.
    - Accepts a JSON request with a story description.
    - Returns a score and feedback based on best practices.
    """
    # Call the function that evaluates the Jira story
    score, feedback = evaluate_jira_story(story.description)

    #Return the score and feedback as a JSON response
    return {"score": score, "feedback": feedback}

def evaluate_jira_story(description: str):
    """
    Function to evaluate a Jira story based on basic best practices.
    - Takes a story description as input.
    - Returns a score (out of 100) and a list of feedback messages.
    """

    score = 0 # Start with a score of 0
    feedback = [] # List to store feedback messages

    # Rule 1: Check if the story follows the common "User Story" format
    if description.lower().startswith("as a"):
        score += 15 # Add points if it follows the correct format
    else:
        feedback.append("Story should start with 'as a [user], I want to [action], so that [benefit]'")

    # Rule 2: Check if the story includes a goal ("I want to")
    if "i want to" in description.lower():
        score += 15 # Add points if it includes a goal
    else:
        feedback.append("Story should clearly state the goal: 'I want to [do something]'")

    # Rule 3: Check if the story includes a reason/benefit ("so that")
    if "so that" in description.lower():
        score += 15 # Add points if it includes a reason/benefit
    else:
        feedback.append("Story should include a reason/benefit: 'so that [some benefit is achieved]'")

    # Rule 4: Check if the story includes an "Acceptance Criteria" section
    if "acceptance criteria" in description.lower():
        score += 15 # Add points if it includes acceptance criteria
    else:
        feedback.append("Story should include 'Acceptance Criteria' section")

    # Rule 5: Check if "Definition of Done" is included
    if "definition of done" in description.lower():
        score += 25 # Add points if the story defined "Definition of Done"
    else:
        feedback.append("Define a 'Definition of Done' for the story")

    # Rule 6: Check if the description avoids technical details (mention of 'database', 'API', etc.)
    technical_keywords = ["database", "api", "query", "code", "server", "frontend", "backend"]
    if any(word in description.lower() for word in technical_keywords):
        feedback.append("Avoid technical details in the story description")
    else: 
        score += 10 # Add points if the description avoids technical details
    
    # Rule 7: Ensure the description has enough detail (at least 10 words)
    word_count = len(description.split())
    if word_count < 10:
        feedback.append("Story description is too short; add more details")
    elif word_count < 50:
        feedback.append("Story description is too long; keep it consise")
    else: 
        score += 10 # Add points if the description has enough detail

    # Final adjustments: Ensure the score does not exceed 100
    score = min(score, 100)

    # Return the total score and the feedback messages
    return score, feedback