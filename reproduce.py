#!/usr/bin/env python3
"""
reproduce.py -- The AI Constraint Relay reproduction script (v5 DATA-FIRST).

Assistance disclosure: AI-assisted drafting (Anthropic Opus 5.0 / Google DeepMind Gemini 3.7).

Philosophy: let the raw numbers speak. This tabulates the verifiable, sourced
metrics behind each risk factor (supply_constraints.csv). It does NOT score,
weight, or rank them -- the v1 "Likelihood x Severity" product was retired
because assigning 1-5 ratings dresses judgment as measurement (false precision).

v5 incorporates the verified Lake Powell / Reclamation trace correction (July
2026 Min Probable 3,503.65 ft year-end projection vs 3,490 ft power pool, noting
the vintage mismatch across traces).

Edit the CSV and re-run to reproduce every figure. Std-lib only.
$ python3 reproduce.py
"""
import csv, os
from itertools import groupby

HERE = os.path.dirname(os.path.abspath(__file__))


def load(name):
    with open(os.path.join(HERE, name), newline="") as f:
        return list(csv.DictReader(f))


def constraints():
    rows = load("supply_constraints.csv")
    print("=" * 78)
    print("THE CONSTRAINT RELAY (v5) -- verifiable, sourced metrics (the raw spine)")
    print("=" * 78)
    for factor, items in groupby(rows, key=lambda r: r["factor"]):
        print(f"\n  {factor}")
        for r in items:
            print(f"    - {r['metric']}: {r['value']}")
            print(f"        [{r['source']}, {r['vintage']}]")
    print()


def main():
    constraints()
    print("-" * 78)
    print("READ: the constraints above are sourced DATA. The 'constraint relay' (where")
    print("bottlenecks hydraulically displace from logic to grid, to price collars,")
    print("to volume deficits, to on-site generation, to turbine castings, to inelastic")
    print("5-year journeyman labour pipelines, and to consumer memory incidence) is")
    print("INTERPRETATION of that data -- labelled as judgment, not measured risk.")
    print("No L/S scores are asserted.")
    print()
    print("CONCLUSION: The register documents a system under continuous hydraulic")
    print("displacement. The non-relocatable tail risks (Taiwan Strait, licensed rare")
    print("earths, Spruce Pine high-purity quartz) represent physical boundaries where")
    print("re-routing is impossible. The register serves as a living referee layer.")


if __name__ == "__main__":
    main()
