# AI Capital-Infrastructure Barbell — reproduction bundle (v3)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20586863.svg)](https://doi.org/10.5281/zenodo.20586863)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
![Python 3](https://img.shields.io/badge/python-3-blue.svg)
![No dependencies](https://img.shields.io/badge/dependencies-none%20(stdlib)-brightgreen.svg)


A risk assessment of the AI compute build-out. **Method-first, not a crash call.**
Most AI-infrastructure commentary argues over *demand* (can revenue justify the capex);
this takes the *supply* side, meaning the physical, material, and geographic limits on
building and running the compute, and shows the shape of risk those limits create: a
**barbell**. A high-probability base case (volatile, energy-constrained growth with sharp
capital corrections) sits at one end; a low-probability, uncapped-severity tail (Taiwan
Strait, licensed materials) at the other; the middle is thin. The compute layer appears
resilient to ordinary competitive shocks but fragile to a single macro-systemic one.

> **Version history.** v1 (DOI 10.5281/zenodo.20586864) → v2 (10.5281/zenodo.20707214) →
> v2.1 (10.5281/zenodo.20708803) → v2.2 (10.5281/zenodo.21191963) → v3. Concept DOI
> 10.5281/zenodo.20586863. ("v2.x / v3" is the author's scheme; Zenodo assigns its own
> version DOI.)
>
> **v3 is the first version to change the register's structure.** The five factors F1–F5
> are renumbered **① to ⑥** to match the register the companion PESTLE scan
> cross-references; the old F5 (critical minerals) folds into ④ beside the physical
> chokepoints; and two forces are **promoted from cost amplifiers to factors**:
> **⑤ commoditisation from below** (because it can invert the shortage premise the other
> factors rest on) and **⑥ export controls** (because the June 2026 model-access episode
> acted on availability, not on cost). The stated scope is correspondingly wider than
> v2.2's strictly supply-side framing, and §1 of the paper argues each promotion rather
> than assuming it.
>
> **Earlier:** **v2** dropped the 1–5 likelihood/severity scores as "dressing judgment as
> measurement", added F5 critical-minerals, added a falsifiable triggers table, and
> corrected the PJM data-centre cost ($23.1B → **$13.8B**, via Monitoring Analytics) and
> the Nanya figure (**+583%** YoY Q1 2026, off a trough, price-driven). **v2.1:** corrected
> the Wood Mackenzie transformer-survey vintage (**Q2 2025**) and added the DOE 60-month
> EHV tail; second-sourced the heavy-REE price to the **IEA**. **v2.2 (external red-team):**
> reconciled the supply-side scope with F1; clarified Nanya as a commodity-DRAM maker (a
> DRAM-leg read, not an HBM proxy); softened the lithography remote-disable claim to
> "reportedly capable".

## On method (the honest split)

The constraints in the paper's §2 are verifiable, sourced, dated numbers, and they carry
the argument. The "barbell" reading is *interpretation of* those numbers and is labelled
as such. No likelihood/severity scores are asserted: assigning 1–5 ratings would dress
judgment as measurement. Thresholds in the triggers table are the **author's**, chosen to
be checkable rather than derived from a source.

For this edition the event-driven and structural claims were checked against their issuing
sources as part of the companion PESTLE scan v1.0 (DOI 10.5281/zenodo.21466083). Market-live
readings are 21 July 2026 readings and will move. Where two sources give different values
for the same quantity, both are shown rather than averaged.

## Contents

| File | What it is |
|---|---|
| `barbell_v3.md` | The paper (Markdown source, the thing you edit). |
| `The AI Capital-Infrastructure Barbell v3.pdf` | The paper (readable PDF). |
| `reproduce.py` | Tabulates and cites every figure from the CSV. Standard library only. |
| `supply_constraints.csv` | Every metric with its value, source, and vintage (the data layer). |
| `README.md` | This file. |

*Rendering:* `bash "House style/render_pdf.sh" barbell_v3.md "The AI Capital-Infrastructure Barbell v3.pdf"`
(markdown → house-style HTML → headless print to PDF, in one command).

## Reproduce

```bash
python3 reproduce.py
```

`reproduce.py` is honest about what it is: this is a **register, not a calculation**. The
script reads `supply_constraints.csv` and prints each metric with its source and vintage,
then the interpretive barbell reading and the shape verdict. Edit the CSV and re-run to
reproduce every figure.

## The six factors (the data)

- **① Capex ahead of revenue, and the credit channel underneath it.** component guides summing to ≈$710B 2026 big-four
  hyperscaler capex (≈$750B top-five, against reported aggregates of $650–700B) set against
  ~$20–30B incremental AI revenue, which v3 flags as the register's weakest number; ~2–3-yr
  accelerator refresh → write-down risk on a 12–36-month horizon. **New in v3:** Moody's
  ≈$662B of off-balance-sheet lease commitments; JPMorgan's ≈$4.1T AI-debt projection
  (~15% of the corporate-bond universe); **rate-sensitivity as the sharpest lever** (long
  paper against long-payback assets, into a higher-for-longer Fed); and
  **single-counterparty concentration** (Oracle to BBB- on 9 Jul 2026, OpenAI ~half of a
  ≈$638B backlog). Deflation: IG spreads ~74 bps, so the stress is issuer-specific.
- **② Grid is the binding constraint, and the price signal is now capped.** ≈$13.8B
  data-centre-attributed PJM capacity cost across the 26/27 + 27/28 auctions (Monitoring
  Analytics); 28–31% interconnection dropout; transformer lead times 128 wk (LPT) / 144 wk
  (GSU) / 36–48 mo (EHV, to ~60 mo extreme), GOES-constrained. **New in v3:** the 2028/29
  auction cleared at the **$325/MW-day cap** but **6,831 MW short**, so the constraint now
  surfaces as **shortfall volume rather than runaway price**.
- **③ Leading-edge fabrication is one geography.** TSMC ~90% of leading-edge logic; CoWoS
  effectively 100% Taiwan with no second source; Taiwan-bound through ~2028–30. Tools
  reportedly remote-disable, so a Strait disruption is a global compute freeze, not a
  capacity transfer. Unchanged from v2.2.
- **④ Manufactured and licensed single-points-of-failure.** HBM/DRAM shortage to ~2028
  (Nanya, a commodity-DRAM maker, +583% YoY Q1-26, a DRAM-leg read); EUV optics
  sole-sourced via ASML/Zeiss; China ~91% REE refining / ~60% magnet-grade mining, with
  **processing not mining** the bottleneck. **New in v3:** **ASE Technology as a second
  packaging chokepoint** ($8.5B 2026 capex, co-packaged optics, distinct from CoWoS);
  memory **de-cyclicalisation** (3–5-yr contracts, up to 30% prepay); the Oct-2025
  **extraterritorial** ≥0.1% rule, suspended under truce and **reviewed around November
  2026**; and helium (Ras Laffan) folded in.
- **⑤ Commoditisation from below** (promoted to a factor in v3). Kimi K3 at $3/$15 per M
  tokens; frontier token index ~−20% off its May 2026 peak; Chinese industrial policy now
  explicitly behind open weights. Carries the **inverse-risk row** below.
- **⑥ Export-control two-stack, now at model access** (promoted to a factor in v3, and carrying its own falsifier, so every factor is held to §4's discipline). The
  12 Jun 2026 BIS "Is-Informed" letter took two frontier models off the market worldwide,
  the first export control applied to a *model* rather than to the chips that train it; it
  needs no rulemaking and spreads (GPT-5.6 limited days later). Plus the sovereign
  open-weight substitution it provokes, the WAICO / Pax Silica bloc split, the state as
  prospective owner, and **standards as the real rate-limiter** on EU enforcement.

## The inverse-risk row (⑤) — the over-capacity tail

The shape verdict, **"fragile to catastrophe, robust to defection", was tested against the
2026 over-capacity evidence and retained.** The glut is carried as a **named,
trigger-attached tail, not a softening of the base case**: hyperscalers leasing spare
compute (xAI's Colossus 1, and Meta Compute, reported by Bloomberg on 1 July 2026) is read by some
analysts as first evidence of over-capacity, which would flatten the HBM demand curve.
Against that: leasing is the ordinary cloud model, and capital efficiency, burn mitigation,
or demand *strength* all fit the same facts, while memory sits sold out on 3–5-yr prepaid
contracts and PJM cleared 6,831 MW short. **Upgrade trigger:** multiple hyperscalers turning
net sellers · published idle-fleet utilisation · HBM contracts renegotiated down · outright
capex-guidance cuts. **None present at 21 Jul 2026.** If they materialise, the shape does not invert, it
collapses to a single mode of stranded assets and write-downs. The barbell is a bimodal
scenario model for capital allocation, not a claim about a probability distribution.

## Triggers (falsifiable)

Each names a threshold and a check-point so the assessment is scored, not re-argued: first
big-four capex down-revision (Q2 prints, 22–30 Jul 2026); a second IG downgrade on AI
concentration or IG OAS beyond 100 bps; the next PJM auction clearing short again; the
Lloyd's JWC listing the Taiwan Strait or hull war premium beyond 3× the 0.15–0.25%
baseline; the minerals suspension lapsing at its ~Nov 2026 review; SEMI billings turning
negative YoY (Q2-2026 print due early Sep); transformer lead times extending; and the
over-capacity upgrade conditions above. Current readings are in the paper's §4.

## Sources (graded)

- **🟢 Primary / load-bearing:** PJM Base Residual Auction filings + the independent market
  monitor (Monitoring Analytics); Wood Mackenzie transformer survey (Q2 2025, corroborated
  by US DOE); LBNL US data-centre electricity; the IEA "Energy and AI" annex and the IEA 4E
  EDNA projection review; US Bureau of Reclamation 24-Month Study (May 2026); SEMI WWSEMS;
  Lloyd's Market Association Joint War Committee circulars; IEA on rare-earth concentration;
  China MOFCOM notices; EU Commission / EUR-Lex on the AI Act and Digital Omnibus.
- **🟡 Contrast / softer:** Moody's, JPMorgan, Allianz and Citadel readings (analyst);
  Rhodium Group (rare-earth share); hyperscaler capex guidance (company-reported); the
  compute-lease and Chinese-model-restriction items (press-reported, preliminary, and
  flagged as such in the paper).

## Authorship & AI assistance

Author: NM AI Research (ORCID 0009-0003-4213-7769), independent, holds no positions in any
entity named. Produced with AI assistance (Claude Opus 4.8, Anthropic) for data retrieval,
literature search, and drafting; the author set the question, method, and interpretation.
**Conflict of interest:** Anthropic is the maker of the assisting model and appears in the
paper as a subject (the ⑥ model-access controls), as a comparator (⑤ Kimi K3), and as the
lessee whose deals form the evidence base for the ⑤ inverse-risk row. The assisting model is
also a reader of work it helped draft, so its review is not independent. Readings favourable
to Anthropic are non-neutral and primary coverage should be preferred. This is macroeconomic
research and open-science documentation only, not investment advice.

## License

CC BY 4.0 — https://creativecommons.org/licenses/by/4.0/
