import pandas as pd
from transformers import ElectraTokenizer, ElectraForSequenceClassification, Trainer, TrainingArguments
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from datasets import Dataset

def compute_metrics(pred):
    labels = pred.label_ids
    preds = pred.predictions.argmax(-1)
    precision, recall, f1, _ = precision_recall_fscore_support(labels, preds, average='binary')
    acc = accuracy_score(labels, preds)
    return {
        'accuracy': acc,
        'f1': f1,
        'precision': precision,
        'recall': recall
    }


# Load dataset
train_df = pd.read_csv('/content/drive/MyDrive/NLU/training_data/NLI/train.csv')
train_df, val_df = train_test_split(train_df, test_size=0.1, random_state=42)

# Convert to HuggingFace dataset format
train_dataset = Dataset.from_pandas(train_df)
val_dataset = Dataset.from_pandas(val_df)

# Load tokenizer
tokenizer = ElectraTokenizer.from_pretrained('google/electra-base-discriminator')

def tokenize_data(example):
    return tokenizer(example['premise'], example['hypothesis'], truncation=True, padding='max_length', max_length=128)

train_dataset = train_dataset.map(tokenize_data, batched=True)
val_dataset = val_dataset.map(tokenize_data, batched=True)

model = ElectraForSequenceClassification.from_pretrained('google/electra-base-discriminator', num_labels=2)

# Training arguments
training_args = TrainingArguments(
    output_dir='/content/drive/MyDrive/NLU/results',          # output directory
    num_train_epochs=3,              # number of training epochs
    per_device_train_batch_size=16,   # batch size for training
    per_device_eval_batch_size=64,   # batch size for evaluation
    warmup_steps=500,                # number of warmup steps for learning rate scheduler
    weight_decay=0.01,               # strength of weight decay
    logging_dir='/content/drive/MyDrive/NLU/logs',            # directory for storing logs
    logging_strategy="epoch",
    evaluation_strategy="epoch",
    learning_rate=3e-5,
    max_grad_norm=1.0,
    load_best_model_at_end=True,
    metric_for_best_model="accuracy",
    save_strategy="epoch",
    save_total_limit=2,
    lr_scheduler_type='linear'
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    compute_metrics=compute_metrics
)

trainer.train()
trainer.evaluate()
























































# from transformers import ElectraTokenizer, ElectraModel, AdamW, Trainer, TrainingArguments
# from torch.utils.data import DataLoader
# import torch
# import pandas as pd
# from sklearn.model_selection import train_test_split
# from datasets import Dataset
# from datasets import load_metric

# # Constants
# MODEL_NAME = 'google/electra-base-discriminator'
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# # Load tokenizer and model
# tokenizer = ElectraTokenizer.from_pretrained(MODEL_NAME)
# electra_model = ElectraModel.from_pretrained(MODEL_NAME).to(device)

# class NLI_Dataset(torch.utils.data.Dataset):
#     def __init__(self, encodings, labels):
#         self.encodings = encodings
#         self.labels = labels

#     def __getitem__(self, idx):
#         item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
#         item['labels'] = torch.tensor(self.labels[idx])
#         return item

#     def __len__(self):
#         return len(self.labels)

# # Load data and prepare dataset
# df = pd.read_csv('training_data/NLI/train.csv')
# train_df, val_df = train_test_split(df, test_size=0.1)

# # Tokenization
# train_encodings = tokenizer(train_df['premise'].tolist(), train_df['hypothesis'].tolist(), truncation=True, padding=True)
# val_encodings = tokenizer(val_df['premise'].tolist(), val_df['hypothesis'].tolist(), truncation=True, padding=True)

# # Dataset preparation
# train_dataset = NLI_Dataset(train_encodings, train_df['label'].tolist())
# val_dataset = NLI_Dataset(val_encodings, val_df['label'].tolist())

# # Define model
# class ElectraForNLI(torch.nn.Module):
#     def __init__(self):
#         super(ElectraForNLI, self).__init__()
#         self.electra = electra_model
#         self.classifier = torch.nn.Linear(768, 2)  # Assuming binary classification

#     def forward(self, input_ids, attention_mask, labels=None):
#         outputs = self.electra(input_ids=input_ids, attention_mask=attention_mask)
#         sequence_output = outputs.last_hidden_state[:, 0, :]  # Use the [CLS] token
#         logits = self.classifier(sequence_output)

#         if labels is not None:
#             loss_fct = torch.nn.CrossEntropyLoss()
#             loss = loss_fct(logits.view(-1, 2), labels.view(-1))
#             return loss, logits
#         return logits

# model = ElectraForNLI().to(device)


# # Metric for evaluation
# metric = load_metric("accuracy")

# def compute_metrics(eval_pred):
#     logits, labels = eval_pred
#     predictions = np.argmax(logits, axis=-1)
#     return metric.compute(predictions=predictions, references=labels)


