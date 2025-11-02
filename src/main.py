# In order to acheive this code, we must import many libraries
import tkinter as tk
from tkinter import messagebox
import time
import matplotlib.pyplot as plt
from quantum_random import quantum_rand_0_to_3, quantum_rand_1_to_10
from elo import update_elo, get_difficulty
from get_questions import get_questions
from quantum_kfactor import QuantumKEstimator

# This Class defines the entire Math Game
class MathQuizGame:
   def __init__(self, root):
       # Window interface setup
       self.root = root
       self.root.title("Math Quiz Game")
       self.root.geometry("750x650")
       self.root.configure(bg="#1a1a2e")

       # Game state (What is the subject, difficulty, etc)
       self.elo = 500
       self.subjects = ["Geometry", "Algebra", "Calculus", "Probability"]
       self.difficulties = ["Easy", "Medium", "Hard", "Expert"]
       self.current_question = None
       self.current_options = []
       self.correct_answer = None
       self.explanation = None
       self.current_difficulty_index = None
       self.question_start_time = None

       # Getting the K estimator from quantum_kfactor
       self.k_est = QuantumKEstimator()

       # Every 5 questions, we plot the elo variation
       self.question_counter = 0
       self.elo_question_index = []
       self.elo_values = []

       # UI
       self.setup_ui()
       self.load_new_question()

   def setup_ui(self):
       # Header with ELO and delta badge
       header = tk.Frame(self.root, bg="#16213e", height=100)
       header.pack(fill="x", padx=20, pady=(20, 10))
       header.pack_propagate(False)

       self.elo_label = tk.Label(
           header,
           text=f"ELO: {self.elo}",
           font=("Arial", 24, "bold"),
           bg="#16213e",
           fg="#00d9ff",
       )
       self.elo_label.pack(pady=(10, 0))

       self.elo_change_label = tk.Label(
           header,
           text="",
           font=("Arial", 14, "bold"),
           bg="#16213e",
       )
       self.elo_change_label.pack(pady=(0, 10))

       # Subject and difficulty info
       info_frame = tk.Frame(self.root, bg="#1a1a2e")
       info_frame.pack(pady=10)

       self.subject_label = tk.Label(
           info_frame,
           text="Subject: ",
           font=("Arial", 14, "bold"),
           bg="#1a1a2e",
           fg="#00d9ff",
       )
       self.subject_label.pack(side="left", padx=10)

       self.difficulty_label = tk.Label(
           info_frame,
           text="Difficulty: ",
           font=("Arial", 14, "bold"),
           bg="#1a1a2e",
           fg="#f39c12",
       )
       self.difficulty_label.pack(side="left", padx=10)

       # Question area
       question_frame = tk.Frame(self.root, bg="#16213e")
       question_frame.pack(fill="both", expand=True, padx=20, pady=10)

       self.question_label = tk.Label(
           question_frame,
           text="",
           font=("Arial", 15, "bold"),
           bg="#16213e",
           fg="#ffffff",
           wraplength=650,
           justify="left",
           pady=15,
       )
       self.question_label.pack(pady=20, padx=20, fill="x")

       # Options
       self.options_frame = tk.Frame(question_frame, bg="#16213e")
       self.options_frame.pack(pady=10, padx=20, fill="both", expand=True)

       self.option_buttons = []
       for _ in range(4):
           btn = tk.Button(
               self.options_frame,
               text="",
               font=("Arial", 12),
               bg="#0f3460",
               fg="#000000",
               activebackground="#1a5490",
               activeforeground="#000000",
               relief="solid",
               bd=2,
               cursor="hand2",
               anchor="w",
               padx=15,
               pady=12,
               justify="left",
               wraplength=600,
           )
           btn.pack(fill="x", pady=6)
           self.option_buttons.append(btn)

       # Feedback area
       self.feedback_frame = tk.Frame(self.root, bg="#1a1a2e", height=100)
       self.feedback_frame.pack(fill="x", padx=20, pady=10)
       self.feedback_frame.pack_propagate(False)

       self.feedback_label = tk.Label(
           self.feedback_frame,
           text="",
           font=("Arial", 15, "bold"),
           bg="#1a1a2e",
           fg="white",
       )
       self.feedback_label.pack(pady=2)

       self.explanation_label = tk.Label(
           self.feedback_frame,
           text="",
           font=("Arial", 11),
           bg="#1a1a2e",
           fg="#cccccc",
           wraplength=650,
           justify="left",
       )
       self.explanation_label.pack(pady=2)

       # Next button
       self.next_button = tk.Button(
           self.root,
           text="Next Question →",
           font=("Arial", 13, "bold"),
           bg="#00d9ff",
           fg="#000000",
           activebackground="#00b8d4",
           activeforeground="#000000",
           relief="flat",
           cursor="hand2",
           width=22,
           height=2,
           command=self.load_new_question,
           state="disabled",
       )

   def _norm(self, x):
       # Normalize text for comparisons
       return str(x).strip().lower()

   def _letter_to_index(self, s):
       # Convert A/B/C/D to 0/1/2/3
       if not isinstance(s, str):
           return None
       s = s.strip().lower()
       if not s:
           return None
       c = s[0]
       if c in "abcd":
           return ord(c) - ord("a")
       return None

   def _compute_correct_index(self):
       # Resolve the correct answer index from multiple formats
       ca = self.correct_answer
       if isinstance(ca, int):
           if 0 <= ca <= 3:
               return ca
           if 1 <= ca <= 4:
               return ca - 1
       if isinstance(ca, str):
           ca_num = None
           try:
               ca_num = int(ca.strip())
           except:
               ca_num = None
           if ca_num is not None:
               if 1 <= ca_num <= 4:
                   return ca_num - 1
               if 0 <= ca_num <= 3:
                   return ca_num
           li = self._letter_to_index(ca)
           if li is not None:
               return li
       ca_norm = self._norm(ca)
       for i, opt in enumerate(self.current_options):
           if self._norm(opt) == ca_norm:
               return i
       return None

   def load_new_question(self):
       # Reset feedback and controls
       self.feedback_label.config(text="")
       self.explanation_label.config(text="")
       self.elo_change_label.config(text="")
       self.next_button.config(state="disabled", bg="#555555")
       try:
           if self.next_button.winfo_ismapped():
               self.next_button.pack_forget()
       except:
           pass

       # Draw subject and difficulty for this question
       subject_index = quantum_rand_0_to_3()
       chosen_subject = self.subjects[subject_index]

       self.current_difficulty_index = get_difficulty(self.elo)
       chosen_difficulty = self.difficulties[self.current_difficulty_index]

       # Draw question id and fetch the content
       question_id = quantum_rand_1_to_10()
       self.current_question, self.current_options, self.correct_answer, self.explanation = get_questions(
           chosen_subject, self.current_difficulty_index, question_id
       )

       # Update UI
       self.subject_label.config(text=f"Subject: {chosen_subject}")
       self.difficulty_label.config(text=f"Difficulty: {chosen_difficulty}")
       self.question_label.config(text=self.current_question)

       option_letters = ["A", "B", "C", "D"]
       for i in range(len(self.option_buttons)):
           if i < len(self.current_options):
               option_text = f"{option_letters[i]}. {self.current_options[i]}"
               self.option_buttons[i].config(
                   text=option_text,
                   state="normal",
                   bg="#0f3460",
                   fg="#000000",
                   activeforeground="#000000",
                   command=lambda idx=i: self.check_answer(idx),
               )
           else:
               self.option_buttons[i].config(text="", state="disabled")

       # Start timer for this question
       self.question_start_time = time.time()

   def check_answer(self, selected_index):
       # Disable options after a choice
       for btn in self.option_buttons:
           btn.config(state="disabled")

       # Determine correctness
       correct_index = self._compute_correct_index()
       if correct_index is None:
           sel_norm = self._norm(self.current_options[selected_index])
           corr_norm = self._norm(self.correct_answer)
           correct = (sel_norm == corr_norm)
       else:
           correct = (selected_index == correct_index)

       # Color feedback
       if correct:
           self.option_buttons[selected_index].config(bg="#27ae60", fg="#000000", activeforeground="#000000")
           self.feedback_label.config(text="✓ Correct!", fg="#27ae60")
       else:
           self.option_buttons[selected_index].config(bg="#e74c3c", fg="#000000", activeforeground="#000000")
           if correct_index is not None and 0 <= correct_index < len(self.option_buttons):
               self.option_buttons[correct_index].config(bg="#27ae60", fg="#000000", activeforeground="#000000")
           self.feedback_label.config(text=f"✗ Incorrect. The correct answer was: {self.correct_answer}", fg="#e74c3c")

       # Show explanation
       self.explanation_label.config(text=f"Explanation: {self.explanation}")

       # ELO update with quantum K and timing
       response_time = time.time() - self.question_start_time if self.question_start_time else 0.0
       k_now = self.k_est.k()
       elo_before = self.elo
       self.elo = update_elo(self.elo, correct, self.current_difficulty_index, k_now)
       elo_delta = int(round(self.elo - elo_before))

       self.elo_label.config(text=f"ELO: {int(round(self.elo))}")
       if elo_delta > 0:
           self.elo_change_label.config(text=f"+{elo_delta} ELO", fg="#27ae60")
       elif elo_delta < 0:
           self.elo_change_label.config(text=f"-{abs(elo_delta)} ELO", fg="#e74c3c")
       else:
           self.elo_change_label.config(text="")

       # Increment question counter first, then record ELO vs question index
       self.question_counter += 1
       self.elo_question_index.append(self.question_counter)
       self.elo_values.append(self.elo)

       # Feed estimator with result and time
       self.k_est.add(correct, response_time)

       # Reveal Next button
       if not self.next_button.winfo_ismapped():
           self.next_button.pack(pady=15)
       self.next_button.config(state="normal", bg="#00d9ff", fg="#000000", activeforeground="#000000")

       # Ask every 5 questions
       if self.question_counter % 5 == 0:
           self.ask_exit_or_continue()

   def ask_exit_or_continue(self):
       # Ask the user if they want to exit and view the ELO-vs-questions plot
       exit_now = messagebox.askyesno(
           "Exit?",
           f"You've answered {self.question_counter} questions. Do you want to exit and view your ELO vs questions plot?"
       )
       if exit_now:
           self.show_elo_plot()
           self.root.destroy()

   def show_elo_plot(self):
       # Plot ELO as a function of questions answered (1..N)
       if len(self.elo_question_index) == 0:
           return
       plt.figure()
       plt.plot(self.elo_question_index, self.elo_values, marker="o")
       plt.xlabel("Question #")
       plt.ylabel("ELO")
       plt.title("ELO vs Questions Answered")
       plt.grid(True)
       plt.tight_layout()
       plt.show()

# This main function is the base of the program. It calls the game function
def main():
   root = tk.Tk()
   app = MathQuizGame(root)
   root.mainloop()

# Call the main function
if __name__ == "__main__":
   main()