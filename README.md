# Advanced Algorithms Portfolio  

### by **Tanjil Siam** – BSc Computer Science, UWE Bristol



This repository contains my personal, portfolio‑ready implementations of several algorithmic tasks designed to demonstrate practical skills in **Python**, **data processing**, **backtracking**, **optimisation**, and **clean software engineering**.



Currently included:



---



## 📘 Activity 1.1 — Degree Classification Engine



A Python tool that calculates a student's university degree classification based on UWE’s credit‑weighted rules:



- Computes **Level 5 best 100 credits** (with fractional credit selection when needed)  

- Computes **Level 6 weighted average** (all L6 modules)  

- Applies final formula →  

  **Final Aggregate = (3 × Level 6 Average + Level 5 Average) / 4**  

- Determines classification: First, 2:1, 2:2, Third, or Fail  

- Checks **pass‑all‑modules** requirement  

- Outputs:

  - `degree_results.csv` → final numbers + classifications  

  - `l5_breakdown.csv` → which Level 5 modules were selected  



This implementation showcases data parsing, weighted optimisation, validation logic, and clean CSV output generation.



---



## 🔐 Activity 1.2 — Constrained Password Generator



A combinatorial password generator using **recursive backtracking** with heavy pruning for efficiency.



**Rules enforced:**

- Must include **at least one** uppercase, lowercase, digit, and special symbol  

- Must **start with a letter**  

- Maximum **2 uppercase letters**  

- Maximum **2 special symbols**  

- Character sets:

  - `A–E`, `a–e`, `1–5`, `{ $, &, % }`



**Features:**

- Generates **all valid passwords** for any length `L`  

- Outputs to: `output/passwords_L{L}.txt`  

- Matches official reference counts for:

  - `L = 4` → 4500  

  - `L = 5` → 207,000  

  - `L = 6` → 5,287,500  

- Optimised with:

  - Pruned search branches  

  - Efficient prefix tracking  

  - Buffered file writing (can handle millions of results)



---



## 📁 Repository Structure



AdvancedAlgorithms/ activity1_1/ degree_calculator.py activity1_1_marks.csv cs modules.csv output/ degree_results.csv l5_breakdown.csv

activity1_2/ password_generator.py output/ passwords_L4.txt passwords_L5.txt passwords_L6.txt

(activity1_3 and activity1_4 will be added later)



---



## 🚀 How to Run



### Activity 1.1 (Degree Calculator)

cd activity1_1 python degree_calculator.py



### Activity 1.2 (Password Generator)

cd activity1_2 python password_generator.py



---



## 🧑‍💻 About Me



**Tanjil Siam**  

BSc Computer Science, University of the West of England (UWE Bristol)  

Focused on algorithm design, optimisation, and practical engineering solutions.



---



## 📄 License



This is a personal portfolio repository.  

All code written by **Tanjil Siam**.
