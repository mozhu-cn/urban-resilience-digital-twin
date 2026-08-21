"""Fetch remaining Crossref metadata (UTF-8 safe output)."""
import json
import time

import requests

DOIS = [
    "10.1016/j.envsoft.2016.07.006",   # Guidolin 2016 (correct DOI guess)
    "10.2166/hydro.2012.245",           # Ghimire 2013 CA urban flood
    "10.5194/hess-11-129-2007",         # Hunter 2007 adaptive time stepping
    "10.5194/hess-17-3295-2013",        # Di Baldassarre 2013 socio-hydrology
    "10.1109/MPRV.2008.80",             # Haklay & Weber 2008 OSM
    "10.1109/TII.2018.2873186",         # Tao 2019 digital twin industry
]

out = {}
for doi in DOIS:
    try:
        r = requests.get(
            f"https://api.crossref.org/works/{doi}", timeout=25,
            headers={"User-Agent": "research-check/1.0 (mailto:test@example.com)"})
        m = r.json()["message"]
        authors = "; ".join(
            f"{a.get('family', '')}, {a.get('given', '')}" for a in m.get("author", []))
        out[doi] = {
            "title": (m.get("title") or [""])[0],
            "authors": authors,
            "journal": (m.get("container-title") or [""])[0],
            "volume": m.get("volume", ""),
            "pages": m.get("page", ""),
            "year": (m.get("issued", {}).get("date-parts") or [[None]])[0][0],
            "doi": doi,
        }
        print("OK", doi, "|", out[doi]["year"], "|", out[doi]["title"][:70])
    except Exception as exc:  # noqa: BLE001
        print("FAIL", doi, type(exc).__name__, str(exc)[:80])
    time.sleep(0.6)

# Guidolin via search if DOI above failed
if "10.1016/j.envsoft.2016.07.006" not in out:
    try:
        r = requests.get(
            "https://api.crossref.org/works",
            params={"query.bibliographic": "A weighted cellular automata 2D inundation model for rapid flood analysis",
                    "rows": 1},
            timeout=25,
            headers={"User-Agent": "research-check/1.0 (mailto:test@example.com)"})
        it = r.json()["message"]["items"][0]
        out["guidolin_search"] = {
            "title": (it.get("title") or [""])[0],
            "authors": "; ".join(f"{a.get('family', '')}, {a.get('given', '')}" for a in it.get("author", [])),
            "journal": (it.get("container-title") or [""])[0],
            "volume": it.get("volume", ""),
            "pages": it.get("page", ""),
            "year": (it.get("issued", {}).get("date-parts") or [[None]])[0][0],
            "doi": it.get("DOI"),
        }
        print("GUIDOLIN-SEARCH OK ->", out["guidolin_search"])
    except Exception as exc:  # noqa: BLE001
        print("GUIDOLIN-SEARCH FAIL", exc)

with open("results/doi_meta2.json", "w", encoding="utf-8") as fh:
    json.dump(out, fh, ensure_ascii=False, indent=1)
print("saved -> results/doi_meta2.json")
