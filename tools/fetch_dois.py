"""Fetch exact citation metadata from Crossref for a list of DOIs."""
import json
import time

import requests

DOIS = [
    "10.1038/nature08932",          # Buldyrev 2010
    "10.1103/PhysRevLett.107.195701",  # Gao 2011
    "10.1063/1.4737204",            # Ouyang & Duenas-Osorio 2012 Chaos
    "10.1016/j.ress.2013.07.009",   # Ouyang 2014 RESS review
    "10.1016/j.jhydrol.2010.06.012",  # Bates 2010
    "10.1016/j.envsoft.2016.07.005",  # Guidolin 2016
    "10.1193/1.1623497",            # Bruneau 2003
    "10.1007/978-3-319-38756-7_4",  # Grieves & Vickers 2017
    "10.1109/37.969131",            # Rinaldi 2001
    "10.1193/1.1772536",            # Chang & Shinozuka 2004
    "10.1016/j.strusafe.2012.03.002",  # Ouyang et al. 2012 Structural Safety
    "10.1287/trsc.1090.0301",       # Laporte 2009 (guess)
    "10.1109/MPE.2015.2397324",     # Panteli & Mancarella 2015 (guess)
    "10.5194/hess-11-1049-2007",    # Hunter 2007 (guess)
    "10.1103/RevModPhys.74.47",     # Albert & Barabasi 2002
    "10.1137/S003614450342480",     # Newman 2003
    "10.1177/2399808318797316",    # Batty 2018 digital twins (guess)
    "10.1111/j.1753-318X.2012.01140.x",  # Di Baldassarre? (guess)
]

out = {}
for doi in DOIS:
    try:
        r = requests.get(
            f"https://api.crossref.org/works/{doi}", timeout=20,
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
    time.sleep(0.5)

with open("results/doi_meta.json", "w", encoding="utf-8") as fh:
    json.dump(out, fh, ensure_ascii=False, indent=1)
print("saved -> results/doi_meta.json")
