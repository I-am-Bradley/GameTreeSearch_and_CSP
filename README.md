# Game Tree Search and Constraint Satisfaction

## 🧭 Project Overview

### Title:
### Game Tree Search and Constraint Satisfaction

### Purpose

This repository contains implementations of classical Artificial Intelligence search algorithms applied to adversarial game playing and constraint satisfaction problems. The project explores game tree search techniques for Connect-4 and Constraint Satisfaction Problem (CSP) algorithms for solving Sudoku puzzles while comparing algorithm performance, heuristics, and optimization strategies.

### Audience

- Artificial Intelligence Students
- Computer Science Students
- Researchers
- Software Engineers
- Machine Learning Enthusiasts

---

# 🧱 Project Scope

## Task 1: Connect-4 AI

Implements intelligent game-playing agents capable of competing against human players using adversarial search and Monte Carlo simulations.

### Components

- Connect-4 Game Engine
- Alpha-Beta Search Agent
- Monte Carlo Tree Search Agent
- Performance Logging
- Gameplay Visualization

### Techniques

- Minimax Search
- Alpha-Beta Pruning
- Monte Carlo Tree Search (MCTS)
- Random Playouts
- Smart Playouts
- Adversarial Search

---

## Task 2: Sudoku Constraint Satisfaction

Implements a Constraint Satisfaction Problem (CSP) solver capable of solving Sudoku puzzles using multiple inference and heuristic strategies.

### Components

- Sudoku CSP Solver
- Puzzle Loader
- Constraint Propagation
- Performance Evaluation
- Visualization

### Techniques

- Constraint Satisfaction Problems (CSP)
- Backtracking Search
- Forward Checking (FC)
- Maintaining Arc Consistency (MAC)
- Minimum Remaining Values (MRV)
- Least Constraining Value (LCV)

---

# 📂 Repository Structure

```text
GameTreeSearch_and_CSP/
│
│
├── Task1_Connect4/
│   ├── Logs/
│   │   ├── ab_depth_timeline.txt
│   │   ├── mcts_random_log.txt
│   │   ├── mcts_smart_log (C = 1.41).txt
│   │   └── mcts_smart_log (C=2).txt
│   ├── data/
│   │   └── connect4 website.txt
│   ├── report/
│   │   └── Project Report.docx
│   ├── results (screenshots)/
│   │   ├── AB_Human_winning.png
│   │   ├── AB_computer_winning.png
│   │   ├── MCTS -random_Human_winning.png
│   │   ├── MCTS-smart_Agent_winning.png
│   │   └── MCTS-smart_human_winning.png
│   └── name it connect4_Bradley_Titagwan.py
│
├── Task2_Sudoku/
│   ├── puzzles
│   │   └── sudoku.json
│   ├── report
│   │   └── Project Report.docx
│   ├── results (performance_plots)
│   │   ├──Comparison - Inf - FC vs MAC - for 9x9 40 empty.png
│   │   ├──Comparison - Inf - FC vs MAC - for 9x9 60 empty.png
│   │   ├──Comparison - Random vs MRV - for 9x9 40 empty.png
│   │   ├──Comparison - Value Selection - Standard Order vs LCV - for 9x9 40 empty.png
│   │   └──Comparison - Value Selection - Standard Order vs LCV - for 9x9 60 empty.png
│   └── Sudoku_Solver_Bradley_Titagwan.py
│
└── README.md

```

---

# 🤖 Algorithms Included

| Task | Algorithm | Purpose |
|------|-----------|----------|
| Connect-4 | Minimax | Decision-making for adversarial game play |
| Connect-4 | Alpha-Beta Pruning | Optimizes Minimax search by pruning unnecessary branches |
| Connect-4 | Monte Carlo Tree Search (MCTS) | Uses probabilistic simulations to determine optimal moves |
| Sudoku | Backtracking Search | Systematically searches for valid puzzle solutions |
| Sudoku | Forward Checking | Eliminates invalid variable assignments early |
| Sudoku | Maintaining Arc Consistency (MAC) | Maintains consistency among constraints during search |
| Sudoku | MRV & LCV Heuristics | Improves search efficiency through variable and value ordering |

---

# 📊 Results Summary

## Connect-4

- Compared Alpha-Beta Pruning against Monte Carlo Tree Search.
- Evaluated Random and Smart MCTS playout strategies.
- Recorded gameplay logs and generated performance visualizations.
- Demonstrated the effectiveness of heuristic search in adversarial game environments.

## Sudoku

- Solved Sudoku puzzles using Constraint Satisfaction techniques.
- Compared Forward Checking and Maintaining Arc Consistency.
- Evaluated the effects of MRV and LCV heuristics on search efficiency.
- Generated performance plots illustrating runtime improvements and heuristic effectiveness.

---

# 🚀 How to Run

## Task 1 — Connect-4

Run the Connect-4 game:

```bash
python connect4_Bradley_Titagwan.py
```

Select one of the available game modes:

- Human vs. Alpha-Beta
- Human vs. MCTS (Random Playouts)
- Human vs. MCTS (Smart Playouts)

---

## Task 2 — Sudoku Solver

Run the Sudoku solver:

```bash
python sudoku_solver_Bradley_Titagwan.py
```

The program loads the provided Sudoku puzzle and solves it using Constraint Satisfaction algorithms and configurable heuristics.

---

# 💻 Skills Demonstrated

- Artificial Intelligence
- Adversarial Search
- Game Tree Search
- Minimax
- Alpha-Beta Pruning
- Monte Carlo Tree Search
- Constraint Satisfaction Problems (CSP)
- Backtracking Algorithms
- Forward Checking
- Arc Consistency (MAC)
- Heuristic Design
- Algorithm Analysis
- Performance Benchmarking
- Python

---

# 📈 Future Improvements

- Implement iterative deepening for Alpha-Beta Search
- Parallelize Monte Carlo Tree Search simulations
- Add transposition tables for game search optimization
- Expand Sudoku support to additional puzzle sizes
- Compare CSP techniques with SAT-based Sudoku solvers

---

# 📄 Documentation

The repository includes:

- Source Code
- Gameplay Logs
- Performance Plots
- Solver Visualizations
- Project Report

The complete report can be found in each task's **report/** directory.

---

# 📬 Author

**Bradley Titagwan**

Version: v1.0
```
