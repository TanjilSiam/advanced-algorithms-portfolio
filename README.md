# Advanced Algorithms Portfolio  
### by **Tanjil Siam** — BSc Computer Science, UWE Bristol

This repository contains my portfolio-ready Python implementations for the Advanced Algorithms coursework.  
Each activity demonstrates skills in **data processing**, **algorithm design**, **graph theory**,  
**optimisation**, **multiprocessing**, and **clean code structure**.

---

# 📘 Activity 1.1 — Degree Classification Engine

A complete automated degree classification calculator based on UWE's credit-weighted system.

### ✔ Features
- Extracts module credit + level from module codes  
- Calculates **Level 5 best 100 credits** (fractional credit support)  
- Computes **Level 6 weighted average**  
- Final score = **(3 × L6 + L5) / 4**  
- Generates:
  - `degree_results.csv`
  - `l5_breakdown.csv`

### ▶ Run
~~~bash
cd activity1_1
python degree_calculator.py
~~~

outputs are saved in:
activity1_1/output/

---

# 🔐 Activity 1.2 — Constrained Password Generator

Backtracking algorithm that generates all passwords of length L that satisfy:

### ✔ Constraints
- Starts with a letter  
- Must include uppercase, lowercase, digit, special  
- Max **2 uppercase**  
- Max **2 special**  
- Character sets:
  - `A–E`, `a–e`, `1–5`, `{ $, &, % }`

### ▶ Run
~~~bash
cd activity1_2
python password_generator.py
~~~

Outputs are saved in:
activity1_2/output/

---

# 🚆 Activity 1.3 — UK Railway Route Planner

Finds the **lowest-cost route** across the UK railway network while visiting required stations.

### ✔ Algorithm Overview
1. Builds a weighted graph from CSV (undirected)  
2. Normalises station names (case-insensitive, trims spaces)  
3. Runs **Dijkstra** from all “important nodes” (start, required, end)  
4. Tries all permutations of required stations  
5. Computes full route cost  
6. Reconstructs the complete station-by-station path  
7. Writes output to text + JSON

### ▶ Run
~~~bash
cd activity1_3
python route_planner.py
~~~

Outputs in:
activity1_3/output/

---

# ⚡ Activity 1.4 — Serial vs Parallel Image Processing (Multiprocessing)

Demonstrates the difference between **serial** CPU-bound execution and **parallel** execution using multiprocessing.

### ✔ What this activity does
- A **serial script** processes images one at a time  
- A **parallel script** processes many images simultaneously using `ProcessPoolExecutor`  
- Both attempt to load images, detect faces, and compare them to a known reference face  
- The parallel version reduces total runtime by distributing work across CPU cores  

### 🧠 Learning Outcomes
- Understand multiprocessing concepts  
- Use workers, task distribution, and result collection  
- Handle file-level errors safely  
- Compare serial vs parallel execution time  

### ▶ Run
~~~bash
cd activity1_4

# Serial version
python activity1_4_serial.py

# Parallel version
python parallel_search.py
~~~

### 📄 Output
The parallel script generates:

activity1_4/output/matches.txt

Containing:
- total elapsed time  
- list of any matches  
- file-level errors (if any)

### 📌 Note  
The dataset includes **very small facial images**, which may affect detection performance.  
The focus of the activity is on **parallelisation**, not on perfect detection accuracy.

---

# 📁 Project Structure

~~~text
AdvancedAlgorithms/
├── activity1_1/
│   ├── degree_calculator.py
│   ├── activity1_1_marks.csv
│   ├── cs modules.csv
│   └── output/
│       ├── degree_results.csv
│       └── l5_breakdown.csv
│
├── activity1_2/
│   ├── password_generator.py
│   └── output/
│       ├── passwords_L4.txt
│       ├── passwords_L5.txt
│       └── passwords_L6.txt
│
├── activity1_3/
│   ├── route_planner.py
│   ├── activity1_3_railnetwork_data.csv
│   ├── task1_3_UK_Railway_Map.pdf
│   └── output/
│       ├── route_result.txt
│       └── route_debug.json
│
├── activity1_4/
│   ├── activity1_4_serial.py
│   ├── parallel_search.py
│   ├── dataset/
│   │   └── task1_4/
│   │       ├── known_man.jpg
│   │       └── imageset/
│   │           ├── img1.jpg
│   │           ├── img2.jpg
│   │           ├── ...
│   └── output/
│       └── matches.txt
│
├── .gitignore
└── README.md
~~~

---

# 🧑‍💻 About Me

**Tanjil Siam**  
BSc Computer Science — UWE Bristol  
I focus on designing clean, efficient algorithmic solutions with a strong emphasis on readability and optimisation.

---

# 📄 License  
Personal academic portfolio — all work authored by **Tanjil Siam**.