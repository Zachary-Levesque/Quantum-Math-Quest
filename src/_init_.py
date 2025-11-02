from quantum_random import quantum_rand_0_to_3, quantum_rand_1_to_10
from elo import update_elo, get_difficulty
from get_questions import get_questions


start_elo = 500
counter = 0
while True:
    if counter == 0:
        elo = start_elo

    subjects = [ "Geometry", "Algebra", "Calculus", "Probability" ]

    subject_index = quantum_rand_0_to_3() # returns 0, 1, 2, or 3
    chosen_subject = subjects[subject_index] # Ex "Geometry"
    print(f"Chosen subject: {chosen_subject}")

    # There are 4 brackets for difficulty, each corresponding to a range of ELO ratings
    difficulties = [ "Easy", "Medium", "Hard", "Expert" ]
    difficulty_index = get_difficulty(elo) # returns 0, 1, 2, or 3
    chosen_difficulty = difficulties[difficulty_index] # Ex "Medium"
    print(f"Chosen difficulty: {chosen_difficulty}")
    question_id = quantum_rand_1_to_10()  # returns from 1 to 10
    print(question_id)

    # chosen subject (0-3 randomiser), chosen difficulty (based on ELO), question ID (1-10 randomiser)
    question, options, correct_answer, explanation = get_questions(chosen_subject, difficulty_index, question_id)
    print(f"Here is your question: {question}")
    print(f"Options:{options}")
    answer = input("Your answer: ")
    if answer == correct_answer:
        print("Correct!")
        print(f"Explanation: {explanation}")
        correct = True
    else:
        print(f"Incorrect. The correct answer was: {correct_answer}")
        print(f"Explanation: {explanation}")
        correct = False
     
    # Once question is answered, update elo
    elo = update_elo(elo, correct)
    print(elo)
    counter +=1