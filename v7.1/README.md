# AI Infrastructure: Commitments, Delivery and Access

Purpose: describe the paper, frozen inputs and executable reproduction package.

Version: v7.1. Licence: CC BY 4.0.

This work was produced through an AI-assisted workflow directed by the author.

The paper compares selected commitments, delivery stages and access obligations across the US, EU and UK. Records were assembled through 14 September 2026, with later Irish-process clarifications. This edition adds executable reproduction and corrects residual draft references. Its scientific findings and reporting periods remain those of the documentary v7 edition. No new long experiment or current-source survey is claimed.

Read PAPER_v7_1.pdf or PAPER_v7_1.md. The previous version v7 remains at https://doi.org/10.5281/zenodo.22911245; the concept record is https://doi.org/10.5281/zenodo.20586863.

## Reproduce

Run in your terminal from the extracted bundle:

```bash
python3 -B reproduce.py --check
```

Python standard library only. Tested with Python 3.14.7 on Linux; other runtime versions and operating systems have not been tested. No installation, network access, credentials, GPU or model service is required. The check recomputes all declared outputs in memory and compares their bytes. It does not rewrite the bundle.

To generate files, run in your terminal, choosing a directory that does not already exist:

```bash
python3 -B reproduce.py --output-dir ../ai-infrastructure-reproduced
```

To exercise the reproduction checks, run in your terminal:

```bash
python3 -B test_reproduce.py -v
```

Tests use disposable copies. Existing output directories and destinations inside the bundle are refused.

## Inspect and reuse a finding

To retrieve a quantity with its qualifications, source details and paper locations, run in your terminal:

```bash
python3 -B reproduce.py --explain C021
```

The JSON joins the quantity to its source URL, reporting period, inspection limits and precise locator. Paper locations name the template line, section and passage marker. A source-only input has no paper location. Related arithmetic includes its operands and formula. The field `paper_excerpt` retains author-prepared extraction wording; it is not a certified verbatim quotation from the original source. Do not present it as one. Source URLs are references and are not fetched by this command.

The default check reports input validation, arithmetic, output generation, output parity and package integrity separately. Source truth, interpretation and PDF layout remain `not_assessed`. Package integrity compares the listed files with REPRODUCTION.json. The manifest does not hash itself, and these checks do not authenticate the author or protect against coordinated edits to the manifest and files. They detect disagreement with the supplied manifest. Read the complete report, including checks that were not run; an overall pass applies only to the selected operation.

Commands return JSON on stdout for success and stderr for failure, with exit codes zero and one respectively. Invalid command-line arguments use argparse's usage message and exit code two. Failures include the affected record or file and expected/observed values where available. Generation permits edited inputs and explicitly leaves package integrity unchecked. It does not turn edited values or preserved source wording into new evidence.

To run the worked example, run in your terminal:

```bash
python3 -B reuse_example.py
```

The example retrieves C021, then uses a temporary copy to change a reservation input. It checks that an inconsistent balance is rejected and that a consistent illustrative balance reaches the calculated result and paper. These changed values are illustrative, not a factual update. The original bundle is unchanged and temporary files are removed. To make a real source update, review the original document and amend the period, qualifier, excerpt and context together with the value before any reuse as evidence.

## Inputs and outputs

| File | Purpose |
| --- | --- |
| QUANTITATIVE_INPUTS.json | Frozen manually extracted values, units, periods, qualifiers, source IDs and locators |
| FOLLOWUPS.json | Author-selected editorial follow-up questions |
| PAPER.template.md | Prose with numerical and table substitution points |
| SOURCE_CATALOGUE.json | Original URLs, source identities and inspection limits |
| reproduce.py | Deterministic arithmetic, rendering and byte comparison |
| test_reproduce.py | Disposable positive, negative and changed-input checks |
| reuse_example.py | Runnable evidence lookup and temporary changed-input example |
| PAPER_v7_1.md | Generated numerical expressions and follow-up table within preserved prose |
| QUANTITIES.csv | Generated quantitative ledger, including context and qualifiers |
| FOLLOWUPS.md | Generated editorial table |
| RESULTS.json | Calculated balances and machine-readable coverage limits |
| PAPER_v7_1.pdf | Readable paper, rendered separately; PDF layout is outside the reproduction command |
| REPRODUCTION.json | Machine-readable entrypoints, inputs, outputs and checksums |

The input contains 36 quantity records: 32 inserted into the paper and four source-only calculation inputs. Some records repeat the same underlying observation for a distinct presentation role; they are not 36 independent observations. Dates, ratings, legal identifiers and other prose claims are not exhaustively structured. The quoted excerpts and context retain the extraction record; changing a value requires corresponding human review of those fields, source and period.

The arithmetic checks are GE Vernova's reservation residual (56 + 18 - 10 - 63 = 1 GW) and firm backlog (44 + 2 + 10 - 3 = 53 GW). The first remains unexplained, not labelled cancellation. Both concern Gas Power beyond AI customers. The follow-up table is regenerated from editorial choices; no later event is automatically assessed.

## Verification and limits

The public inputs are exported from the existing reviewed claim/source records, with the GE Vernova locator corrected to source-labelled lines 64 to 67. No fresh source retrieval was needed. Selected extracts, rather than every complete agreement, were inspected. Source URLs and locators allow inspection; raw third-party documents and internal review logs are not part of this bundle.

Generating prose from a template is not independent verification of that prose. A successful check establishes the declared arithmetic and output parity, not causal validity, source truth, current regulatory status or model performance. No bank reconciliation, site inspection, customer acceptance audit or matched project-finance baseline was run. The historical supply-constraints script and dataset remain separate.

The new code, exported inputs and method wording received a separate read-only Gemini review. The recorded tests were executed by OpenAI GPT-6; no independent execution is claimed. Author publication approval remains separate.

## AI assistance, conflicts and limitations

The research design, method, sourcing decisions and analytical judgements are the author's. OpenAI GPT-6 prepared the integrated manuscript, source catalogue and reproduction package through an AI-assisted process; the text was artificially generated. Claude and Gemini contributed earlier source work, drafting and challenges. A separate Gemini review examined the complete dated manuscript and its held source evidence; that review is distinct from the author's release decision. Gemini's earlier contributions limit its independence from related work. A separate Gemini run reviewed the reproduction addition without independently executing its tests. The earlier manuscript review alone does not constitute acceptance of that addition. Separate review does not establish complete validation. The assisting models are not always neutral parties to the subject matter. OpenAI is a named infrastructure counterparty and appears in the political discussion. Anthropic's leadership is discussed, and Google competes with several subjects.

The source catalogue and Verification note identify the documents, inspected locations and evidence limits. They do not certify every underlying company statement or a complete causal account. No matched project-finance baseline, complete historical replay, bank reconciliation, site inspection or customer acceptance audit is claimed.

Guarantee: within the scope stated in the Verification note, reproduce.py recalculates the named balances and regenerates selected numerical expressions and the follow-up table from frozen inputs. It checks output parity, not source truth or causal validity. A reader can check this without trusting either party.

What the author cannot guarantee: errors or omissions can survive model review, including confident but incorrect review findings. The author does not claim the review is exhaustive. Corrections are logged against the DOI when surfaced. No warranty is offered beyond the terms of the CC BY 4.0 licence.
