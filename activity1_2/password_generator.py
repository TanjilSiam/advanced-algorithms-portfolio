# password_generator.py
# -------------------------------------------------------------
# UWE Advanced Algorithms - Activity 1.2 Password Generator
# Rules:
#   - Character sets:
#       UPPERS  = {A, B, C, D, E}
#       LOWERS  = {a, b, c, d, e}
#       DIGITS  = {1, 2, 3, 4, 5}
#       SPECIAL = {$, &, %}
#   - Must include at least one character from EACH category
#   - Must START with a letter (upper or lower)
#   - At most TWO uppercase letters in total
#   - At most TWO special symbols in total
# Input:
#   - Read integer length L from console
# Output:
#   - Write ALL valid passwords with 1-based indices to output/passwords_L{L}.txt
#   - Print total count and (if L in {4,5,6}) expected counts for quick validation
# -------------------------------------------------------------

import sys
from pathlib import Path
from time import perf_counter

UPPERS = "ABCDE"
LOWERS = "abcde"
DIGITS = "12345"
SPECIAL = "$&%"
ALL_CHARS = UPPERS + LOWERS + DIGITS + SPECIAL

EXPECTED = {4: 4500, 5: 207000, 6: 5287500}

OUT_DIR = Path("output")
OUT_DIR.mkdir(parents=True, exist_ok=True)


def generate_passwords(L: int, out_path: Path) -> int:
    """Generate all valid passwords of length L to out_path. Returns total count.
    Uses backtracking with pruning; writes incrementally to avoid huge memory use."""
    buffer = []
    BUFSIZE = 100_000  # adjust if needed
    count = 0

    # Use list for prefix for faster append/pop; we join only when writing
    prefix = []

    def can_still_satisfy(remaining: int, has_u: bool, has_l: bool, has_d: bool, has_s: bool) -> bool:
        need = (0 if has_u else 1) + (0 if has_l else 1) + (0 if has_d else 1) + (0 if has_s else 1)
        return remaining >= need

    def backtrack(pos: int, upper_cnt: int, special_cnt: int, has_u: bool, has_l: bool, has_d: bool, has_s: bool):
        nonlocal count
        remaining = L - pos
        if not can_still_satisfy(remaining, has_u, has_l, has_d, has_s):
            return

        if pos == L:
            # all category flags must be True (guaranteed by prune)
            count += 1
            # write line: "index password"\n
            pwd = ''.join(prefix)
            buffer.append(f"{count} {pwd}\n")
            if len(buffer) >= BUFSIZE:
                out_f.write(''.join(buffer))
                buffer.clear()
            return

        # choices for this position
        if pos == 0:
            # must start with a letter (upper or lower)
            choices = UPPERS + LOWERS
        else:
            choices = ALL_CHARS

        # cap constraints
        if upper_cnt >= 2:
            # remove uppers
            choices = choices.replace('A','').replace('B','').replace('C','').replace('D','').replace('E','')
        if special_cnt >= 2:
            # remove specials
            for ch in SPECIAL:
                choices = choices.replace(ch, '')

        # iterate choices
        for ch in choices:
            prefix.append(ch)
            if ch in UPPERS:
                backtrack(pos+1, upper_cnt+1, special_cnt, True, has_l, has_d, has_s)
            elif ch in LOWERS:
                backtrack(pos+1, upper_cnt, special_cnt, has_u, True, has_d, has_s)
            elif ch in DIGITS:
                backtrack(pos+1, upper_cnt, special_cnt, has_u, has_l, True, has_s)
            else:  # special
                backtrack(pos+1, upper_cnt, special_cnt+1, has_u, has_l, has_d, True)
            prefix.pop()

    with out_path.open('w', encoding='utf-8') as out_f:
        backtrack(0, 0, 0, False, False, False, False)
        if buffer:
            out_f.write(''.join(buffer))
            buffer.clear()

    return count


def main():
    try:
        L_s = input("Enter password length (integer, >=4 is meaningful): ").strip()
        L = int(L_s)
    except Exception:
        print("Please enter a valid integer.")
        sys.exit(1)

    if L < 1:
        print("Length must be at least 1 (note: to satisfy all rules, 4+ makes sense).")
        sys.exit(1)

    out_path = OUT_DIR / f"passwords_L{L}.txt"
    t0 = perf_counter()
    total = generate_passwords(L, out_path)
    t1 = perf_counter()

    print(f"Wrote {total} passwords to {out_path}")
    if L in EXPECTED:
        print(f"Expected (from coursework guidance) for L={L}: {EXPECTED[L]}")
        if total == EXPECTED[L]:
            print("✔ Count matches expected.")
        else:
            print("✘ Count differs from expected — recheck constraints.")
    else:
        print("No reference count provided for this L; just ensure rules are satisfied.")

    print(f"Time taken: {t1 - t0:.2f} seconds")


if __name__ == "__main__":
    main()
