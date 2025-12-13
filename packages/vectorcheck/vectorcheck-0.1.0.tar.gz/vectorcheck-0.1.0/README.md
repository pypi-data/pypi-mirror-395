# VectorCheck: AI Native Testing Framework

[![PyPI version](https://badge.fury.io/py/vectorboard.svg)](https://badge.fury.io/py/vectorboard)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

**VectorBoard** is a **regression testing framework** designed for AI agents and LLM-based applications.

Traditional string comparison methods (`assert a == b`) are often insufficient for testing generative AI, where responses can vary with each execution. VectorBoard leverages **Vector Similarity** and **Semantic Evaluation** to validate tests based on **"Intent"**, ensuring that semantically identical outputs pass even if the exact wording differs.

---

## ✨ Key Features

* **🧠 Semantic Testing:** Validates test results based on meaning rather than exact text matching. (Uses LLM Judge or Embedding Similarity)
* **⏪ Golden Data Replay:** Fetches verified "Golden Data" (production logs) from Weaviate and replays them to ensure regression stability.
* **⚡ Zero Config Setup:** Automatically generates optimal default configurations (including `.env`) if they are missing.
* **🔍 Smart Auto-Discovery:** Automatically detects and registers target functions within your project.
* **📊 CLI Dashboard:** Provides real-time, intuitive Pass/Fail reports directly in your terminal.

---

## 🚀 Installation

You can easily install VectorBoard via `pip`. (Requires the VectorWave framework)

```bash
pip install vectorcheck
````

-----

## 🏁 Quick Start

Run the following command in your project's root directory:

```bash
vw test
```

On the first run, it will automatically generate a `.env` file and apply local environment settings.

-----

## ⚙️ Configuration

### 1\. `vwtest.ini` (Testing Strategy)

You can define different testing strategies for each function. Use `similarity` for functions with high randomness, and `exact` for deterministic functions.

```ini
[vectorboard]
python_paths = test_ex  # Path to the module being tested

; 1. LLM Summary Function (High Randomness) -> Pass if similarity > 85%
[test:test_ex.example.generate_review_summary]
strategy = similarity
threshold = 0.85

; 2. Payment Process (Partial Changes like IDs) -> Pass if similarity > 95%
[test:test_ex.example.process_payment]
strategy = similarity
threshold = 0.95

; 3. URL Generation (Deterministic) -> Must match exactly
[test:test_ex.example.generate_report]
strategy = exact
```

### 2\. `.env` (Environment Variables)

Choose between HuggingFace (Free, Local) or OpenAI (Paid, High Performance) for your vectorizer.

```bash
# Default: Use Local HuggingFace Model (Zero Cost)
VECTORIZER="huggingface"
HF_MODEL_NAME="sentence-transformers/all-MiniLM-L6-v2"

# Optional: Use OpenAI
# OPENAI_API_KEY=sk-...
```

-----

## 🛠 CLI Usage

### Run Tests (`vw test`)

```bash
# Run all tests (follows ini configuration)
vw test

# Run a specific target function
vw test --target test_ex.example.process_payment

# Force Semantic (LLM Judge) mode for all tests
vw test --semantic

# Force Similarity mode (Threshold > 0.8) for all tests
vw test --threshold 0.8
```

### Export Logs (`vw export`)

Export execution logs from the DB for training or analysis purposes.

```bash
vw export --output ./data/dataset.jsonl
```

-----

## 🏗 Architecture

VectorBoard operates in integration with the **VectorWave** core.

1.  **Trace:** Captures function Inputs/Outputs and metadata, storing them in Weaviate (Vector DB).
2.  **Fetch:** Retrieves verified 'Golden Data' during testing.
3.  **Replay:** Re-executes the current code logic using the same inputs.
4.  **Evaluate:** Compares the past results (Expected) with the current results (Actual) in vector space.

-----

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.

Developed by **Kim Junyeong**.
