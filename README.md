# Audio Chord Estimation - *(Ongoing...)*

In this project, we searching for methods to recognize audio chord with neural networks
There are various approach for either **Pre-Processing** and **Neural Network Modeling**

## Pre Processing

* **One Hot Encodings** for Annotations
* **Indexing** on Annotations & Timeseries
![](images/Vector_flow.png)
* **Slicing** *in small chunks in order for the NN to extract information* & **Padding** *with zeros at frequencies, and the Neutral chord in Annotations*.
![](images/slicing.png)

## Train Data

### Spectrograms
Converting raw audio to spectrograms, and use frequencies as features.

### Chromagrams
Converting raw audio to spectrograms, and then "stack" each frequency to it's semitone -> So we have 12 features, (same as the number of semitones).

## Model

I tried to predict chords, and not each semitone separately and then build the chord

### Spectrogram models
- Convolutional Layers for 'chord entities'
- Recurrent Layers for 'sequences of chords'
- Embedding Layer for 'harmonies'
- Final Dense Layer with softmax activation for chord prediction

### Chromagram models
- Multiple Recurrent Convolutional Layers for 'chord entities'
- Recurrent Layer for 'sequences of chords'
- sigmoid activation for the semitones activated
- Dense layer, and then softmax activation for the chord

## Exploring the use of chord embeddings
* chord embeddings just like NLP -> <b>chords2vec</b>
