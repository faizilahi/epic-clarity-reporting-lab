# Night Extract: Clarity ORU and ADT Spill Into the Reporting Mart

Faiz Elahi - https://www.linkedin.com/in/faizilahi - https://pendataco.com - https://github.com/faizilahi

Portfolio project. Synthetic Clarity-shaped tables only - not an Epic customer engagement and not a claim that Faiz worked inside a health system.

This is the story of one overnight extract for an inpatient census + result feed used by care-management reporting. The Python service under `src/` is a production-shaped runner (config, extract windows, load, reconcile), not a notebook.

## PATIENT@CLARITY - who walked in after midnight

`PATIENT` is the person spine for the extract. The night job pulls every patient with an open encounter or a result filed since the prior watermark. Grain is one row per `PAT_ID`. The service rejects ORUs rows whose `PAT_ID` is absent here - that is the first join failure we page on.

## PAT_ENC - encounters that own the night

`PAT_ENC` carries `PAT_ENC_CSN_ID`, admit/discharge timestamps, hospital account, and acuity. The extract window is **encounter-touch**: any encounter with `HOSP_ADMSN_TIME` in window *or* still open (`HOSP_DISCH_TIME` null) at watermark. Closed encounters with no new results are skipped unless they appear on the ADT delta.

## ORDER_PROC / ORDER_RESULTS - labs that arrived late

Results filed between watermarks land in `ORDER_RESULTS` keyed by `ORDER_PROC_ID` -> `PAT_ENC_CSN_ID`. The runner flattens LOINC + numeric value into `mart.fact_result_nightly`. Nested components (SYS/DIA) become two fact rows sharing `ORDER_PROC_ID`.

## CLARITY_ADT - the pipe that explains the census swing

ADT A01/A02/A03 events are the reason the census board moved between 01:00 and 05:00. We keep raw event type, effective time, and prior/next point of care. Transfers (A02) do not create a new encounter; they update location on the open CSN.

## How the service runs

```bash
pip install -r requirements.txt
python scripts/generate_clarity_slice.py
python scripts/run_night_extract.py
pytest -q
```

Concrete printout includes row counts per Clarity table, rejected orphans, and the census delta for the synthetic night of 2024-11-12.

Rows under `data/` are synthetic and sized for git.

---

Faiz Elahi - [LinkedIn](https://www.linkedin.com/in/faizilahi) - [pendataco.com](https://pendataco.com) - [GitHub](https://github.com/faizilahi)

