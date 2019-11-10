import numpy as np


def chords_to_onehot(encoder, Spectrograms, Chordlab, Chords, Artist='The Beatles'):
    chords2vec = {}
    for album in Spectrograms[Artist].keys():
        chords2vec[album] = {}
        for track_no in Spectrograms[Artist][album].keys():
            times = Spectrograms[Artist][album][track_no]['times']
            df_rows = Chordlab[Artist][album][track_no].itertuples()
            index = 0
            max_len = len(Chordlab[Artist][album][track_no])
            vector = np.empty((len(Chords),))
            row = next(df_rows)
            for timestamp in times:
                if ((index + 1) < max_len) & (timestamp >= row[2]):
                    index += 1
                    row = next(df_rows)
                vector = np.column_stack((vector, encoder.transform([[row[3]]]).toarray()[0]))
            chords2vec[album][track_no] = vector
            # print(album, ': track ', track_no, ' completed')

    # Take care fo the one extra row in the beginning of the array
    for album in chords2vec.keys():
        for track_no in chords2vec[album].keys():
            chords2vec[album][track_no] = np.delete(chords2vec[album][track_no], 0, 1)

    return chords2vec
