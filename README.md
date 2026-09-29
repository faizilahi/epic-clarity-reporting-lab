# Epic Clarity Reporting Lab (Teaching Approximations, Synthetic)

**Author:** Faiz Elahi · **Type:** EDUCATIONAL PORTFOLIO LAB · **SYNTHETIC DATA ONLY**

---

## Educational disclaimer / synthetic data

This lab uses **entirely synthetic** patients, encounters, departments, and orders. Table and column names **resemble Clarity-style reporting patterns** for learning—they are **not** Epic documentation, not a licensed Clarity extract, and not real hospital PHI.

Use honest language: *“I practiced operational SQL on synthetic Clarity-like CSVs with DuckDB.”*

---

## Problem statement (detailed)

Hospital operational analytics teams answer recurring questions from relational reporting schemas:

- **ALOS:** What is average (and median) length of stay by inpatient unit?
- **Volume:** How do encounter counts trend by month and encounter type (inpatient, emergency, ambulatory)?
- **Procedure mix:** Which procedure codes appear most often on orders?

You cannot ship real Clarity schemas in a public portfolio. This lab gives you **approximate naming** (`PAT_ENC`, `CLARITY_DEP`, `ORDER_PROC`, `PATIENT`) on generated CSVs plus **DuckDB SQL** that mirrors how BI developers think in production—without implying Epic employment or access.

The generator builds ~800 patients, ~3,200 encounters, and ~4,500 orders with realistic encounter-type weights and inpatient LOS on Med-Surg and ICU departments.

---

## Why this tool

| Ad hoc Excel | This lab pipeline |
|--------------|-------------------|
| Hidden join grain | Explicit encounter and order grain in CSV dictionary |
| One-off SQL | Reusable `reporting.py` functions |
| No audit trail | Version-controlled scripts + `output/` CSV exports |

Pairs naturally with **`caboodle-edw-star-schema-lab`** (EDW thinking) and **`dbt-healthcare-marts-lab`** (mart layer on top of extracts).

---

## Architecture

```mermaid
flowchart LR
  GEN[generate_synthetic_data.py]
  CSV[data/*.csv]
  RUN[run_reports.py]
  SQL[reporting.py DuckDB]
  OUT[output/*.csv]
  CHART[generate_charts.py]
  GEN --> CSV --> RUN --> SQL --> OUT
  OUT --> CHART
```

See [`docs/architecture.md`](docs/architecture.md).

---

## Dataset dictionary (tables / columns)

| File | Grain | Key columns | Notes |
|------|-------|-------------|-------|
| `patient.csv` | Patient | `PAT_ID`, `PAT_NAME`, `SEX`, `BIRTH_DATE` | Synthetic dimension |
| `pat_enc.csv` | Encounter | `PAT_ENC_CSN_ID`, `PAT_ID`, `DEPARTMENT_ID`, `CONTACT_DATE`, `ENC_TYPE`, `LENGTH_OF_STAY_DAYS` | LOS populated for inpatient only |
| `clarity_dep.csv` | Department | `DEPARTMENT_ID`, `DEPARTMENT_NAME`, `SERVICE_AREA` | Med-Surg, ICU, ED, clinics |
| `order_proc.csv` | Order | `ORDER_ID`, `PAT_ENC_CSN_ID`, `PROC_CODE`, `PROC_NAME`, `ORDER_STATUS` | Includes canceled rows for teaching |
| `output/alos_by_department.csv` | Report | `DEPARTMENT_NAME`, `avg_los_days`, `median_los_days` | Inpatient ALOS |
| `output/encounter_volume_by_month.csv` | Report | `month`, `ENC_TYPE`, `encounter_count` | Monthly volume |
| `output/top_procedures.csv` | Report | `PROC_CODE`, `order_count` | Top procedures by volume |

---

## Prerequisites

- Python 3.10+
- Packages in `requirements.txt`: `pandas`, `duckdb`, `matplotlib`

---

## Step-by-step: how to run

### Windows PowerShell

```powershell
cd epic-clarity-reporting-lab
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python scripts/generate_synthetic_data.py
python src/run_reports.py
python scripts/generate_charts.py
```

### Optional bash

```bash
cd epic-clarity-reporting-lab
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python scripts/generate_synthetic_data.py
python src/run_reports.py
python scripts/generate_charts.py
```

