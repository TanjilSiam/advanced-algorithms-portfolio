# degree_calculator.py
# -------------------------------------------------------------
# UWE Advanced Algorithms - Activity 1.1 Degree Calculator
# Inputs:
#   - activity1_1_marks.csv  (headerless, wide: student_id, code1, mark1, code2, mark2, ...)
#   - cs modules.csv         (module_code, module_name)
#
# Outputs:
#   - output/degree_results.csv
#   - output/l5_breakdown.csv  (shows which L5 modules were used + credits taken)
#
#Done by: Tanjil Siam , ID: 24024535
# -------------------------------------------------------------

import csv
import re
from pathlib import Path
from typing import List, Tuple, Optional, Dict

# ---- File names (as present in your folder) ----
MARKS_CSV = "activity1_1_marks.csv"
MODULES_CSV = "cs modules.csv"

# ---- Outputs ----
OUT_DIR = Path("output")
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_MAIN = OUT_DIR / "degree_results.csv"
OUT_L5 = OUT_DIR / "l5_breakdown.csv"


# ---------- Helpers ----------

def parse_code(code: str) -> Tuple[Optional[int], Optional[int]]:
    """
    Extract credits and year from module codes like 'UFCFHS-30-1' (credits=30, year=1).
    Your marks CSV uses this '...-<credits>-<year>' pattern. """
    m = re.search(r"-([0-9]+)-([0-9]+)$", code.strip())
    if not m:
        return None, None
    return int(m.group(1)), int(m.group(2))  # credits, year(1/2/3)


def classify(mark: float) -> str:
    if mark >= 70.0: return "First"
    if mark >= 60.0: return "Upper Second (2:1)"
    if mark >= 50.0: return "Lower Second (2:2)"
    if mark >= 40.0: return "Third"
    return "Fail"


def weighted_avg(items: List[Tuple[float, float]]) -> Optional[float]:
    """
    items: list of (mark, credits_taken). credits_taken can be fractional."""
    total_c = sum(c for _, c in items)
    if total_c == 0:
        return None
    return sum(m * c for m, c in items) / total_c


def best_100_credits(level5: List[Tuple[str, float, int]]) -> Tuple[List[Tuple[str, float, float]], str]:
    """
    level5: list of (code, mark, credits) for Level 5 modules.
    Strategy:
      - Sort by mark DESC.
      - Take whole modules until adding the next would exceed 100.
      - If the next would exceed 100, take just the FRACTION needed to hit exactly 100.
    Returns:
      chosen: [(code, mark, credits_taken)]   # credits_taken may be fractional
      note: optional note string
    """
    target = 100.0
    chosen: List[Tuple[str, float, float]] = []
    used = 0.0
    note = ""

    for code, mark, cr in sorted(level5, key=lambda x: x[1], reverse=True):
        if used >= target:
            break
        remain = target - used
        take = float(cr) if cr <= remain else remain
        if take > 0:
            chosen.append((code, mark, take))
            used += take
            if take < cr:
                note = "Used partial credits from one module to reach exactly 100."
                break

    if used < target:
        note = f"Only {used:.1f} L5 credits available in data."
    return chosen, note


