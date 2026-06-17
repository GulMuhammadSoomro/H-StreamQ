# H-StreamQ: Adaptive Kafka-Based Pipeline for Healthcare Data Quality Monitoring

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)
[![Kafka 3.x](https://img.shields.io/badge/Kafka-3.x-orange.svg)](https://kafka.apache.org/)

**H-StreamQ** is a proof-of-concept adaptive pipeline for streaming-oriented healthcare data quality monitoring built on Apache Kafka. It ingests streaming clinical data, detects missing values, outliers, and duplicates, applies correction strategies, and computes a composite Data Quality Score (DQS).

> **Paper:** Soomro GM, Amur ZH, Krayem S, Chramcov B, Jasek R, Allahwerdi I. H-StreamQ: A Proof-of-Concept Kafka-Based Pipeline for Adaptive Data Quality Monitoring in Healthcare Streaming Environments. *SoftwareX* (under review).

---

## Quick Start

### 1. Prerequisites

- Python 3.9+
- Apache Kafka 3.x (standalone, no Docker required)
- Java 11+ (required by Kafka)
- Kafdrop 3.x (optional, for topic monitoring UI)
- Credentialed MIMIC-IV access via [PhysioNet](https://physionet.org/content/mimiciv/)

### 2. Clone and install

```bash
git clone https://github.com/GulMuhammadSoomro/H-StreamQ.git
cd H-StreamQ
conda create -n hstreamq python=3.9
conda activate hstreamq
pip install -r requirements.txt
```

### 3. Start Kafka

```bash
# Download Kafka 3.x from https://kafka.apache.org/downloads
# Extract and navigate to the Kafka directory

# Start Zookeeper
bin/zookeeper-server-start.sh config/zookeeper.properties

# Start Kafka broker (in a new terminal)
bin/kafka-server-start.sh config/server.properties

# Create topics (in a new terminal)
bin/kafka-topics.sh --create --topic hstreamq-input --bootstrap-server localhost:9093 --partitions 1 --replication-factor 1
bin/kafka-topics.sh --create --topic hstreamq-output --bootstrap-server localhost:9093 --partitions 1 --replication-factor 1
```

### 4. Generate the MIMIC-IV demonstration subset

> You must have completed PhysioNet credentialing and downloaded MIMIC-IV v3.1 labevents.csv locally.

```bash
python generate_demo_subset.py --input /path/to/your/labevents.csv --output data/demo_subset.csv
```

This script uses seed 42 and selects records from 10 fixed hospital admissions (hadm_id values listed in `hadm_ids.txt`), producing a reproducible 1,996-row subset. The demonstration uses 200 records sampled from this subset.

### 5. Run the demonstration

```bash
jupyter notebook H_StreamQ_Pipeline.ipynb
```

Run all cells in order. The notebook:
1. Publishes 200 records to `hstreamq-input` in 20 batches of 10
2. Processes each batch through the 7-component quality pipeline
3. Publishes corrected records and DQS scores to `hstreamq-output`
4. Generates Table 4 and Figure 2 from the paper

---

## Repository Structure

```
H-StreamQ/
├── H_StreamQ_Pipeline.ipynb      # Main demonstration notebook
├── generate_demo_subset.py        # MIMIC-IV subset generation script
├── requirements.txt               # Python dependencies (pinned versions)
├── environment.yml                # Conda environment specification
├── config/
│   └── hadm_ids.txt               # Fixed hospital admission IDs for reproducibility
├── data/
│   └── .gitkeep                   # Placeholder — user populates with MIMIC-IV data
├── outputs/
│   └── .gitkeep                   # Generated outputs saved here
└── README.md
```

---

## Seven-Component Pipeline

| Component | Function |
|---|---|
| 1. Data Observation | Schema validation, raw record ingestion |
| 2. Issue Identification | Missing values, IQR outliers, duplicates |
| 3. Learning Mechanism | Sliding window issue-rate tracking (3-batch warm-up) |
| 4. Adaptive Adjustment | k₀ parameter update (α=0.05, δk=0.1) |
| 5. Adaptive Correction | Imputation, capping, deduplication |
| 6. Quality Assessment | DQS = (S_completeness + S_validity + S_uniqueness) / 3 |
| 7. Quality Output | Corrected records + DQS scores to output topic |

---

## Kafka Configuration

| Parameter | Value |
|---|---|
| Broker | localhost:9093 |
| Input topic | hstreamq-input |
| Output topic | hstreamq-output |
| Batch size | 10 records |
| Warm-up window | 3 batches |
| Serialisation | JSON |

---

## Proof-of-Concept Results (MIMIC-IV v3.1, 200 records)

| Quality issue | Before | After | Reduction |
|---|---|---|---|
| Missing field occurrences | 163 / 1,400 (11.6%) | — | Detected and flagged |
| Outlier instances (valuenum) | 67 / 200 (33.5%) | — | Capped to IQR boundary |
| Duplicate records | 0 / 200 (0.0%) | 0 | None detected |
| Mean batch DQS | — | 0.877 | — |

---

## Important Notes

- **MIMIC-IV data:** Cannot be redistributed. Users must obtain credentialed access via PhysioNet independently.
- **Proof-of-concept:** This pipeline simulates streaming from retrospective data. It is not validated for clinical deployment.
- **Outlier detection:** Uses a global IQR rule across all lab itemids. Item-specific clinical ranges are planned as future work.

---

## Citation

If you use H-StreamQ in your research, please cite:

```bibtex
@article{soomro2025hstreamq,
  title={H-StreamQ: A Proof-of-Concept Kafka-Based Pipeline for Adaptive Data Quality Monitoring in Healthcare Streaming Environments},
  author={Soomro, Gul Muhammad and Amur, Zaira Hassan and Krayem, Said and Chramcov, Bronislav and Jasek, Roman and Allahwerdi, Ismail},
  journal={SoftwareX},
  year={2025},
  note={Under review}
}
```

---

## License

MIT License. See [LICENSE](LICENSE) for details.

---

## Acknowledgements

This research was supported by the Internal Grant Agency of Tomas Bata University in Zlín, Faculty of Applied Informatics, grant number IGA/FAI/2024/006.
