# Quantum-Bros
Hello World! Welcome to our repository for the 2025 Qiskit Hackathon featuring our project: Quantum Math Quest — a gamified, adaptive math challenge powered by quantum-inspired algorithms.


## Introduction:
Quantum Math Quest is an interactive game that merges mathematical problem-solving with adaptive learning inspired by quantum computation principles.

The idea: a Math Quest that evolves with you. As players solve problems, the game adjusts the difficulty dynamically using an ELO-style rating system, ensuring a continuous, personalized challenge.

Our project explores how quantum computing concepts—such as probabilistic reasoning and state-based progression—can enhance educational systems and game design.

We’re building this as part of the QFF25 Hackathon, hosted by the University of Ottawa Quantum Club.


## Approach
Our approach combines classical adaptive algorithms with quantum-inspired mechanisms:

1) ELO-based Adaptation:

Each player and question has a dynamic ELO rating.

Correct answers increase difficulty, incorrect answers adjust it downward.

The system continuously estimates the player's skill level to match them with optimal problems.

2) Quantum-Inspired Randomization:

Quantum randomness (simulated or derived from Qiskit backends) introduces variability in question selection, ensuring replayability.

Some gameplay features depend on quantum measurement outcomes, adding unpredictability and fairness.

3) Gamification Layer:

Players progress through mathematical “realms” themed around quantum gates and concepts.

Each realm introduces progressively complex math aligned with quantum foundations (linear algebra, probability, etc.).

4) Technology Stack:

Python (core logic and ELO engine)

Qiskit (quantum randomness & optional circuit demos)

Streamlit / Flask (for interactive front-end)


## How to run

### Setup
pip install -r requirements.txt

### Training
python train_model.py

### Evaluation
python evaluate.py

#### Demo 
streamlit run app.py

## Team members
### Zachary Levesque: 
4th year Electrical Engineering and Physics student at the University of Ottawa. Zachary is an expert in machine learning.

### Aleksa Zarin: 
4th year Electrical Engineering and Physics student at the University of Ottawa. Aleksa is an expert in Python libraries

### Samir Jr Abou Serhal: 
4th year Electrical Engineering and Physics student at the University of Ottawa. Samir is an expert in quantum mechanics.

