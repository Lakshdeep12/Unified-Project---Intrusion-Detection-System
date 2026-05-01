# Model Results

This project uses a hybrid intrusion detection approach:

- Supervised model: Random Forest
- Unsupervised model: Isolation Forest
- Default model set: `Set-1`
- Dataset family: CICIDS2017 and UNSW-NB15

## Reproducible Evaluation Snapshot

Command used:

```powershell
.\.venv\Scripts\python.exe Scripts\evaluate_sample.py --model-key Set-1 --sample-size 5000
```

Evaluation data:

- Source file: `DataSet/Raw DataSet/CICD2017/Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv`
- Sampling: 5,000 BENIGN rows and 5,000 DDoS rows
- Total rows: 10,000
- Random seed: 42

Results:

| Metric | Score |
| --- | ---: |
| Accuracy | 0.9238 |
| Precision | 1.0000 |
| Recall | 0.8476 |
| F1-score | 0.9175 |

Confusion matrix:

| Actual / Predicted | Normal | Attack |
| --- | ---: | ---: |
| Normal | 5000 | 0 |
| Attack | 762 | 4238 |

## Broader CICIDS2017 Benchmark

Command used:

```powershell
.\.venv\Scripts\python.exe Scripts\evaluate_sample.py --all-cicids --model-key Set-1 --sample-size 1000
```

This evaluates every CICIDS2017 CSV that contains both normal and attack rows. Each evaluated file is sampled as 1,000 normal rows and 1,000 attack rows where enough rows exist.

| Dataset | Rows | Accuracy | Precision | Recall | F1-score |
| --- | ---: | ---: | ---: | ---: | ---: |
| Friday Afternoon DDoS | 2,000 | 0.9285 | 1.0000 | 0.8570 | 0.9230 |
| Friday Afternoon PortScan | 2,000 | 0.5000 | 0.0000 | 0.0000 | 0.0000 |
| Friday Morning | 2,000 | 0.5000 | 0.0000 | 0.0000 | 0.0000 |
| Thursday Afternoon Infiltration | 72 | 0.5000 | 0.0000 | 0.0000 | 0.0000 |
| Thursday Morning WebAttacks | 2,000 | 0.4995 | 0.0000 | 0.0000 | 0.0000 |
| Tuesday WorkingHours | 2,000 | 0.5000 | 0.0000 | 0.0000 | 0.0000 |
| Wednesday WorkingHours | 2,000 | 0.6765 | 0.9862 | 0.3580 | 0.5253 |

Macro average across evaluated files:

| Metric | Score |
| --- | ---: |
| Accuracy | 0.5864 |
| Precision | 0.2837 |
| Recall | 0.1736 |
| F1-score | 0.2069 |

`Monday-WorkingHours` is skipped because the sample does not contain both normal and attack classes.

## Interpretation

The default `Set-1` model is strong on the DDoS file but does not generalize well across all attack categories. This is useful for evaluation because it shows an honest limitation and motivates the included multiple model sets, threshold tuning, and broader retraining as future work.

## Suggested Viva Points

- Random Forest gives strong known-attack classification.
- Isolation Forest adds anomaly detection for suspicious unseen traffic.
- The dashboard connects model output to alerts, logs, and live statistics.
- The current limitation is cross-category generalization: future work can select the best model set per attack family, tune thresholds, retrain with class balancing, and add a combined multi-class benchmark.
