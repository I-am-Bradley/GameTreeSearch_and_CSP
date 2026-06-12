# GameTreeSearch_and_CSP
### Connect‑4 AI (Alpha‑Beta & MCTS) + Sudoku CSP Solver  
Author: Bradley Titagwan

This repository contains my full implementation for Project 2, covering:

- **Connect‑4 AI using Alpha‑Beta Pruning**
- **Monte Carlo Tree Search (Random & Smart Playouts)**
- **Sudoku Solver using CSP + Backtracking + Heuristics**

All results, logs, and plots referenced in the report are included in their respective folders.

---

## 📁 Repository Structure

Project2/  
│  
├── README.md  
│  
├── Task1_Connect4/                
│   ├── name it connect4_Bradley_Titagwan.py              
│   │
│   ├── logs/  
│   │   ├── ab_depth_timeline.csv  
│   │   ├── mcts_random_log.txt        # too large to load, but include in repo  
│   │   ├── mcts_smart_log_(C1.41).txt  
│   │   ├── mcts_smart_log_(C2).txt  
│   │  
│   ├── results/  
│   │   ├── screenshots/               # all terminal screenshots you uploaded  
│   │   │   ├── AB_computer_winning.png  
│   │   │   ├── AB_Human_winning.png  
│   │   │   ├── MCTS_-random_Human_winning.png  
│   │   │   ├── MCTS-smart_Agent_winning.png  
│   │   │   └── MCTS-smart_human_winning.png  
│   │   ├── plots/                     # performance charts (inference, MRV, LCV)  
│   │  
│   ├── data/  
│   │   └── connect4 website.txt       # reference link  
│   │  
│   └── report/  
│       └── CS Project 2 Report.docx  
│  
├── Task2_Sudoku/  
│   ├── sudoku_solver_Bradley_Titagwan.py               # your solver (placeholder)  
│   │  
│   ├── puzzles/  
│   │   └── sudoku.json                # the 16×16 puzzle you uploaded  
│   │  
│   ├── results/  
│   │   ├── performance_plots/         # MRV vs Random, FC vs MAC, LCV vs Standard  
│   │   └── solved_examples/           # solved puzzle outputs (optional)  
│   │  
│   └── report/  
│       └── CS Project 2 Report.docx   # same report or separate if needed  
│  
└── LICENSE (optional)  


---

## 🚀 How to Run

### **Connect‑4 Agents**

**"python connect4_game.py"**

You will be prompted to choose:
- Human vs Alpha‑Beta  
- Human vs MCTS‑Random  
- Human vs MCTS‑Smart  

### **Sudoku Solver**

**"python sudoku_csp/sudoku_solver.py"**

---

## 📄 Documentation
The full project report is included as:

**Project Report.docx**
