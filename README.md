# Advanced Algorithms Portfolio  

### by **Tanjil Siam** – BSc Computer Science, UWE Bristol



This repository contains my portfolio‑ready Python implementations for the **Advanced Algorithms** coursework at UWE Bristol.  

Each activity demonstrates skills in **data processing**, **algorithm design**, **optimisation**, **graph theory**, **path‑finding**, and **backtracking**.



---



## 📘 Activity 1.1 — Degree Classification Engine



A complete, automated degree classification calculator following UWE’s credit‑weighted rules.



### Features

- Extracts **level** and **credit** from module codes  

- Computes **Level 5 best 100 credits** (supports fractional credit usage when required)  

- Computes **Level 6 weighted average**  

- Applies UWE formula: **(3 × L6 Average + L5 Average) / 4**  

- Applies classification bands (First, 2:1, 2:2, Third, Fail)  

- Checks **pass‑all‑modules** rule  

- Outputs:

  - `degree_results.csv`

  - `l5_breakdown.csv`



### ▶ Run

~~~bash

cd activity1_1

python degree_calculator.py

~~~



---



## 🔐 Activity 1.2 — Constrained Password Generator



A combinatorial password generator using efficient **backtracking + pruning**.



### Rules

- Must include: uppercase, lowercase, digit, special symbol  

- Must **start with a letter**  

- Max **2 uppercase** characters  

- Max **2 special** characters  

- Character sets:

  - A–E  

  - a–e  

  - 1–5  

  - $, &, %



### Expected counts (for validation)

- L = 4 → **4500**  

- L = 5 → **207000**  

- L = 6 → **5287500**



### ▶ Run

~~~bash

cd activity1_2

python password_generator.py

~~~



Outputs saved in:

activity1_2/output/



---



## 🚆 Activity 1.3 — UK Railway Route Planner



A shortest‑route engine using the full **UK rail network** dataset (500+ stations).



### Task

Given:

- **start** station  

- **end** station  

- **required** stations (must be visited exactly once)



Find the **lowest‑cost route** that starts at the start station, visits all required stations, and ends at the destination.



### Algorithm (high level)

1. Load railway CSV (undirected, weighted graph)  

2. Normalise station names (case‑insensitive, trims whitespace)  

3. Identify important nodes (start + required + end)  

4. Compute **Dijkstra** shortest paths between important nodes  

5. Try all permutations of the required stations  

6. Sum segment costs, choose the **cheapest** ordering  

7. Rebuild the **full station‑by‑station route**  

8. Save results as text + JSON



### ▶ Run

~~~bash

cd activity1_3

python route_planner.py

~~~



Example input (interactive prompts):

london
 
exeter st davids

 bristol temple meads, reading



Outputs saved in:

activity1_3/output/



---

## ⚡ Activity 1.4 — Serial vs Parallel Image Processing (Multiprocessing)

Activity 1.4 demonstrates how serial execution compares to parallel execution when processing a batch of images.  
The goal is to show how a CPU‑bound task (such as scanning many image files and performing analysis on each one) can be accelerated using Python's multiprocessing capabilities.

### 🔍 What the task involves
- A **serial version** that processes images one by one in a loop.
- A **parallel version** using `ProcessPoolExecutor` to distribute image-processing work across CPU cores.
- Both scripts attempt to load images, detect faces, and compare them to a known reference encoding.
- CPU‑bound workloads benefit greatly from parallel execution, reducing overall wall‑clock time.

### 🧠 Key learning outcomes
- How to structure a multiprocessing program in Python.
- How to manage worker initialization and data sharing.
- Safe handling of per‑file errors when processing large batches.
- Understanding the difference between serial throughput and parallel throughput.

### ▶ Run
```bash
# Serial version
python activity1_4_serial.py

# Parallel version
python parallel_search.py
📄 Output
The parallel script produces a summary file:
activity1_4/output/matches.txt
This includes:
total elapsed time,
list of matches,
and any file‑level errors encountered.
📌 Note
The provided dataset contains small facial images. While the detection library may not identify all faces reliably on every machine, the parallelisation logic, structure, and overall design are correct and fulfil the task's intent.

---


## Project Structure



~~~

AdvancedAlgorithms/

├── activity1_1/

│   ├── degree_calculator.py            # Degree classification engine

│   ├── activity1_1_marks.csv           # Raw marks dataset

│   ├── cs modules.csv                  # Module info

│   └── output/                         # Generated CSV outputs

│       ├── degree_results.csv

│       └── l5_breakdown.csv

│

├── activity1_2/

│   ├── password_generator.py           # Backtracking password generator

│   └── output/                         # Generated password lists

│       ├── passwords_L4.txt

│       ├── passwords_L5.txt

│       └── passwords_L6.txt

│

├── activity1_3/

│   ├── route_planner.py                # UK rail network route optimiser

│   ├── activity1_3_railnetwork_data.csv # Railway connections dataset

│   ├── task1_3_UK_Railway_Map.pdf       # Reference map

│   └── output/                          # Route result files

│       ├── route_result.txt

│       └── route_debug.json

│

├── .gitignore                           # Git ignore rules

└── README.md                            # This file

~~~



## 🧑‍💻 About Me



**Tanjil Siam**  

BSc Computer Science — **UWE Bristol**



I focus on clean, efficient algorithmic solutions and practical engineering with clear outputs and reproducibility.



---



## 📄 License



This is a personal portfolio repository.  

All code written by **Tanjil Siam**.