"""Fetch the last two references via Crossref search with UTF-8 output."""
import json
import time

import requests


def search(query, rows=2):
    r = requests.get(
        "https://api.crossref.org/works",
        params={"query.bibliographic": query, "rows": rows},
        timeout=25,
        headers={"User-Agent": "research-check/1.0 (mailto:test@example.com)"})
    items = r.json()["message"]["items"]
    result = []
    for it in items:
        result.append({
            "title": (it.get("title") or [""])[0],
            "authors": "; ".join(
                f"{a.get('family', '')}, {a.get('given', '')}" for a in it.get("author", [])),
            "journal": (it.get("container-title") or [""])[0],
            "volume": it.get("volume", ""),
            "pages": it.get("page", ""),
            "year": (it.get("issued", {}).get("date-parts") or [[None]])[0][0],
            "doi": it.get("DOI"),
        })
    return result


out = {}
for key, query in [
    ("guidolin2016", "A weighted cellular automata 2D inundation model for rapid flood analysis"),
    ("ouyang2012_safety", "A three-stage resilience analysis framework for urban infrastructure systems"),
    ("issermann2020", "Efficient Urban Inundation Model for Live Flood Forecasting with Cellular Automata"),
]:
    try:
        out[key] = search(query)
        for it in out[key]:
            print(key, "|", it["year"], "|", it["title"][:60], "|", it["doi"])
    except Exception as exc:  # noqa: BLE001
        print("FAIL", key, exc)
    time.sleep(0.6)

with open("results/doi_search2.json", "w", encoding="utf-8") as fh:
    json.dump(out, fh, ensure_ascii=False, indent=1)
print("saved -> results/doi_search2.json")