---

## File-by-file walkthrough

| Path | Role |
|------|------|
| `scripts/generate_synthetic_data.py` | Builds `data/*.csv` with weighted encounter types and order catalog |
| `src/paths.py` | `DATA_DIR` and `OUTPUT_DIR` constants |
| `src/reporting.py` | Registers CSV views in DuckDB; ALOS, volume, top procedures SQL |
| `src/run_reports.py` | Runs reports and writes `output/*.csv` |
| `scripts/generate_charts.py` | ALOS bar chart and ambulatory volume trend under `docs/images/` |
| `docs/architecture.md` | Diagram notes and teaching context |

---

## Expected outputs and how to interpret them

- **`output/alos_by_department.csv`** — Averages **inpatient** rows with non-null `LENGTH_OF_STAY_DAYS`; compare mean vs median for skew.
- **`output/encounter_volume_by_month.csv`** — Counts by `ENC_TYPE`; synthetic dates are uniform—not seasonal epidemiology.
- **`output/top_procedures.csv`** — Ranked `PROC_CODE` counts; canceled orders are **included** unless you filter in an exercise.
- **Charts in `docs/images/`** — Visual sanity check for classroom discussion.

---

## Results interpretation

- **ALOS** here is a SQL average on synthetic inpatient stays—production teams add exclusion rules (transfers, observation, leave of absence).
- **Ambulatory vs ED vs inpatient** must stay separated; mixing types invalidates LOS metrics.
- **Order volume ≠ completed procedures**; status fields matter for revenue-cycle vs clinical ops views.

---

## Glossary (8+ terms)

1. **Clarity** — Epic’s SQL reporting database concept (not replicated in this repo).
2. **ALOS** — Average length of stay in days for inpatient encounters.
3. **CSN** — Contact serial number pattern for encounter identifiers.
4. **Encounter grain** — One row per patient visit episode in `pat_enc.csv`.
5. **DuckDB** — In-process analytical SQL engine used as a Clarity query stand-in.
6. **SERVICE_AREA** — Department grouping (Inpatient, Emergency, Ambulatory).
7. **PROC_CODE** — Procedure/CPT-style code on orders (synthetic catalog).
8. **ORDER_STATUS** — Lifecycle state (e.g., Completed, Canceled).
9. **Teaching approximation** — Naming inspired by industry patterns, not vendor copy.

---

## Common mistakes (5+)

1. Including **emergency or ambulatory** rows in ALOS denominators.
2. Assuming **column names match** your employer’s licensed Clarity model one-to-one.
3. Joining **orders to patients** without encounter keys when grain requires `PAT_ENC_CSN_ID`.
4. Ignoring **canceled orders** when ranking “top procedures” for clinical utilization.
5. Treating **synthetic monthly volume** as proof of seasonality modeling skill.
6. Claiming **Epic certification or production Clarity access** from this portfolio lab.

---

## Exercises (5+)

1. Exclude `ORDER_STATUS = 'Canceled'` from procedure rankings and compare top 5 lists.
2. Add **ED length-of-stay proxy** columns in the generator using arrival/discharge timestamps.
3. Parameterize reports for **fiscal year** vs calendar year in SQL.
4. Write plain-English definitions for each report query for a clinical ops stakeholder.
5. Export a **single combined dashboard CSV** joining department names to monthly volumes.
6. Cross-read with **`hl7-fhir-interop-lab`** — contrast relational extracts vs FHIR resources.

---

## Limitations / simulation vs production

- No Epic SDK, Caboodle, Chronicles, or real facility identifiers.
- CSV extracts only—no incremental Clarity refresh or security/RLS.
- Synthetic distributions are **plausible for teaching**, not benchmarked to any health system.
- Educational code—**no production SLA or compliance attestation**.

---

## Related labs

- [`caboodle-edw-star-schema-lab`](../caboodle-edw-star-schema-lab/) — EDW star schema patterns.
- [`dbt-healthcare-marts-lab`](../dbt-healthcare-marts-lab/) — Mart layer and tests.
- [`hedis-quality-measures-lab`](../hedis-quality-measures-lab/) — Quality measure numerators/denominators from claims.

---

**Author:** Faiz Elahi · Educational portfolio use.
