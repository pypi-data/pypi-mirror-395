import librosa
import numpy as np
import pandas as pd

def extract_audio_features(file_path):

    y, sr = librosa.load(file_path, sr=None)

    # MFCC mean and std
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    mfcc_mean = np.mean(mfcc, axis=1)
    mfcc_std = np.std(mfcc, axis=1)

    # Zero Crossing Rate
    zcr = np.mean(librosa.feature.zero_crossing_rate(y=y))

    # RMS Energy
    rms_val = np.mean(librosa.feature.rms(y=y))

    # Spectral features
    spec_centroid = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))
    spec_bandwidth = np.mean(librosa.feature.spectral_bandwidth(y=y, sr=sr))
    spec_rolloff = np.mean(librosa.feature.spectral_rolloff(y=y, sr=sr))
    spec_contrast = np.mean(librosa.feature.spectral_contrast(y=y, sr=sr))

    # Pitch (pyin)
    f0, voiced_flag, voiced_probs = librosa.pyin(
        y,
        fmin=librosa.note_to_hz('C2'),
        fmax=librosa.note_to_hz('C7')
    )
    pitch_mean = np.nanmean(f0)
    pitch_std = np.nanstd(f0)

    # All features into a row
    features = np.concatenate([
        mfcc_mean, mfcc_std,
        [zcr, rms_val, spec_centroid, spec_bandwidth,
         spec_rolloff, spec_contrast, pitch_mean, pitch_std]
    ])

    # column names
    columns = [f'mfcc_mean_{i+1}' for i in range(13)] + \
              [f'mfcc_std_{i+1}' for i in range(13)] + \
              ['zcr', 'rms', 'spec_centroid', 'spec_bandwidth',
               'spec_rolloff', 'spec_contrast', 'pitch_mean', 'pitch_std']

    df = pd.DataFrame([features], columns=columns)
    return df