# # Define training arguments
# training_args = TrainingArguments(
#     output_dir='./results',          # output directory
#     num_train_epochs=3,              # number of training epochs
#     per_device_train_batch_size=16,   # batch size for training
#     per_device_eval_batch_size=64,   # batch size for evaluation
#     warmup_steps=500,                # number of warmup steps for learning rate scheduler
#     weight_decay=0.01,               # strength of weight decay
#     logging_dir='./logs',            # directory for storing logs
#     logging_strategy="epoch",
#     evaluation_strategy="epoch",
#     learning_rate=3e-5,
#     max_grad_norm=1.0,
#     load_best_model_at_end=True,
#     metric_for_best_model="accuracy",
#     save_strategy="epoch",
#     save_total_limit=2,
#     lr_scheduler_type='linear'
# )

# # Initialize Trainer
# trainer = Trainer(
#     model=model,
#     args=training_args,
#     train_dataset=train_dataset,
#     eval_dataset=val_dataset,
#     compute_metrics=compute_metrics
# )

# # Train the model
# trainer.train()

# test_results = trainer.evaluate(val_dataset)
# print(test_results)

# torch.save(model.state_dict(), './hybrid_nli_model.pth')
# print("Model saved successfully!")


# # Constants
# MODEL_NAME = 'google/electra-base-discriminator'
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# # Load tokenizer and model
# tokenizer = ElectraTokenizer.from_pretrained(MODEL_NAME)
# electra_model = ElectraModel.from_pretrained(MODEL_NAME).to(device)

# class NLI_Dataset(torch.utils.data.Dataset):
#     def __init__(self, encodings, labels):
#         self.encodings = encodings
#         self.labels = labels

#     def __getitem__(self, idx):
#         item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
#         item['labels'] = torch.tensor(self.labels[idx])
#         return item

#     def __len__(self):
#         return len(self.labels)

# # Load data and prepare dataset
# df = pd.read_csv('/content/drive/MyDrive/NLU/training_data/NLI/train.csv')
# train_df, val_df = train_test_split(df, test_size=0.1)

# # Tokenization
# train_encodings = tokenizer(train_df['premise'].tolist(), train_df['hypothesis'].tolist(), truncation=True, padding=True)
# val_encodings = tokenizer(val_df['premise'].tolist(), val_df['hypothesis'].tolist(), truncation=True, padding=True)

# # Dataset preparation
# train_dataset = NLI_Dataset(train_encodings, train_df['label'].tolist())
# val_dataset = NLI_Dataset(val_encodings, val_df['label'].tolist())

# # Define model
# class ElectraForNLIWithGNN(torch.nn.Module):
#     def __init__(self):
#         super().__init__()
#         self.electra = ElectraModel.from_pretrained(MODEL_NAME).to(device)
#         self.gnn = GCNConv(768, 768)  # Example GNN layer
#         self.classifier = torch.nn.Linear(768, 2)

#     def forward(self, input_ids, attention_mask, edge_index, batch_index, labels=None):
#         # Encoder part
#         outputs = self.electra(input_ids=input_ids, attention_mask=attention_mask)
#         sequence_output = outputs.last_hidden_state

#         # GNN part (simplified example)
#         gnn_output = F.relu(self.gnn(sequence_output, edge_index))
#         gnn_output = global_mean_pool(gnn_output, batch_index)  # Pooling over the graph
        
#         # Combine ELECTRA and GNN outputs
#         combined_output = sequence_output[:, 0, :] + gnn_output

#         # Classifier
#         logits = self.classifier(combined_output)
        
#         if labels is not None:
#             loss_fct = torch.nn.CrossEntropyLoss()
#             loss = loss_fct(logits.view(-1, 2), labels.view(-1))
#             return loss, logits
#         return logits

# model = ElectraForNLI().to(device)


# # Metric for evaluation
# metric = load_metric("accuracy")

# def compute_metrics(eval_pred):
#     logits, labels = eval_pred
#     predictions = np.argmax(logits, axis=-1)
#     return metric.compute(predictions=predictions, references=labels)


# # Define training arguments
# training_args = TrainingArguments(
#     output_dir='/content/drive/MyDrive/NLU/results',          # output directory
#     num_train_epochs=1,              # number of training epochs
#     per_device_train_batch_size=16,   # batch size for training
#     per_device_eval_batch_size=64,   # batch size for evaluation
#     warmup_steps=500,                # number of warmup steps for learning rate scheduler
#     weight_decay=0.01,               # strength of weight decay
#     logging_dir='/content/drive/MyDrive/NLU/logs',            # directory for storing logs
#     logging_strategy="epoch",
#     evaluation_strategy="epoch",
#     learning_rate=3e-5,
#     max_grad_norm=1.0,
#     load_best_model_at_end=True,
#     metric_for_best_model="accuracy",
#     save_strategy="epoch",
#     save_total_limit=2,
#     lr_scheduler_type='linear'
# )

# # Initialize Trainer
# trainer = Trainer(
#     model=model,
#     args=training_args,
#     train_dataset=train_dataset,
#     eval_dataset=val_dataset,
#     compute_metrics=compute_metrics 
# )

# # Train the model
# trainer.train()

# test_results = trainer.evaluate(val_dataset)
# print(test_results)

# torch.save(model.state_dict(), '/content/drive/MyDrive/NLU/hybrid_nli_model.pth')
# print("Model saved successfully!")