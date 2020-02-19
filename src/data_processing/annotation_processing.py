import numpy as np


def chords_to_onehot(encoder, Timestamps, Chordlab, Chords, Artist='The Beatles'):
    chords2vec = {}
    for album in Chordlab[Artist].keys():
        chords2vec[album] = {}
        for track_no in Chordlab[Artist][album].keys():
            df_rows = Chordlab[Artist][album][track_no].itertuples()
            index = 0
            max_len = len(Chordlab[Artist][album][track_no])
            vector = np.empty((len(Chords),))
            row = next(df_rows)
            for timestamp in Timestamps[Artist][album][track_no]:
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


def data_to_numpy_arrays(chords2vec, Timeseries, frequencies_num, chords_num, test_track_no):
    x_initial_train = np.zeros((1, frequencies_num))
    y_initial_train = np.zeros((1, chords_num))
    x_initial_test = np.zeros((1, frequencies_num))
    y_initial_test = np.zeros((1, chords_num))
    for album in chords2vec.keys():
        for track_no in chords2vec[album].keys():
            if track_no != test_track_no or album != '12_-_Let_It_Be':
                y_initial_train = np.append(y_initial_train, chords2vec[album][track_no].T, axis=0)
                x_initial_train = np.append(x_initial_train,
                                            Timeseries['The Beatles'][album][track_no]['powerSpectrum'].T, axis=0)
            else:
                y_initial_test = np.append(y_initial_test, chords2vec[album][track_no].T, axis=0)
                x_initial_test = np.append(x_initial_test,
                                           Timeseries['The Beatles'][album][track_no]['powerSpectrum'].T, axis=0)

    return x_initial_train, y_initial_train, x_initial_test, y_initial_test


def slicing(chunk_size, frequencies_num, chords_num, x_initial_train, y_initial_train, x_initial_test, y_initial_test):

    # train data
    x_train = np.zeros((1, chunk_size, frequencies_num))  # num of frequencies
    y_train = np.zeros((1, chunk_size, chords_num))

    timestep = 0
    while timestep < x_initial_train.shape[0]:
        batch_x = np.resize(x_initial_train[timestep:timestep + chunk_size, :],
                            (1, chunk_size, frequencies_num))  # num of frequencies
        batch_y = np.resize(y_initial_train[timestep:timestep + chunk_size, :], (1, chunk_size, chords_num))

        x_train = np.append(x_train, batch_x, axis=0)
        y_train = np.append(y_train, batch_y, axis=0)
        timestep += chunk_size

    print(x_train.shape)
    print(y_train.shape)

    # test data
    x_test = np.zeros((1, chunk_size, frequencies_num))  # num of frequencies
    y_test = np.zeros((1, chunk_size, chords_num))

    timestep = 0
    while timestep < x_initial_test.shape[0]:
        batch_x = np.resize(x_initial_test[timestep:timestep + chunk_size, :],
                            (1, chunk_size, frequencies_num))  # num of frequencies
        batch_y = np.resize(y_initial_test[timestep:timestep + chunk_size, :], (1, chunk_size, chords_num))

        x_test = np.append(x_test, batch_x, axis=0)
        y_test = np.append(y_test, batch_y, axis=0)
        timestep += chunk_size

    print(x_test.shape)
    print(y_test.shape)

    # delete first line batch of array because its zeros
    x_train = np.delete(x_train, 0, 0)
    y_train = np.delete(y_train, 0, 0)
    x_test = np.delete(x_test, 0, 0)
    y_test = np.delete(y_test, 0, 0)

    return x_train, y_train, x_test, y_test


def chord_embeddings(Chordlab, Timeseries, test_track_no, chords_num, chunk_size):
    Chord_Progressions = []
    slice_count = 0
    for Artist in Chordlab.keys():
        for album in Chordlab[Artist].keys():
            for track_no in Chordlab[Artist][album].keys():
                if track_no == test_track_no and album == '12_-_Let_It_Be': continue
                progression = []
                times = Timeseries[Artist][album][track_no]['times']
                df_rows = Chordlab[Artist][album][track_no].itertuples()
                index = 0
                max_len = len(Chordlab[Artist][album][track_no])
                vector = np.empty((chords_num,))
                row = next(df_rows)
                for timestamp in times:

                    if ((index + 1) < max_len) & (timestamp >= row[2]):
                        index += 1
                        row = next(df_rows)

                    # not filtering silences
                    slice_count += 1
                    progression.append(row[3])

                    if slice_count % chunk_size == 0:
                        Chord_Progressions.append(progression)
                        progression = []

    return Chord_Progressions