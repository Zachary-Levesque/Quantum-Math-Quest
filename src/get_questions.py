import json
import os

def get_questions(subject, difficulty, question_id):
    """
    Returns the question, options, correct answer, and explanation 
    for the given subject, difficulty, and question number (1-10).
    """

    # Map subjects to JSON filenames
    subject_files = {
        "Algebra": "algebra.json",
        "Calculus": "calcul.json",
        "Geometry": "geometry.json",
        "Probability": "probabilite.json"
    }

    if subject not in subject_files:
        raise ValueError(f"Subject '{subject}' not recognized.")

    # Get the directory of this script file
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Build the full path to the JSON file
    file_path = os.path.join(script_dir, "..", "data", "questions", subject_files[subject])

    # Normalize the path
    file_path = os.path.normpath(file_path)

    # Load JSON file
    with open(file_path, "r", encoding="utf-8") as f:
        questions_data = json.load(f)

    # Map difficulty to lowercase string in JSON
    difficulty_map = ["easy", "medium", "hard", "expert"]
    difficulty_str = difficulty_map[difficulty]

    # Filter questions by difficulty
    filtered_questions = [q for q in questions_data if q["difficulty"] == difficulty_str]

    if not (1 <= question_id <= len(filtered_questions)):
        raise ValueError(f"Question ID {question_id} out of range for {difficulty_str} questions in {subject}.")

    # Select question by question_id (1-based indexing)
    question_data = filtered_questions[question_id - 1]

    return (
        question_data["question"],
        question_data["options"],
        question_data["correct_answer"],
        question_data["explanation"]
    )
