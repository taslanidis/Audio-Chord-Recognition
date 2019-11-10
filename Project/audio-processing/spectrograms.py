# python input/output and regex
import re
import os
from pathlib import Path

# signal processing libraries
from scipy.io import wavfile
from scipy import signal


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
