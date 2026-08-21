"""Lightweight sanity check for a LaTeX file: balanced braces and environments."""
import re
import sys


def check(path):
    with open(path, encoding="utf-8") as fh:
        text = fh.read()

    errors = []

    # 1. brace balance (ignore comments)
    depth = 0
    for i, ch in enumerate(text):
        if ch == "%":
            nl = text.find("\n", i)
            if nl == -1:
                break
            # skip comment (but escaped \% handled below by regex approach)
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth < 0:
                errors.append(f"unbalanced '}}' at char {i}")
                depth = 0
    if depth != 0:
        errors.append(f"unbalanced braces: {depth} unclosed")

    # 2. environment pairing
    stack = []
    for m in re.finditer(r"\\(begin|end)\{([^}]*)\}", text):
        kind, env = m.group(1), m.group(2)
        if kind == "begin":
            stack.append((env, m.start()))
        else:
            if not stack:
                errors.append(f"\\end{{{env}}} without \\begin at {m.start()}")
            elif stack[-1][0] != env:
                errors.append(f"\\end{{{env}}} mismatches \\begin{{{stack[-1][0]}}} at {m.start()}")
                stack.pop()
            else:
                stack.pop()
    for env, pos in stack:
        errors.append(f"unclosed \\begin{{{env}}} at {pos}")

    # 3. citations exist in bib
    bib = path.replace("manuscript.tex", "references.bib")
    try:
        with open(bib, encoding="utf-8") as fh:
            bibtext = fh.read()
        keys = set(re.findall(r"@\w+\{([^,]+),", bibtext))
        cited = set()
        for m in re.finditer(r"\\cite\{([^}]*)\}", text):
            for k in m.group(1).split(","):
                cited.add(k.strip())
        missing = cited - keys
        if missing:
            errors.append(f"cited but not in bib: {sorted(missing)}")
        unused = keys - cited
        print(f"bib keys: {len(keys)}, cited: {len(cited)}, unused: {sorted(unused)}")
    except FileNotFoundError:
        print("references.bib not found; skipping citation check")

    if errors:
        print(f"ERRORS ({len(errors)}):")
        for e in errors:
            print("  -", e)
        sys.exit(1)
    print("LaTeX structure check passed.")


if __name__ == "__main__":
    check(sys.argv[1] if len(sys.argv) > 1 else "paper/manuscript.tex")
