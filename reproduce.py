#!/usr/bin/env python3
"""
reproduce.py -- Barbell Risk Assessment v3 (DATA-FIRST).

Philosophy: let the raw numbers speak. This tabulates the verifiable, sourced
metrics behind each risk factor (supply_constraints.csv). It does NOT score,
weight, or rank them -- the v1 "Likelihood x Severity" product was retired
because assigning 1-5 ratings dresses judgment as measurement (false precision).

v3 renumbers the factors from F1-F5 to 1-6, folds the old F5 (critical minerals)
into 4 alongside the physical chokepoints, and promotes two forces from cost
amplifiers to factors: 5 commoditisation from below, and 6 export controls.
The CSV also carries the factor-5 inverse-risk row (the over-capacity tail) with
its upgrade trigger attached, and the v3 corrections (Lake Powell deferred;
per-query energy revised down; the minerals review stated as a month, not a day).

The "barbell" reading is INTERPRETATION drawn from these numbers, and is labelled
as such -- judgment, not measured risk.

Edit the CSV and re-run to reproduce every figure.  Std-lib only.
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
    print("THE SIX FACTORS -- verifiable, sourced metrics (the raw spine)")
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
    print("READ: the constraints above are sourced DATA. The 'barbell' (a volatile")
    print("base case in factors 1-2 + a low-probability / uncapped-severity tail in")
    print("factor 3 Taiwan and the licensed-materials leg of factor 4) is")
    print("INTERPRETATION of that data -- labelled as judgment, not measured risk.")
    print("No L/S scores are asserted.")
    print()
    print("SHAPE: 'fragile to catastrophe, robust to defection' was tested against")
    print("the 2026 over-capacity evidence and RETAINED. The glut is carried as a")
    print("named inverse-risk row under factor 5, with an upgrade trigger; none of")
    print("its conditions was present at 21 Jul 2026. If they fire, the shape does")
    print("not invert, it COLLAPSES to a single mode of stranded assets, and the")
    print("register needs rebuilding not amending. The barbell is a bimodal")
    print("scenario model for capital allocation, not a probability distribution.")


if __name__ == "__main__":
    main()
