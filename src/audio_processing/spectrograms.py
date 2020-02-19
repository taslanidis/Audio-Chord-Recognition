# python input/output and regex
import re
import os
from pathlib import Path

# signal processing libraries
from scipy.io import wavfile
from scipy import signal

# librosa
import librosa
from librosa.core.time_frequency import frames_to_time


# get all audio files and create spectrogram for each track
def create_spectrograms(n_fft=1024, nperseg=1024, audiofiles_path='Test-Audiofiles/The Beatles'):
    Spectrograms = {'The Beatles': {}}
    frequencies_num = 0
    for filename in Path(audiofiles_path).glob('**/wav/*.wav'):

        path, track = os.path.split(filename)
        path, wav = os.path.split(path)
        path, album = os.path.split(path)

        track_no = re.search('([0-9].).', track).group(1)

        # read wav and create spectrogram
        sample_rate, samples = wavfile.read(filename)
        frequencies, times, powerSpectrum = signal.spectrogram(samples, fs=sample_rate, nfft=n_fft, nperseg=nperseg)
        frequencies_num = frequencies.shape[0]

        if album not in Spectrograms['The Beatles']:
            Spectrograms['The Beatles'][album] = {}

        Spectrograms['The Beatles'][album][track_no] = {'powerSpectrum': powerSpectrum,
                                                        'frequencies': frequencies,
                                                        'times': times}
    return Spectrograms, frequencies_num


# get all audio files and create chromagram for each track
def create_chromagrams(hop_length=512, audiofiles_path='Audiofiles/The Beatles'):
    Chromagrams = {'The Beatles': {}}
    Timestamps = {'The Beatles': {}}

    for filename in Path(audiofiles_path).glob('**/wav/*.wav'):

        path, track = os.path.split(filename)
        path, wav = os.path.split(path)
        path, album = os.path.split(path)

        track_no = re.search('([0-9].).', track).group(1)

        # read wav and create chromagram
        track, sample_rate = librosa.load(filename)
        track_time = librosa.get_duration(y=track, sr=sample_rate)
        n_fft = int(track_time // (hop_length / sample_rate))
        chroma = librosa.feature.chroma_stft(track, sr=sample_rate, n_fft=n_fft, hop_length=hop_length)

        frames = list(range(0, chroma.shape[1]))
        times = frames_to_time(frames, sr=sample_rate, hop_length=hop_length, n_fft=n_fft)

        if album not in Chromagrams['The Beatles']:
            Chromagrams['The Beatles'][album] = {}
            Timestamps['The Beatles'][album] = {}

        Chromagrams['The Beatles'][album][track_no] = chroma.T
        Timestamps['The Beatles'][album][track_no] = times

    return Chromagrams, Timestamps
