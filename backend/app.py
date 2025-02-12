# Importing necessary libraries for NLP and text analysis
import spacy # spaCy is a powerful NLP library used for text processing, tokenization, dependency parsing, and named entity recognition (NER)
from textblob import TextBlob # TextBlob is a simple NLP library that helps with sentiment analysis, text classification, and more

# Load the spaCy model for Natural Language Processing (NLP)
# This model is pre-trained and helps analyze text by breaking it into words (tokens), identifying parts of speech, and more
nlp = spacy.load("en_core_web_md")

custom_keywords = ["user", "developer", "admin", "feature", "login", "payment", "payment system", "dashboard", "data", "security"]


def evaluate_jira_story(description: str):
    """
    Evaluates a Jira story description by analyzing its structure and content using NLP techniques.
    The function checks if the story follows best practices for Jira user stories and provides a score along with feedback for improvement.

    The evaluation is based on:
    - User Story format (using dependency parsing)
    - Clarity and actionability (via sentiment analysis)
    - Presence of key sections (using named entity recognition)
    - Story length and conciseness

    Parameters:
        description (str): The Jira story description to be evaluated

    Returns:
        tuple: A score (out of 100) representing the quality of the sotry, and a list of feedback messages
    """

    score = 0 # Start with a score of 0
    feedback = [] # List to store feedback messages

    # Rule 1: Check if the story follows the common "User Story" format (using dependency parsing)
    # The spaCy NLP model processes the text, breaking it down into structured tokens.
    doc = nlp(description) # Apply spaCy NLP model to analyze the story text
    # We check if the sentence structure contains key patterns like "as a [user], I want to [action], so that [benefit]"
    has_as_a_user = any(token.text.lower() == "as" and token.dep_ == "prep" for token in doc) and \
                    any(token.text.lower() == "user" and token.dep_ == "pobj" for token in doc)
    
    has_i_want_to = any(token.text.lower() == "want" and token.dep_ == "ROOT" for token in doc)

    if has_as_a_user and has_i_want_to:
        score += 15
    else:
        feedback.append("❌ Story should follow the format: 'As a [user], I want to [do something], so that [benefit]'")

    # Rule 2: Check if the story includes a goal ("I want to")
    if "i want to" in description.lower():
        score += 15 # Add points if it includes a goal
    else:
        feedback.append("❌ Story should clearly state the goal: 'I want to [do something]'")

    # Rule 3: Check if the story includes a reason/benefit ("so that")
    if "so that" in description.lower():
        score += 15 # Add points if it includes a reason/benefit
    else:
        feedback.append("❌ Story should include a reason/benefit: 'so that [some benefit is achieved]'")

    # Rule 4: Sentiment analysis -  A clear, actionable story usually has a positive sentiment
    # TextBlob is used to perform sentiment analysis on the story description and assigns a polarity score:
    # - Positive (>0) means it's likely clear and actionable
    # - Negative (<0) means it might be unclear or not actionable
    # - Neutral (0) means it could go either way
    sentiment = TextBlob(description).sentiment # Analyze the sentiment of the story description
    if sentiment.polarity > 0.1:
        score += 10
    elif sentiment.polarity < -0.1:
        feedback.append("❌ Story might be unclear or not actionable; consider revising the description")
    else:
        score += 10 # Neutral sentiment, so add some points

    # Rule 5: Extract Named Entities (e.g., user roles, actions, benefits) using spaCy's Named Entity Recognition (NER)
    # Named Entity Recognition (NER) is used to detect important words or phrases in the story description
    # These could be things like "developer", "feature", "payment system", etc.
    entities = [ent.text for ent in doc.ents]

    if not entities:
        # No entities detected by spaCy, so let's check for custom keywords
        matches = [keyword for keyword in custom_keywords if keyword in description.lower()]
        if matches:
            entities.extend(matches)

    # Check if we have enough relevant entities (user roles, actions, benefits)
    if len(entities) == 0:
        feedback.append("❌ Story should include specific user roles, actions, or benefits for clarity")
    else:
        score += 10  # Add points if entities are present
    
    # Rule 7: Ensure the description has enough detail 
    word_count = len(description.split())
    if word_count < 10:
        feedback.append("❌ Story description is too short; add more details")
    elif word_count > 50:
        feedback.append("❌ Story description is too long; keep it consise")
    else: 
        score += 10 # Add points if the description has enough detail

    # Final adjustments: Ensure the score does not exceed 100
    score = min(score, 100)

    # Return the total score and the feedback messages
    return score, feedback

if __name__ == "__main__":
    # Ask the user for the Jira story description
    description = input("Enter the Jira story description: ")

    # Call the evaluate_jira_story function to evaluate the story description
    score, feedback = evaluate_jira_story(description)

    # Display the evaluation results
    print("\nJira Story Evaluation Results:")
    print(f"Score: {score}/100")
    print("Feedback:")
    for message in feedback:
        print(message)