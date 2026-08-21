"""Search Crossref by bibliographic query for the remaining references."""
import json
import time

import requests

QUERIES = [
    ("ouyang_review", "Review on modeling and simulation of interdependent critical infrastructure systems Ouyang"),
    ("bates2010", "A simple inertial formulation of the shallow water equations for efficient two dimensional flood inundation modelling"),
    ("guidolin2016", "A weighted cellular automata 2D inundation model for rapid flood analysis"),
    ("chang_shinozuka", "Measuring improvements in the disaster resilience of communities Chang Shinozuka"),
    ("ouyang2012_safety", "A three-stage resilience analysis framework for urban infrastructure systems Ouyang Dueñas-Osorio Min"),
    ("panteli2015", "The Grid Stronger Bigger Smarter Presenting a Conceptual Framework of Power System Resilience Panteli Mancarella"),
    ("hunter2007", "Adaptive time stepping in fast cellular automata flood inundation models Hunter"),
    ("batty2018", "Digital twins Batty Environment and Planning B"),
    ("dibaldassarre", "An Integrative Research Framework to Unravel the Two-Way Interplay between Human Society and Floods Di Baldassarre"),
]

out = {}
for key, query in QUERIES:
    try:
        r = requests.get(
            "https://api.crossref.org/works",
            params={"query.bibliographic": query, "rows": 3},
            timeout=25,
            headers={"User-Agent": "research-check/1.0 (mailto:test@example.com)"})
        items = r.json()["message"]["items"]
        print(f"\n=== {key} ===")
        for it in items:
            authors = "; ".join(
                f"{a.get('family', '')}, {a.get('given', '')}" for a in it.get("author", [])[:6])
            print(" -", it.get("title", [""])[0][:80])
            print("   ", authors[:120])
            print("   ", (it.get("container-title") or [""])[0][:60],
                  "vol", it.get("volume", ""), "pp", it.get("page", ""),
                  (it.get("issued", {}).get("date-parts") or [[None]])[0][0],
                  "DOI:", it.get("DOI"))
        out[key] = [
            {
                "title": (it.get("title") or [""])[0],
                "authors": "; ".join(
                    f"{a.get('family', '')}, {a.get('given', '')}" for a in it.get("author", [])),
                "journal": (it.get("container-title") or [""])[0],
                "volume": it.get("volume", ""),
                "pages": it.get("page", ""),
                "year": (it.get("issued", {}).get("date-parts") or [[None]])[0][0],
                "doi": it.get("DOI"),
            }
            for it in items
        ]
    except Exception as exc:  # noqa: BLE001
        print("FAIL", key, exc)
    time.sleep(0.6)

with open("results/doi_search.json", "w", encoding="utf-8") as fh:
    json.dump(out, fh, ensure_ascii=False, indent=1)
print("\nsaved -> results/doi_search.json")
