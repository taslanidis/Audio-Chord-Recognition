# python input/output and regex
import re
import os
from pathlib import Path
from pydub import AudioSegment


# get all audio files and create spectrogram for each track
def mp3_to_wav(audiofile_path='Audiofiles/The Beatles', channels=1):
    for filename in Path(audiofile_path).glob('**/mp3/*.mp3'):
        # files
        path, track = os.path.split(filename)
        dst = re.sub(r'mp3', 'wav/', path) + re.sub(r'mp3', 'wav', track)
        # convert wav to mp3
        sound = AudioSegment.from_mp3(filename)
        # optional line if you want them in mono
        sound = sound.set_channels(channels)
        sound.export(dst, format="wav")


def stereo_to_mono(audiofile_path='Audiofiles/The Beatles'):
    for filename in Path(audiofile_path).glob('**/wav/*.wav'):
        # convert stereo to mono
        sound = AudioSegment.from_wav(filename)
        sound = sound.set_channels(1)
        sound.export(filename, format="wav")
