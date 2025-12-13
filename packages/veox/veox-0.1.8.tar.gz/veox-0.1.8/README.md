# Veox: The Incredible ML Client for DOUG

Veox is a standalone, pip-installable Python client for DOUG (Distributed Optimization Using GP). It delivers an "incredible" developer experience with a sklearn-style API, real-time TQDM progress bars, and rich terminal output.

## Features

- **sklearn-style API**: Familiar `fit(X, y)` interface with full pandas DataFrame support.
- **Distributed Evolution**: Seamlessly offload heavy computation to the DOUG cluster.
- **Real-time Streaming**: Beautiful TQDM progress bars and live status updates.
- **Built-in Datasets**: Instant access to curated ML datasets (Heart Disease, Titanic, etc.).
- **Code Pulling**: Extract generated pipeline code directly to your local machine.

## Installation

```bash
pip install veox
```

## Usage

### Python API

```python
from veox import Veox
from veox.datasets import load_heart_disease

# Initialize client
client = Veox(api_url="http://localhost:8090")

# Load built-in dataset
X, y = load_heart_disease()

# Run evolution
model = client.fit(X=X, y=y, task="binary", population=50, generations=10)

# Pull best pipeline code
client.pull_code(output_file="best_pipeline.py")
```

### Command Line Interface

```bash
# Run evolution on a CSV file
veox fit --csv my_data.csv --target-column target --task binary --verbose

# Pull code from the last job
veox pull-code --job-id job_abc123 --output pipeline.py
```
