# Dictionaries
ChordLib = {'C' : 0, 'C#': 1, 'Db' : 1, 'D' : 2, 'D#' : 3, 'Eb' : 3, 'E' : 4, 'F' : 5, 'F#' : 6, 'Gb' : 6, 'G' : 7, 'G#' : 8, 'Ab' : 8, 'A' : 9, 'A#' : 10, 'Bb' : 10, 'B' : 11, 'N' : 12}
InverseLib = {0 : 'C', 1 : 'C#', 2 : 'D', 3 : 'Eb', 4 : 'E', 5 : 'F', 6 : 'Gb', 7 : 'G', 8 : 'G#', 9 : 'A', 10 : 'Bb', 11 : 'B', 12 : 'N'}


def parse_chords(Chords, df):
    for chord in Chords:
        # print('* Chord: ', chord)
        Mode = 'Major'
        bass = ''
        fourth_note = ''
        fourth_note_mode = ''
        Unknown = False
        if chord.find(':') != -1:
            root, chord = chord.split(':')
            if chord[:3] == 'min':
                Mode = 'Minor'
                if chord != 'min':
                    if chord[3] == '7':
                        fourth_note = '7'
                        fourth_note_mode = 'minor'
                        if chord[3:].find('/') != -1:
                            chord = chord[4:]
                            if chord in ['3' ,'b3' ,'5', 'b5', '7', 'b7']:
                                bass = chord
                            else:
                                Unknown = True
                        else:
                            bass = '0'
                    elif chord.find('/') != -1:
                        _, chord = chord.split('/')
                        if chord in ['3' ,'b3' ,'5', 'b5']:
                            bass = chord
                        else:
                            Unknown = True
                    else:
                        Unknown = True
                else:
                    bass = '0'
            elif chord[:3] == 'dim':
                Mode = 'Dim'
                if chord != 'dim':
                    chord = chord[3:]
                    fourth_note = chord[0]
                    fourth_note_mode = 'dominant'
                    if fourth_note == '/':
                        fourth_note = ''
                        bass = chord[1:]
                    else:
                        chord = chord[1:]
                        if chord.find('/') != -1:
                            bass = chord[1:]
                        else:
                            bass = '0'
                else:
                    bass = '0'
            elif chord[:3] == 'aug':
                Mode = 'Aug'
                if chord != 'aug':
                    fourth_note = chord[3]
                    fourth_note_mode = 'major'
                    if fourth_note == '/':
                        fourth_note = ''
                        bass = chord[4:]
                    else:
                        if chord[3:].find('/') != -1:
                            bass = chord[5:]
                        else:
                            bass = '0'
                else:
                    bass = '0'
            elif chord[:3] == 'maj':
                Mode = 'Major'
                fourth_note_mode = 'major'
                if chord != 'maj':
                    chord = chord[3:]
                    fourth_note = chord[0]
                    if fourth_note == '/':
                        fourth_note, bass = chord.split('/')
                    elif fourth_note == '(':
                        fourth_note = chord[1]
                        if fourth_note != '9':
                            Unknown = True
                        bass = '0'
                    else:
                        bass = '0'
                else:
                    bass = '0'
            elif chord[:4] == 'sus2':
                Mode = 'Sus2'
                bass = '0'
                Unknown = True
            elif chord[:4] == 'sus4':
                Mode = 'Sus4'
                bass = '0'
                Unknown = True
            elif chord[:4] == 'sus7':
                Mode = 'Sus7'
                bass = '0'
                Unknown = True
            elif chord[:4] == 'sus9':
                Mode = 'Sus9'
                bass = '0'
                Unknown = True
            elif chord[:4] == 'hdim':
                # half diminished
                Mode ='Dim'
                fourth_note_mode = 'minor'
                fourth_note = chord[4]
            else:
                Mode = 'Major'
                # Dominant seventh
                fourth_note = chord[0]
                fourth_note_mode = 'dominant'
                if fourth_note != '(':
                    if chord[1:].find('/') != -1:
                        if chord[1:].find('(') != -1:
                            bass = chord[2]
                        else:
                            bass = chord[2:]
                    else:
                        bass = '0'
                else:
                    Unknown = True

        elif chord.find('/') != -1:
            root, chord = chord.split('/')
            if chord in ['3', 'b3', '5', 'b5']:
                bass = chord
            else:
                Unknown = True
        else:
            root = chord
            bass = '0'

        if not Unknown:
            # print(root, bass, Mode, fourth_note)
            df['Root'].append(ChordLib[root])

            if root == 'N':
                df['Bass'].append(0)
            elif ChordLib[root] + Semitonize(bass, Mode) <= 12:
                df['Bass'].append(ChordLib[root] + Semitonize(bass, Mode))
            else:
                df['Bass'].append((ChordLib[root] + Semitonize(bass, Mode)) % 12)

            df['Unknown'].append(0)
            df['Major'].append(int(Mode == 'Major'))
            df['Minor'].append(int(Mode == 'Minor'))
            df['Diminished'].append(int(Mode == 'Dim'))
            df['Augmented'].append(int(Mode == 'Aug'))
            df['Seventh'].append(int(fourth_note == '7' and fourth_note_mode == 'dominant'))
            df['Major Seventh'].append(int((fourth_note == '7' or fourth_note == '9') and fourth_note_mode == 'major'))
            df['Minor Seventh'].append(int((fourth_note == '7' or fourth_note == '9') and fourth_note_mode == 'minor'))
            df['Major Sixth'].append(int(fourth_note == '6'))
            df['Ninth'].append(int(fourth_note == '9'))
        else:
            # print ('Unknown')
            df['Root'].append(ChordLib[root])
            df['Bass'].append(0)
            df['Unknown'].append(1)
            df['Major'].append(0)
            df['Minor'].append(0)
            df['Diminished'].append(0)
            df['Augmented'].append(0)
            df['Seventh'].append(0)
            df['Major Seventh'].append(0)
            df['Minor Seventh'].append(0)
            df['Major Sixth'].append(0)
            df['Ninth'].append(0)
        # print('-----')


