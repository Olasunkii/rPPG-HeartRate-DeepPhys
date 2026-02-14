# Remote Photoplethysmography (rPPG) – DeepPhys Implementation

This project implements a remote photoplethysmography (rPPG) pipeline using the DeepPhys model from the rPPG-Toolbox repository. The goal is to estimate heart rate (HR) from facial videos and compare it with ground truth PPG signals.

---

## Project Objective

The objectives of this project were to:

- Deploy an existing implementation on a subset of the UBFC dataset
- Compare estimated heart rate (HR) with ground truth HR values
- Summarize findings

---

## Original Repository

This project is based on the following repository:

rPPG-Toolbox  
https://github.com/ubicomplab/rPPG-Toolbox

---

## Environment Setup

### 1. Clone Repository

```bash
git clone https://github.com/ubicomplab/rPPG-Toolbox.git
cd rPPG-Toolbox
```

### 2. Create Conda Environment

```bash
conda create -n rppg python=3.8
conda activate rppg
```

### 3. Install Requirements

```bash
pip install -r requirements.txt
```

Notes:
- Mamba and causal-conv1d==1.0.0 were not used to avoid failures due to CUDA complications.
- CPU execution was used for testing.
- Bland-Altman metric was removed to avoid the program from crashing since KDE cannot handle NaN, Inf and Zero variance data

---

## Dataset

Dataset used:
- UBFC-rPPG dataset (small subset for testing), Default setting was UBFC-PHYS

Dataset directory structure:

```
dataset/
  UBFC_small/
    subject1/
    subject2/
    subject3/
```

---

## Running Inference

To run inference:

```bash
python main.py --config_file configs/infer_configs/UBFC-rPPG_UBFC-PHYS_DEEPPHYS_BASIC.yaml
```

Prediction outputs are saved in:

```
runs/exp/.../saved_test_outputs/
```

---

## Example Result

| Subject   | Ground Truth HR | Estimated HR |
|-----------|-----------------|--------------|
| subject3  | 65.00 bpm       | 65.00 bpm    |

Observations:

- Estimated HR matches ground truth HR.
- Signals are not identical in waveform.
- Dominant frequency peak is correctly captured.

---

## Key Insights

- rPPG can successfully estimate heart rate from facial video.
- Even when waveform shapes differ, frequency-domain alignment validates accuracy.
- Bandpass filtering improves physiological signal isolation.
- FFT peak detection provides reliable HR estimation.

---

## Important Files

- `load_output.py` – Extracts and computes HR from saved outputs
- `configs/` – Configuration files used for inference
- `README.md` – Project documentation
- `RESULTS.md` – Summary of results and interpretation

---

## Notes

- Large dataset files and experiment outputs are excluded from version control.
- `.gitignore` is configured to ignore dataset and run outputs.

---

##  Author
Olasunkanmi Felix Oyadokun 
2026

