---
{}
---
language: en
license: cc-by-4.0
tags:
- nli-premise-hypothesis-classification
repo: https://drive.google.com/drive/folders/1K7nLTnhCAv_MXHH9AjFCRUoo5Zgu-IKi?usp=sharing

---

# Model Card for c09618hm-j80841pg-NLI

<!-- Provide a quick summary of what the model is/does. -->

This is a classification model that was trained to
      detect whether premise and hypothesis entailment or conradictioc.


## Model Details

### Model Description

<!-- Provide a longer summary of what this model is. -->

This model is based upon a Attention LSTM model that uses BERT word embeddings.

- **Developed by:** Pavel Ghazaryan and Hayk Melkumyan
- **Language(s):** English
- **Model type:** Supervised
- **Model architecture:** Attention LSTM with BERT Embeddings
- **Finetuned from model [optional]:** bert-base-uncased

### Model Resources

<!-- Provide links where applicable. -->

- **Repository:** [More Information Needed]
- **Paper or documentation:** [More Information Needed]

## Training Details

### Training Data

<!-- This is a short stub of information on the training data that was used, and documentation related to data pre-processing or additional filtering (if applicable). -->

30K pairs of texts drawn from emails, news articles and blog posts.

### Training Procedure

<!-- This relates heavily to the Technical Specifications. Content here should link to that section when it is relevant to the training procedure. -->

#### Training Hyperparameters

<!-- This is a summary of the values of hyperparameters used in training the model. -->


      - learning_rate: 0.01
      - train_batch_size: 16
      - eval_batch_size: 16
      - num_epochs: 5

#### Speeds, Sizes, Times

<!-- This section provides information about how roughly how long it takes to train the model and the size of the resulting model. -->


      - overall training time: 20 minutes
      - duration per training epoch: 4 minutes
      - model size: 411MB

## Evaluation

<!-- This section describes the evaluation protocols and provides the results. -->

### Testing Data & Metrics

#### Testing Data

<!-- This should describe any evaluation data used (e.g., the development/validation set provided). -->

A subset of the development set provided, amounting to 3K pairs.

#### Metrics

<!-- These are the evaluation metrics being used. -->


      - Precision
      - Recall
      - F1-score
      - Accuracy

### Results

The model obtained an F1-score of 72% and an accuracy of 70%.

## Technical Specifications

### Hardware


      - RAM: at least 16 GB
      - Storage: at least 2GB,
      - GPU: L4

### Software


      - Transformers 4.18.0
      - Pytorch 1.11.0+cu113

## Bias, Risks, and Limitations

<!-- This section is meant to convey both technical and sociotechnical limitations. -->

Any inputs (concatenation of two sequences) longer than
      512 subwords will be truncated by the model.

## Additional Information

<!-- Any other information that would be useful for other people to know. -->

The hyperparameters were determined by experimentation
      with different values.