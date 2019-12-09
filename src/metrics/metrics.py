import chord_parser


def CSR(Spectrograms, Chordlab, df_predictions, album_test_track, test_track_no):

    segments_true_chords = True_Chords(Spectrograms, Chordlab, 'The Beatles', album_test_track, test_track_no)

    # segments of audio data
    segments = Spectrograms['The Beatles'][album_test_track][test_track_no]['times']

    # compute total time of correct estimations
    step = 0
    prev_timing = 0
    total_time_of_correct_estimation = 0
    for time in segments:
        true_chord = segments_true_chords[step]
        estimated_chord = chord_parser.Chordify(df_predictions['Root'][step], df_predictions['Bass'][step],
                                   df_predictions['Quality'][step])
        if estimated_chord == true_chord:
            total_time_of_correct_estimation += time - prev_timing
        prev_timing = time
        step += 1

    # total time of segments
    total_time_of_segments = Spectrograms['The Beatles'][album_test_track][test_track_no]['times'][-1]

    # CSR
    CSR = total_time_of_correct_estimation / total_time_of_segments
    print("Accuracy Achieved by MIREX metric CSR = % 3.3f" % (CSR * 100))
    return CSR


def True_Chords(Spectrograms, Chordlab, Artist, album_test_track, test_track_no):
    times = Spectrograms[Artist][album_test_track][test_track_no]['times']
    df_rows = Chordlab[Artist][album_test_track][test_track_no].itertuples()
    index = 0
    max_len = len(Chordlab[Artist][album_test_track][test_track_no])
    segments_true_chords = []
    row = next(df_rows)
    for timestamp in times:
        if ((index + 1) < max_len) & (timestamp >= row[2]):
            index += 1
            row = next(df_rows)
        segments_true_chords.append(row[3])
    return segments_true_chords
