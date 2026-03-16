# Advanced Algorithms Portfolio  

### by **Tanjil Siam** – BSc Computer Science, UWE Bristol



This repository contains my personal, portfolio‑ready Python implementations for the Advanced Algorithms module.  

Each activity demonstrates practical skills in **data processing**, **algorithm design**, **optimisation**, **graph theory**, **backtracking**, and **clean software engineering**.



---



# 📘 **Activity 1.1 — Degree Classification Engine**



A fully automated degree classification calculator following UWE’s credit‑weighted rules.



### ✅ Features

- Parses module codes to extract **credits** and **level**  

- Computes **Level 5 best 100 credits** using weighted selection (supports fractional credits when required)  

- Computes **Level 6 weighted average** from all L6 modules  

- Applies UWE’s final formula:  

  **Final Aggregate = (3 × L6 Average + L5 Average) / 4**  

- Performs **“pass all modules”** validation  

- Outputs two CSV files:

  - `degree_results.csv` → aggregate + classification  

  - `l5_breakdown.csv` → modules chosen for best‑100 L5 calculation  



### ▶ Run

```bash

cd activity1_1

python degree_calculator.py



---



🔐 Activity 1.2 — Constrained Password Generator

A combinatorial password generator using efficient backtracking + pruning.

🔑 Rules enforced

Must include uppercase, lowercase, digit, special symbol
Must start with a letter
Max 2 uppercase characters
Max 2 special characters
Character sets:
A–E, a–e, 1–5, { $, &, % }
📈 Validation

Matches official expected counts:

L=4 → 4500
L=5 → 207,000
L=6 → 5,287,500
▶ Run

cd activity1_2

python password_generator.py

Outputs are written to:
activity1_2/output/passwords_L{L}.txt



---



🚆 Activity 1.3 — UK Railway Route Planner

A shortest‑route optimisation tool operating on the full UK railway network dataset (over 500 stations).

🎯 Task

Given:

a start station
an end station
a list of required stations
The program finds the lowest‑cost route that visits all required stations exactly once and ends at the destination.

🔧 Core Algorithm

Loads the railway graph from activity1_3_railnetwork_data.csv (undirected weighted edges).
Normalises station names (case‑insensitive, whitespace‑tolerant).
Identifies “important stations”: start + required + end.
Runs Dijkstra from each important station.
Tries all permutations of required stations to compute total cost.
Selects the cheapest permutation.
Rebuilds full station‑by‑station route.
Saves human‑readable and JSON debug outputs.
📄 Output files

output/route_result.txt
output/route_debug.json
▶ Run

cd activity1_3

python route_planner.py

Example input:

Enter start station: london

Enter end station: exeter st davids

Enter required stations (comma separated): bristol temple meads,reading



---



📁 Repository Structure

AdvancedAlgorithms/

  activity1_1/

    degree_calculator.py

    activity1_1_marks.csv

    cs modules.csv

    output/...



  activity1_2/

    password_generator.py

    output/...



  activity1_3/

    route_planner.py

    activity1_3_railnetwork_data.csv

    task1_3_UK_Railway_Map.pdf

    output/...



  .gitignore

  README.md



---



🧑‍💻 About Me

Tanjil Siam
BSc Computer Science
University of the West of England (UWE Bristol)

I focus on algorithm design, optimisation, clean engineering, and writing solutions that are efficient, reproducible, and easy to understand.



---



📄 License

This is a personal portfolio repository.
All code written by Tanjil Siam.



---