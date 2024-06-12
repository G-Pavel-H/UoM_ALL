---
{}
---
language: en
license: cc-by-4.0
tags:
- model
repo: https://drive.google.com/drive/folders/1UCREZU38qlWOGu3mORDJjqVtNTu0TrWA?usp=share_link

---

# Model Card for c09618hm-j80841pg-NLI

<!-- Provide a quick summary of what the model is/does. -->

This model combines the strengths of ELECTRA and RoBERTa, two advanced transformer-based architectures, to perform natural language inference (NLI). By integrating embeddings from both models, it offers enhanced capabilities for understanding and predicting relationships between premises and hypotheses in text, achieving higher accuracy and robustness in classification tasks.


## Model Details

### Model Description

<!-- Provide a longer summary of what this model is. -->

This model leverages the transformer architectures of ELECTRA and RoBERTa to tackle the task of natural language inference, where the goal is to determine if a hypothesis is true (entailment) or false (contradiction) based on a given premise. ELECTRA is utilized for its efficient discriminator-based approach that enhances learning efficiency by classifying whether tokens are original or replaced in a sentence, rather than merely predicting masked words. RoBERTa, known for its robust optimization on large text corpora without the next-sentence prediction objective, complements ELECTRA by providing deep contextual embeddings that capture subtle nuances in language. The model integrates these features through a custom architecture that concatenates embeddings from both models, feeding them into a final classifier that outputs the inference results. This combination not only improves the model's understanding of complex language constructs but also enhances its ability to generalize from training data to new, unseen examples, making it highly effective for applications requiring detailed language comprehension and reasoning.

- **Developed by:** Pavel Ghazaryan and Hayk Melkumyan
- **Language(s):** English
- **Model type:** PLM
- **Model architecture:** Transformers, ELECTRA, RoBERTa
- **Finetuned from model:** roberta-base, electra-base-discriminator

### Model Resources

<!-- Provide links where applicable. -->

- **Repository:** https://drive.google.com/drive/folders/1UCREZU38qlWOGu3mORDJjqVtNTu0TrWA?usp=share_link

## Training Details

### Training Data

<!-- This is a short stub of information on the training data that was used, and documentation related to data pre-processing or additional filtering (if applicable). -->

Around 26K pairs of texts provided in tran.csv dataset file. Data is truncated to 128 tokens for processing. The text is tokenized using separate tokenizers for ELECTRA and RoBERTa, optimizing compatibility and performance.

### Training Procedure

<!-- This relates heavily to the Technical Specifications. Content here should link to that section when it is relevant to the training procedure. -->
Custom model architecture combines ELECTRA's efficient learning and RoBERTa's robust embeddings. 


#### Training Hyperparameters

<!-- This is a summary of the values of hyperparameters used in training the model. -->


    - num_train_epochs: 3
    - per_device_train_batch_size: 8
    - per_device_eval_batch_size: 16
    - warmup_steps: 500
    - weight_decay: 0.07
    - logging_strategy: "epoch"
    - evaluation_strategy: "no"
    - learning_rate: 3e-5
    - max_grad_norm: 1.0
    - lr_scheduler_type: 'linear' 

#### Speeds, Sizes, Times

<!-- This section provides information about how roughly how long it takes to train the model and the size of the resulting model. -->


      - overall training time: 21 minutes
      - duration per training epoch: 7 minutes
      - model size: 900MB

## Evaluation

<!-- This section describes the evaluation protocols and provides the results. -->
The development set includes 3K pairs, with metrics focusing on binary classification tasks (Precision, Recall, F1-score, Accuracy), crucial for the model’s intended NLI applications.


### Testing Data & Metrics

#### Testing Data

<!-- This should describe any evaluation data used (e.g., the development/validation set provided). -->

The development set provided, amounting to 3K pairs.

#### Metrics

<!-- These are the evaluation metrics being used. -->


      - Precision
      - Recall
      - F1-score
      - Accuracy

### Results

The model obtained around 89% for all aforementioned metrics.

## Technical Specifications

### Hardware


      - RAM: at least 32 GB
      - Storage: at least 5GB,
      - GPU: L4

### Software


      - Transformers 4.18.0
      - Pytorch 1.11.0+cu113

## Bias, Risks, and Limitations

<!-- This section is meant to convey both technical and sociotechnical limitations. -->

The model's training data, while extensive, may not fully represent the linguistic diversity of broader populations, potentially leading to biased outcomes. Future updates will aim to address these limitations by expanding dataset diversity and refining computational strategies.

## Additional Information

<!-- Any other information that would be useful for other people to know. -->

The hyperparameters were determined by experimentation
      with different values and taking into account popular values chosen by various papers and experiments (no time and resources for applying hyperparameter optimization through GridSearch or Bayesian Optimization).
