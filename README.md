# The AI Constraint Relay, reproduction bundle (v5)

*AI disclosure: the research is the author's; this text was drafted with AI assistance and reviewed by the author. The models, and the conflicts they create, are named in the Conflict of interest and scope section.*

A supply-side assessment of the AI compute build-out. **Method-first, not a crash call.**
Most AI-infrastructure commentary argues over *demand* (can revenue justify the capex);
this takes the *supply* side, meaning the physical, material, and geographic limits on
building and running the compute, and tracks how those limits displace across the stack.

> **Version history.** Concept DOI 10.5281/zenodo.20586863 (resolves to the current version).
>
> **v5 updates (16 August 2026).**
> - *Lake Powell & USBR Trace Correction:* Corrected study attribution and scenario elevations. Documented the vintage mismatch across Reclamation 24-Month traces (Min Probable July 2026, Max May 2026; canonical August file remains August 2025). The 3,490 ft minimum power pool breach remains deferred past 2026, with the July 2026 Probable Minimum trace projecting 3,503.65 ft at year-end (≈13.7 ft clearance, with 36 per cent unregulated inflows and 6.00 maf releases). Dropped the unanchored 3,504 ft threshold.
>
> **v4 updates (16 August 2026).** 
> - *Retitled & Reframed to The Constraint Relay:* Replaces the static 'barbell' metaphor with the empirical finding of continuous hydraulic displacement across grid rationing, prime movers, non-tradable labour, and incidence re-routing.
> - *Tape Re-anchoring & Financing Mechanics (①):* 14 August 2026 close readings incorporated across equities (Meta $589.85, Oracle $150.52, Micron $971.66) and credit (IG OAS 80 bps, HY OAS 2.82%). Notes the tape inversion where Oracle rose on backlog while Meta fell on capex. Added single-campus reinsurance accumulation limits ($15B to $40B+ TIV) as a physical cap on syndicated debt.
> - *Energy Baseline & Non-Tradable Labour (②):* STEO 11 August path shifts fuel shocks to baseline friction ($86.81/bbl 2026 average). Added journeyman electrician/lineman training ceilings (BLS/RAPIDS 4 to 5-yr pipeline); turbine manufacturing backlogs (GE Vernova/Siemens) and superalloy castings (Howmet) closing the on-site bypass; switchgear/HVDC lead times; water basin siting moratoria; and nuclear licensing/HALEU enrichment constraints.
> - *Upstream Materials & Chemical Chokepoints (③ & ④):* Added ABF substrate packaging concentration (Ibiden/Shinko); Japan METI EUV photoresist monopolies; Spruce Pine high-purity quartz crucible single-point-of-failure (USGS); ATE memory test slot scaling (Advantest/Teradyne); and 1.6T InP optical lasers.
> - *Memory Incidence Inversion (④):* Documents HBM wafer reallocation shifting price spikes to commodity DRAM (+54% to +116%) and consumer electronics rather than AI buyers. Verified via trade-press consensus estimates in the Verification note.
> - *Coupled Financing & Inverse Glut Tail (⑤):* Records Anthropic Series H strategic equity integration with memory makers. Documents the Micron paradox (sold-out datacenter books vs -22.6% equity drop and -14% smartphone shipments).
> - *Capex Guidance & Regulatory Rationing (① & ②):* Updates Q2 hyperscaler capex guides ($720 to $745B combined) and PJM post-auction FERC filings ($20B procurement, 50 MW BYOP rules).

## On method (the honest split)

The constraints in the paper's §2 are verifiable, sourced, dated numbers, and they carry
the argument. The "constraint relay" reading in §3 is *interpretation of* those numbers and is labelled
as such. No likelihood/severity scores are asserted: assigning 1 to 5 ratings would dress
judgement as measurement. Thresholds in the checkpoints table are the **author's**, chosen to
be checkable rather than derived from a source.

For this edition the event-driven and structural claims were checked against their issuing
sources as part of the companion PESTLE scan (concept DOI 10.5281/zenodo.20680575) and updated
through 16 August 2026. Market-live readings are 14 August 2026 market-close readings (with
21 July 2026 comparators noted) and will move. Where two sources give different values for the
same quantity, both are shown rather than averaged.

## Contents

| File | What it is |
|---|---|
| `constraint_relay_v5.md` | The paper (Markdown source, the thing you edit). |
| `The AI Constraint Relay v5.pdf` | The paper (readable PDF). |
| `reproduce.py` | Tabulates and cites every figure from the CSV. Standard library only. |
| `supply_constraints.csv` | Every metric with its value, source, and vintage (the data layer). |
| `README.md` | This file. |

*Rendering:* `bash "House style/render_pdf.sh" constraint_relay_v5.md "The AI Constraint Relay v5.pdf"`
(markdown → house-style HTML → headless print to PDF, in one command).

## Reproduce

```bash
python3 reproduce.py
```

`reproduce.py` is honest about what it is: this is a **register, not a calculation**. The
script reads `supply_constraints.csv` and prints each metric with its source and vintage,
then the interpretive relay reading and conclusion. Edit the CSV and re-run to
reproduce every figure.

