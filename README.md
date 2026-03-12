# ASR Robustness Pipeline

### Evaluating Wav2Vec2 Phoneme Error Rate under variable SNR levels

[![DVC](https://img.shields.io/badge/Data_Version_Control-DVC-white.svg?logo=dvc&logoColor=945dd6)](https://dvc.org/)
[![Python 3.12](https://img.shields.io/badge/Python-3.12-3776ab.svg?logo=python&logoColor=white)](https://www.python.org/)
[![UV](https://img.shields.io/badge/Package_Manager-uv-blue.svg)](https://github.com/astral-sh/uv)

## Overview
This repository implements a production-grade MLOps pipeline designed to benchmark the robustness of a Wav2Vec2 Phoneme-based model (Hugging Face) against acoustic degradation. 

The project automates the entire lifecycle of an experiment:
1.  **Acoustic Augmentation**: Injecting white noise at specific Signal-to-Noise Ratios (SNR).
2.  **Inference**: Transcribing noisy audio into phonetic sequences using eSpeak-ng.
3.  **Evaluation**: Calculating the Phoneme Error Rate (PER).
4.  **Visualization**: Generating comparative analytics of performance vs. noise intensity.

---

## Architecture
The codebase follows Clean Architecture and Domain-Driven Design (DDD) principles to ensure high maintainability, separation of concerns, and testability:

* **`pipeline/domain/`**: Pure business logic and core domain entities (e.g., `Utterance`), independent of any external frameworks.
* **`pipeline/infra/`**: Technical implementations and external adapters (I/O, Hugging Face wrappers, Sound processing).
* **`pipeline/app/`**: Application services and orchestration logic for specific use cases (Transcribe, Evaluate).
* **`entrypoints/`**: Thin CLI wrappers used by the DVC pipeline to execute individual stages.

---

## Prerequisites
* **uv**: Fast Python package installer and resolver.
  `curl -LsSf https://astral.sh/uv/install.sh | sh`
* **Python 3.12+** (managed by uv).
* **eSpeak-ng**: Required for phonemization.
  * *Linux (Debian/Ubuntu)*: 
    `sudo apt-get update && sudo apt-get install espeak-ng`

---

## Installation & Setup

1.  **Clone the repository**:
    `git clone <your-repo-url>`
    `cd ucite_pro_skill_dvc_pipeline`

2.  **Synchronize dependencies**:
    `uv sync`

3.  **Initialize DVC**:
    `uv run dvc init --no-scm`

---

## Execution
The entire experiment is managed by DVC. To reproduce the results:

`uv run dvc repro`

### Parameters
You can adjust the noise levels in the `params.yaml` file:
- 20.0
- 10.0
- 0.0
- -5.0

---

## Results
The final output is a visualization located in `reports/per_vs_snr.png`. It illustrates the correlation between the Signal-to-Noise Ratio and the model's accuracy.

The SNR is calculated as follows:  
SNR_dB = 10 * log10(P_signal / P_noise)

---

## Testing & Quality
We maintain high code quality through static analysis and unit testing:

* **Linter**: `uv run ruff check .`
* **Type Checking**: `uv run mypy .`
* **Unit Tests**: `uv run pytest tests/`