# data-prep-engine  
A lightweight, modular, production-friendly Python library for **data ingestion**, **diagnostics**, **sanitization**, **visualization**, and **end-to-end ML data preparation**.

Built to provide a **single, unified, reproducible** pipeline that works across CSV, JSON, Parquet, images, and more — without depending on massive profiling libraries.

---

## 🌟 Key Features

### 🔌 **1. Ingestion Engine (Loader)**
Load CSV, JSON, Parquet, Images, and more into a unified `StandardTable`.

### 🩺 **2. Diagnostics Engine (DataDoctor)**
Column-level summaries, warnings, null counts, duplicates, outliers, cardinality & constant-column detection.

### 🧼 **3. Sanitization Engine (The Surgeon)**
- Missing value imputation  
- Duplicate removal  
- IQR-based outlier capping  
- Fully extensible sanitization steps  

### 🎨 **4. Visualization Engine (The Artist)**
Smart single-flag plots (numeric histograms, categorical counts) guided by the diagnostics report.

### 🚀 **5. AutoPrep — End-to-End Unified Pipeline**
One line to prepare any dataset:

```python
from data_prep_engine import AutoPrep

prep = AutoPrep.default()
result = prep.run_from_uri("data.csv")

result.cleaned_table.to_pandas().head()

⚙️ Installation

```bash
pip install data-prep-engine
```

(Coming soon to PyPI — currently install locally using:)

```bash
### pip install -e .
```

## 🏁 Quickstart

```bash
from data_prep_engine import AutoPrep
prep = AutoPrep.default()
# Load, diagnose, clean, visualize — all in one step
result = prep.run_from_uri("data.csv")
print(result.sanitization_logs)
result.cleaned_table.to_pandas().head()
```

## 📥 Ingestion Examples

```bash
from data_prep_engine.ingestion import Loader
loader = Loader()
table_csv    = loader.load("data.csv")
table_json   = loader.load("data.json")
table_parquet = loader.load("data.parquet")
table_image   = loader.load("image.jpg")   # stored as array metadata
```
All ingestion results are returned as a StandardTable, guaranteeing uniform structure.

## 🩺 Diagnostics Examples

```bash
from data_prep_engine.diagnostics import DataDoctor
doctor = DataDoctor()
report = doctor.diagnose(table)
print(report.summary_table())
print(report.warnings)
```
Common warnings include:
	• High missing values
	• High-cardinality categorical columns
	• Outlier-heavy numeric columns
	• Constant features
Duplicate rows

## 🧼 Sanitization Examples

```bash
from data_prep_engine.sanitization.pipeline import SanitizationPipeline
from data_prep_engine.sanitization.steps import (
    MissingValueHandler,
    DuplicateHandler,
    OutlierHandler,
)
pipeline = SanitizationPipeline([
    MissingValueHandler(),
    DuplicateHandler(),
    OutlierHandler(),
])
result = pipeline.run(table)
clean_table = result.cleaned_table
print(result.logs)
```

## 🎨 Visualization Examples

```bash
from data_prep_engine.visualization import Artist
fig = Artist.plot(clean_table, doctor.diagnose(clean_table))
fig.show()
Or save as PNG:

Artist.to_png(fig, "preview.png")
```

### 🚀 Full AutoPrep Pipeline

```bash
from data_prep_engine import AutoPrep
prep = AutoPrep.default()
result = prep.run_from_uri("data.csv")
print("Warnings before:", result.diagnostics_before.warnings)
print("Warnings after:", result.diagnostics_after.warnings)
fig = prep.plot(result)
fig.show()
```

###📐 Project Architecture

```bash
data_prep_engine/
│
├── ingestion/         # Loaders + format adapters
├── diagnostics/       # DataDoctor + reports
├── sanitization/      # Sanitization steps + pipeline
├── visualization/     # Artist plotting engine
├── core/              # StandardTable + utilities
└── autoprep.py        # Full unified pipeline
```
Each block is independent, testable, and extendable.

### 🧪 Running Tests

```bash
pytest -q
```
The test suite covers:
	• Ingestion adapters
	• Diagnostics summaries
	• Sanitization steps
	• Visualization engine
	• AutoPrep unified pipeline

### 🤝 Contributing
	1. Fork the repo
	2. Create a feature branch
	3. Add tests for your change
	4. Submit a PR
All PRs must pass GitHub Actions (unit tests, linting, and security scanners).

### 📜 License
MIT License © 2025



