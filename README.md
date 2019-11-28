# Audio Chord Estimation

In this project, we searching for methods to recognize audio chord with neural networks
There are various approach for either **Pre-Processing** and **Neural Network Modeling**

## Pre Processing

* One Hot Encodings for Annotations
* Indexing on Annotations & Timeseries
![](images/Vector_flow.png)
* Slicing & Padding
![](images/slicing.png)

## Train Data

### Spectrograms
Converting raw audio to spectrograms, and use frequencies as features.

### Chromagrams
Converting raw audio to spectrograms, and then "stack" each frequency to it's semitone -> So we have 12 features, (same as the number of semitones).

## Exploring the use of chord embeddings
* chord embeddings just like NLP -> <b>chords2vec</b>