def Semitonize(interval, mode):
    if interval == '0':
        return 0

    if mode == 'Major':
        if interval == '2':
            return 2
        elif interval == 'b2':
            return 1
        if interval == '3':
            return 4
        elif interval == 'b3':
            return 3
        if interval == '5':
            return 7
        elif interval == 'b5':
            return 6
        if interval == '6':
            return 9
        elif interval == 'b6':
            return 8
        if interval == '7':
            return 10
        elif interval == 'b7':
            return 10
        if interval == '9':
            return 13
        else:
            return 0
    elif mode == 'Minor':
        if interval == '2':
            return 2
        elif interval == 'b2':
            return 1
        if interval == '3':
            return 4
        elif interval == 'b3':
            return 3
        if interval == '5':
            return 7
        elif interval == 'b5':
            return 6
        if interval == '7':
            return 10
        elif interval == 'b7':
            return 10
    elif mode == 'Dim':
        if interval == '2':
            return 2
        elif interval == 'b2':
            return 1
        if interval == '3':
            return 4
        elif interval == 'b3':
            return 3
        if interval == '5':
            return 7
        elif interval == 'b5':
            return 6
        if interval == '7':
            return 10
        elif interval == 'b7':
            return 10
        else:
            return 0
    elif mode == 'Aug':
        if interval == '2':
            return 2
        elif interval == 'b2':
            return 1
        if interval == '3':
            return 4
        elif interval == 'b3':
            return 3
        if interval == '5':
            return 7
        elif interval == 'b5':
            return 6
        if interval == '7':
            return 10
        elif interval == 'b7':
            return 10
        else:
            return 0
    else:
        return 0


def Chordify(root, bass, quality):
    if root == 'N': return root
    inverse = ''
    chord = root

    if quality[2] == 1:
        chord += ':min'

    if quality[3] == 1:
        chord += ':7'

    if quality[4] == 1:
        chord += ':maj7'

    if quality[5] == 1:
        chord += ':min7'

    if root != bass:
        semitones = (12 - ChordLib[root]) - (12 - ChordLib[bass])
        if semitones < 0:
            semitones += 12
        if semitones != 0:
            if semitones == 2:
                inverse = '/2'
            elif semitones == 3:
                inverse = '/b3'
            elif semitones == 4:
                inverse = '/3'
            elif semitones == 5:
                inverse = '/4'
            elif semitones == 6:
                inverse = '/b5'
            elif semitones == 7:
                inverse = '/5'
            elif semitones == 8:
                inverse = '/6'
            elif semitones == 9:
                inverse = '/b7'
            elif semitones == 10:
                inverse = '/7'
            elif semitones == 11:
                inverse = '/#7'
        chord += inverse
    return chord