def read_marks_wide(path: str):
    """
    Read headerless 'wide' CSV:
      student_id, code1, mark1, code2, mark2, ...
    Yields (student_id, [(code, mark), ...]) """
    with open(path, newline="", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line:
                continue
            parts = [p.strip() for p in line.split(",")]
            sid = parts[0]
            pairs = []
            i = 1
            while i + 1 < len(parts):
                code = parts[i]
                mark_s = parts[i + 1]
                if code:
                    try:
                        mark = float(mark_s)
                        pairs.append((code, mark))
                    except ValueError:
                        # skip non-numeric cells if any
                        pass
                i += 2
            yield sid, pairs


def read_modules_map(path: str) -> Dict[str, str]:
    """
    Read 'cs modules.csv' where each line is: code,name
    Returns: dict code -> name """
    mapping = {}
    if not Path(path).exists():
        return mapping
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if not row or not row[0].strip():
                continue
            code = row[0].strip()
            name = row[1].strip() if len(row) > 1 else ""
            mapping[code] = name
    return mapping


# ---------- Main ----------

def main():
    # (Optional) progress prints so you see it runs
    print(">>> START degree_calculator")
    print("CWD:", Path.cwd())
    print("Inputs exist?",
          "marks:", Path(MARKS_CSV).exists(),
          "modules:", Path(MODULES_CSV).exists())

    # 1) Open outputs FIRST so headers are always written
    with open(OUT_MAIN, "w", newline="", encoding="utf-8") as f_main, \
         open(OUT_L5, "w", newline="", encoding="utf-8") as f_l5:

        main_writer = csv.writer(f_main)
        l5_writer = csv.writer(f_l5)

        main_writer.writerow([
            "student_id", "L5_avg", "L6_avg",
            "final_aggregate", "classification",
            "passed_all_modules", "notes"
        ])
        l5_writer.writerow([
            "student_id", "module_code", "module_name", "mark", "credits_taken"
        ])

        # 2) Load inputs safely
        try:
            marks_rows = list(read_marks_wide(MARKS_CSV))
            print("Loaded students:", len(marks_rows))
            if not marks_rows:
                print("No rows found in marks file. Done (headers only).")
                print(">>> DONE. Wrote outputs to:", OUT_DIR)
                return
        except Exception as e:
            print("!! ERROR reading marks file:", e)
            print(">>> DONE. Wrote headers only to:", OUT_DIR)
            return

        try:
            modules_map = read_modules_map(MODULES_CSV)
        except Exception as e:
            print("!! WARNING reading modules map:", e)
            modules_map = {}

        # 3) Per-student processing
        processed = 0
        for sid, pairs in marks_rows:
            # Parse credits/year out of module codes
            enriched = []
            unknown_codes = []
            for code, mark in pairs:
                cr, yr = parse_code(code)
                if cr is None or yr is None:
                    unknown_codes.append(code)
                else:
                    enriched.append((code, mark, cr, yr))

            # Pass-all rule across Years 1–3 (>= 40)
            passed_all = all(mark >= 40.0 for _, mark, _, _ in enriched)

            # Level 5 (year == 2): best 100 credits
            l5_full = [(c, m, cr) for c, m, cr, yr in enriched if yr == 2]
            l5_chosen, l5_note = best_100_credits(l5_full)
            l5_avg = weighted_avg([(m, c_taken) for _, m, c_taken in l5_chosen])

            # Write breakdown rows for demo/report
            for code, mark, taken in l5_chosen:
                l5_writer.writerow([
                    sid, code, modules_map.get(code, ""), f"{mark:.2f}", f"{taken:.2f}"
                ])

            # Level 6 (year == 3): ALL modules
            l6_full = [(c, m, cr) for c, m, cr, yr in enriched if yr == 3]
            l6_avg = weighted_avg([(m, cr) for _, m, cr in l6_full])

            # Notes & classification
            final_agg = None
            cls = "Insufficient data"
            notes = l5_note if l5_note else ""
            if unknown_codes:
                notes += (" " if notes else "") + f"Unknown codes ignored: {unknown_codes}"

            if l5_avg is not None and l6_avg is not None:
                final_agg = (3.0 * l6_avg + l5_avg) / 4.0
                cls = classify(final_agg)
                if not passed_all:
                    notes += (" " if notes else "") + \
                             "Has failed module(s); degree award not permitted by regulations."

            main_writer.writerow([
                sid,
                f"{l5_avg:.2f}" if l5_avg is not None else "",
                f"{l6_avg:.2f}" if l6_avg is not None else "",
                f"{final_agg:.2f}" if final_agg is not None else "",
                cls,
                "Yes" if passed_all else "No",
                notes
            ])
            processed += 1

        print("Processed:", processed)
        print(">>> DONE. Wrote outputs to:", OUT_DIR)


# ---- Entry point (make sure this is EXACT) ----
if __name__ == "__main__":
    main()