## The six factors (the data)

- **① Capex ahead of revenue, and the credit channel underneath it.** Component guides summing to
  ≈$720 to $745B 2026 big-four hyperscaler capex (Alphabet $195 to $205B, Amazon ≈$220B, Meta $130 to $145B,
  Microsoft $175B stated post asset-life extension); reported aggregates track $670 to $710B. Accelerators
  carry a ≈2 to 3-yr refresh clock → write-down risk on a 12 to 36-month horizon. Capex increases decompose
  into component price pass-through (Amazon and Microsoft) as well as capacity. Moody's ≈$662B of
  off-balance-sheet leases; JPMorgan's ≈$4.1T AI-debt projection; rate-sensitivity under the Warsh Fed
  (3.50 to 3.75% held 29 July 2026, 3.8% median); single-campus property reinsurance limits ($15B to $40B+ TIV);
  and single-counterparty concentration (Oracle to BBB-). Market tape on 14 August 2026 shows Meta down 8.4%
  since 21 July, while Oracle rebounded 18.5%.
- **② Grid is the binding constraint, and the price signal is now capped.** ≈$13.8B data-centre-attributed
  PJM capacity cost across the 26/27 + 27/28 auctions; 28 to 31% interconnection dropout; transformer lead
  times 128 wk (LPT) / 144 wk (GSU) / 36 to 48 mo (EHV); substation switchgear and HVDC cables (3 to 5 yrs).
  2028/29 auction cleared at the **$325/MW-day cap** but **6,831 MW short**. PJM post-auction FERC filings
  (31 July $20B procurement, 7 August 50 MW BYOP rules) expand the grid bottleneck into active regulatory rationing.
  Skilled high-voltage labour non-tradability (BLS SOC 47-2111 / 49-9051, 4 to 5-yr apprenticeships); prime mover
  backlogs (GE Vernova, Siemens Energy) and superalloy blade castings (Howmet) close the on-site generation bypass.
  Water siting moratoria (USBR / ADWR) and nuclear baseload / HALEU enrichment constraints (Centrus Energy, NRC).
  EIA STEO Brent path ($87 2026 average, $85 Q3, $78 Q4, $69 2027) shifts energy cost to 2026 baseline operating friction.
  Lake Powell minimum power pool breach deferred past 2026 (July 2026 Min Probable 3,503.65 ft, ≈13.7 ft clearance; 36% unregulated inflows).
- **③ Leading-edge fabrication is one geography.** TSMC ≈90% of leading-edge logic; CoWoS effectively
  100% Taiwan with no second source; Taiwan-bound through ≈2028 to 2030. Tools reportedly remote-disable, so a
  Strait disruption is a global compute freeze, not a capacity transfer. ABF substrate concentration in Japan/Taiwan
  (Ibiden, Shinko); Japan METI EUV photoresist monopolies (Tokyo Ohka Kogyo, JSR, Shin-Etsu); and Spruce Pine
  high-purity quartz crucible single-point-of-failure (USGS).
- **④ Manufactured and licensed single-points-of-failure.** Memory shortage to ≈2028. **Memory price
  incidence inverts:** HBM takes 23% of DRAM wafers at a 3:1 penalty, with HBM ASP rising moderately
  (+1% to +22%) while traditional DRAM bit revenue surges (+54% to +116%), transferring inflation to consumer
  device buyers (trade-press estimates). **Chokepoints and frontier demand couple:** Anthropic Series H brings Micron,
  Samsung, SK Hynix as strategic partners. ATE memory test slot scaling (Advantest, Teradyne); 1.6T InP optical lasers
  (Coherent, Lumentum); ASE Technology ($8.5B capex) as second packaging node; EUV optics sole-sourced via ASML/Zeiss;
  China refines most REEs with truce review ≈Nov 2026; helium buffer.
- **⑤ Commoditisation from below.** Kimi K3 at $3/$15 per M tokens; frontier token index ≈-20% off May 2026
  peak; Chinese industrial policy behind open weights. Carries the **inverse-risk row & Micron paradox**:
  Micron sold out through 2027 but stock closed $971.66 on 14 August (-22.6% from peak); Samsung -33%; SK Hynix -15%;
  IDC smartphone shipments -14%. Shortage order books and equity demand destruction co-exist in the same company.
- **⑥ Export-control two-stack, now at model access.** June 2026 BIS Is-Informed letter took two frontier
  models off the market worldwide, spurring sovereign open-weight procurement across EU, Gulf, and Japan.
  Hardware controls continue (H200 stalled). WAICO (29 states) vs Pax Silica (35 states) bloc split.
  EU AI Act GPAI enforcement active from 2 Aug 2026, with Annex III gated on CEN-CENELEC standards.

## The inverse-risk row (⑤): the over-capacity tail

