# Quantum Math Quest

Quantum Math Quest is a Python desktop quiz game that combines adaptive math practice with quantum-random question selection. It was built for the 2025 Qiskit Hackathon by Zachary Levesque, Aleksa Zarin, and Samir Jr. Abou Serhal.

Players answer algebra, probability, geometry, and calculus questions while an Elo-style rating system adjusts difficulty. Quantum circuits generated with Qiskit provide randomized category and question selection, making the game a practical demonstration of how quantum measurement can be used inside an educational application.

## Features

- Adaptive difficulty based on player Elo
- Quantum-random category and question selection with Qiskit Aer
- Four math categories: algebra, probability, geometry, and calculus
- Instant feedback with explanations
- Elo progression tracking and visualization
- Tkinter desktop interface

## Why It Matters

The project connects quantum computing concepts to a user-facing learning tool. Instead of presenting quantum randomness as an isolated circuit demo, the game uses measurement outcomes as part of the product loop: selecting practice material, varying difficulty, and keeping repeated sessions unpredictable.

## Project Structure

```text
Quantum-Bros/
├── data/questions/          Math question banks
├── demo/                    Hackathon visuals and generated outputs
├── src/
│   ├── main.py              Tkinter game interface
│   ├── elo.py               Rating and difficulty updates
│   ├── get_questions.py     Question loading
│   ├── quantum_kfactor.py   Quantum-inspired Elo K-factor logic
│   └── quantum_random.py    Qiskit-based random number generation
├── requirements.txt
└── README.md
```

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

The original hackathon dependency file, `Requirements.txt`, is kept for compatibility. New setup instructions use the standard lowercase `requirements.txt`.

## Run The Game

```bash
python src/main.py
```

The app opens a local Tkinter window. A desktop Python environment is required.

## Technical Notes

- `quantum_random.py` builds small Qiskit circuits, measures them with `AerSimulator`, and maps the bitstrings to category or question indexes.
- `elo.py` adjusts the player rating based on correctness and current difficulty.
- `quantum_kfactor.py` experiments with a quantum-inspired dynamic K-factor so rating changes can vary by state.
- Question data is stored as JSON so new categories or difficulty tiers can be added without changing the UI.

## Team

- Zachary Levesque: quantum algorithm design and machine-learning direction
- Aleksa Zarin: Python application structure and library integration
- Samir Jr. Abou Serhal: math question development, documentation, and maintenance
