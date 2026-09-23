# AI Infrastructure: Commitments, Delivery and Access

Purpose: route readers to the current paper and its executable evidence bundle.

**Version:** v7.1. [Concept DOI](https://doi.org/10.5281/zenodo.20586863).

This work was produced through an AI-assisted workflow directed by the author.

The paper examines selected disclosed commitments, delivery stages and access obligations across the US, EU and UK. It uses dated records assembled through 14 September 2026, with later Irish-process clarifications. It does not establish an industry-wide causal relay, a regional performance ranking or unusual risk relative to matched conventional project finance. No matched baseline was run.

Read [the main paper](v7.1/PAPER_v7_1.pdf), or its [Markdown text](v7.1/PAPER_v7_1.md). The [source catalogue](v7.1/SOURCE_CATALOGUE.json) records original URLs, reporting periods, inspected locations and source limits. Most commercial sources are interested company disclosures. Political coverage is expressly attributed, including original statements not retrieved.

## Reproduction and reuse

The [v7.1 bundle](v7.1/README.md) contains frozen quantitative inputs, source references and executable checks for the named calculations and tables. It provides an evidence lookup, separate arithmetic and file-integrity results, and a disposable worked example. Selected numerical expressions are regenerated within supplied prose. Source truth and interpretation remain human assessments; this is not a replay of the full research process.

Run in your terminal from this repository:

```bash
python3 -B v7.1/reproduce.py --check
```

To inspect a quantity with its qualifiers and source details, run in your terminal:

```bash
python3 -B v7.1/reproduce.py --explain C021
```

For the temporary changed-input example, run in your terminal:

```bash
python3 -B v7.1/reuse_example.py
```

The commands require only Python's standard library. They do not use a model, credentials or network access. The [bundle guide](v7.1/README.md) defines the check results and exclusions. The [previous documentary v7](v7/README.md) and the [historical edition](https://doi.org/10.5281/zenodo.22015680) remain available.

## Verification

The source catalogue preserves issuing documents and inspected locations for the paper's disclosed amounts, contract terms, dates and attributed statements. Selected extracts were inspected; not every full agreement was read. Source availability is distinct from semantic support. No bank reconciliation, site inspection, customer acceptance audit, current regulatory determination or matched project-finance baseline is claimed.

## AI assistance, conflicts and limitations

The research design, method, sourcing decisions and analytical judgements are the author's. OpenAI GPT-6 prepared the integrated manuscript, source catalogue and reproduction package through an AI-assisted process; the text was artificially generated. Claude and Gemini contributed earlier source work, drafting and challenges. A separate Gemini review examined the complete dated manuscript and its held source evidence; that review is distinct from the author's release decision. Gemini's earlier contributions limit its independence from related work. A separate Gemini run reviewed the reproduction addition without independently executing its tests. The earlier manuscript review alone does not constitute acceptance of that addition. Separate review does not establish complete validation. The assisting models are not always neutral parties to the subject matter. OpenAI is a named infrastructure counterparty and appears in the political discussion. Anthropic's leadership is discussed, and Google competes with several subjects.

The source catalogue and Verification note identify the documents, inspected locations and evidence limits. They do not certify every underlying company statement or a complete causal account. No matched project-finance baseline, complete historical replay, bank reconciliation, site inspection or customer acceptance audit is claimed.

Guarantee: within the scope stated in the Verification note, reproduce.py recalculates the named balances and regenerates selected numerical expressions and the follow-up table from frozen inputs. It checks output parity, not source truth or causal validity. A reader can check this without trusting either party.

What the author cannot guarantee: errors or omissions can survive model review, including confident but incorrect review findings. The author does not claim the review is exhaustive. Corrections are logged against the DOI when surfaced. No warranty is offered beyond the terms of the CC BY 4.0 licence.

## Historical files

The root `supply_constraints.csv` and `reproduce.py` belong to historical v6. They do not regenerate v7 or v7.1. Use `v7.1/reproduce.py` for the current bundle. The historical README and all earlier edition files remain available.