The premise that compute deployment is governed by physical ceilings rather than speculative glut was tested against the 2026 over-capacity
evidence and retained. The glut is carried as a **named, trigger-attached tail, not a softening of the base case**:
hyperscalers leasing spare compute is read by some analysts as first evidence of over-capacity.
Against that: leasing is the ordinary cloud model, and memory sits sold out through 2027 on 3 to 5-yr prepaid
contracts while PJM cleared 6,831 MW short. **Upgrade trigger:** multiple hyperscalers turning net sellers ·
published idle-fleet utilisation · HBM contracts renegotiated down · outright capex-guidance cuts. **None present
at 15 Aug 2026.**

## Relocation checkpoints (falsifiable)

Each names a threshold and a check-point so the assessment is scored, not re-argued: hyperscaler capex
conviction (recalibrated to 26 Aug Nvidia gap); financing strain (Oracle BBB-, IG OAS 80 bps, HY OAS 2.82%); grid volume
shortfall (6,831 MW short); skilled electrical labour wage growth; prime mover turbine and casting lead times;
nuclear and SMR HALEU licensing milestones; water basin siting moratoria; Taiwan Strait war-risk (not listed under JWLA-032/033);
chemical resists and high-purity quartz crucible lead times; minerals suspension review (≈Nov 2026); SEMI billings (+14% YoY)
and ATE test slot capacity; transformer and switchgear lead times (128/144 wk); model-access controls; and
over-capacity upgrade conditions. Current readings are in §4.

## Verification note

Every measured figure in this register is traced to an official primary document or regulatory filing: PJM Base Residual Auction filings and Monitoring Analytics market reports; US Energy Information Administration Short-Term Energy Outlook data tables (11 August 2026); US Bureau of Reclamation 24-Month Studies (May 2026 Max and July 2026 Min Probable traces); US Bureau of Labor Statistics Occupational Employment and Wage Statistics (SOC 47-2111, SOC 49-9051) and US Department of Labor Registered Apprenticeship data; US Geological Survey Mineral Commodity Summaries (Silica/Industrial Sand); Japan METI Current Survey of Production; US Nuclear Regulatory Commission dockets; Wood Mackenzie transformer lead-time surveys corroborated by the US Department of Energy (Q2 2025); SEMI Worldwide Semiconductor Equipment Market Statistics (Q1 2026); Lloyd's Market Association Joint War Committee circulars (JWLA-032/033); China MOFCOM trade notices; SEC Form 10-Q, Form 10-K, and earnings disclosures from Alphabet, Amazon, Meta, Microsoft, Micron, Samsung, SK Hynix, TSMC, GE Vernova, Howmet Aerospace, Centrus Energy, Advantest, Teradyne, Ibiden, and Tokyo Ohka Kogyo; Federal Reserve FOMC statements (29 July 2026); Nasdaq official historical market-close data (14 August 2026); and ICE BofA credit spread indices via FRED (14 August 2026).

Modelled or estimated inputs are identified as estimates rather than empirical measurements: memory supplier ASP growth and commodity bit revenue figures are consensus estimates from trade-press and industry trackers (TrendForce, DigiTimes, Counterpoint Research); industry incremental AI revenue figures are analyst estimates; token price indices are proxy readings (Citadel); datacentre electricity scenario projections are sourced from Lawrence Berkeley National Laboratory and the IEA; and off-balance-sheet lease aggregates are sourced from Moody's credit research.

## Conflict of interest and scope

The research design, method, sourcing decisions and analytical judgements are the author's. Anthropic Opus 5.0 and Google DeepMind Gemini 3.7 assisted with data retrieval, calculation, literature search and drafting, so this text was artificially generated and was reviewed by the author before publication.

The assisting models are not always a neutral party to the subject matter, and each creates a distinct, directed conflict:

- **Anthropic**, whose Claude Opus 5.0 model assisted with drafting: the paper carries a dedicated analysis of Anthropic's Series H round ($65B, $965B post-money) with memory chokepoint suppliers (④), and it cites demand from compute-constrained labs, naming Anthropic, to argue against the over-capacity glut tail (⑤). An Anthropic model is drafting text in which Anthropic's own demand is presented as evidence for the paper's thesis, creating a potential bias toward understating over-capacity risk.
- **Alphabet**, whose Gemini 3.7 model assisted with fact-checking and retrieval: Alphabet is a named subject in the capital-expenditure factor (①), the paper cites Google's reported per-query energy figure (0.24 Wh) to revise a widely cited figure downward (②), and it names Google's internal TPU silicon as a substitution channel against merchant hardware (①). A Google model is reporting figures published by Google that are favourable to Google.

Guarantee: every measured claim is traced to the primary document named in the Verification note, and reproduce.py regenerates every table from supply_constraints.csv. Modelled or estimated inputs are identified as such in the Verification note rather than presented as measurements. A reader can check this without trusting either party.

What the author cannot guarantee: a language model's output can be wrong in ways that survive review. In prose the error is locally plausible and consistent in tone with what surrounds it; in code it simply runs, and a wrong constant or a mis-set filter still returns a clean number. Several methods have been deployed to mitigate this, including explicit instructions, internal red-teaming and cross-lab blindspot checks, but the author does not claim the review is exhaustive. Corrections are logged against the DOI when surfaced.

No warranty is offered beyond the terms of the CC BY 4.0 licence. Independent analysis and open-science documentation only, not investment advice.
