import pickle
import numpy as np
from scipy.signal import butter, filtfilt

# -------- Load file --------
path = "runs/exp/UBFC-rPPG_SizeW72_SizeH72_ClipLength210_DataTypeDiffNormalized_Standardized_DataAugNone_LabelTypeDiffNormalized_Crop_faceTrue_BackendHC_Large_boxTrue_Large_size1.5_Dyamic_DetTrue_det_len35_Median_face_boxTrue/saved_test_outputs/UBFC-rPPG_DeepPhys_UBFC-rPPG_outputs.pickle"

with open(path, "rb") as f:
    data = pickle.load(f)

predictions = data["predictions"]
labels = data["labels"]
fs = data["fs"]

print("Subjects:", list(predictions.keys()))
print("Sampling frequency:", fs)

# -------- Bandpass filter function --------
def bandpass_filter(signal, fs, low=0.75, high=2.5):
    nyq = 0.5 * fs
    low /= nyq
    high /= nyq
    b, a = butter(2, [low, high], btype='band')
    return filtfilt(b, a, signal)

# -------- HR computation function --------
def compute_hr(signal, fs):
    signal = signal - np.mean(signal)
    signal = bandpass_filter(signal, fs)

    n = len(signal)
    freqs = np.fft.rfftfreq(n, d=1/fs)
    fft = np.abs(np.fft.rfft(signal))

    mask = (freqs >= 0.75) & (freqs <= 2.5)
    fft_masked = fft[mask]
    freqs_masked = freqs[mask]

    peak_freq = freqs_masked[np.argmax(fft_masked)]

    # Harmonic correction
    if peak_freq > 2.0:
        peak_freq /= 2

    # Top 5 peaks
    indices = np.argsort(fft_masked)[-5:]
    top_peaks = freqs_masked[indices] * 60  # in bpm
    return peak_freq * 60, top_peaks

# -------- Loop through subjects --------
for subject in predictions.keys():
    print(f"\nSubject: {subject}")

    # Concatenate all clips
    pred_clips = predictions[subject]
    pred_signal = np.concatenate([np.squeeze(pred_clips[k]) for k in sorted(pred_clips.keys())])

    gt_clips = labels[subject]
    gt_signal = np.concatenate([np.squeeze(gt_clips[k]) for k in sorted(gt_clips.keys())])

    # Compute HR
    pred_hr, pred_peaks = compute_hr(pred_signal, fs)
    gt_hr, gt_peaks = compute_hr(gt_signal, fs)

    print(f"  Ground Truth HR : {gt_hr:.2f} bpm")
    print(f"  Estimated HR    : {pred_hr:.2f} bpm")
    print(f"  Signals identical? {np.allclose(pred_signal, gt_signal)}")
    print(f"  Top 5 predicted frequency peaks (bpm): {pred_peaks}")
    print(f"  Top 5 GT frequency peaks (bpm)      : {gt_peaks}")
    print("-" * 50)

    print(f"  Pred signal length: {len(pred_signal)}")
    print(f"  GT signal length  : {len(gt_signal)}")
