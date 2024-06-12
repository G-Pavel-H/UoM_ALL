import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report

# Load the dataset
df = pd.read_csv('path_to_your_file/AV_trial.csv')  # Make sure to replace 'path_to_your_file' with the actual file path

# Concatenate text_1 and text_2 for TF-IDF vectorization
df['text_combined'] = df['text_1'] + " " + df['text_2']

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(df['text_combined'], df['label'], test_size=0.2, random_state=42)

# Define a pipeline with TF-IDF Vectorization and SVM Classifier
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(stop_words='english')),
    ('svm', SVC(kernel='linear', probability=True))
])

# Train the model on the training data
pipeline.fit(X_train, y_train)

# Make predictions on the test set
y_pred = pipeline.predict(X_test)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)

# Generate a classification report
report = classification_report(y_test, y_pred)

print(f'Accuracy: {accuracy}')
print('Classification Report:')
print(report)


#--------------------------------------------

from transformers import RobertaTokenizer, RobertaForSequenceClassification, Trainer, TrainingArguments
import torch
from torch.utils.data import Dataset
import pandas as pd
from sklearn.model_selection import train_test_split

# Assuming df is your DataFrame after loading the dataset
df = pd.read_csv('path_to_your_file/AV_trial.csv')  # Update the path accordingly

class AuthorshipDataset(Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)

# Load the tokenizer
tokenizer = RobertaTokenizer.from_pretrained('roberta-base')

# Tokenize the input texts
texts = df['text_1'] + tokenizer.sep_token + df['text_2']  # Use RoBERTa's separator token
labels = df['label'].tolist()
encodings = tokenizer(texts.tolist(), truncation=True, padding=True, max_length=512)

# Split the data into training and validation sets
train_encodings, val_encodings, train_labels, val_labels = train_test_split(encodings, labels, test_size=0.1)

# Create dataset objects
train_dataset = AuthorshipDataset(train_encodings, train_labels)
val_dataset = AuthorshipDataset(val_encodings, val_labels)

# Define training arguments
training_args = TrainingArguments(
    output_dir='./results',          # directory to save model and logs
    num_train_epochs=3,              # total number of training epochs
    per_device_train_batch_size=8,   # batch size per device during training
    per_device_eval_batch_size=8,    # batch size for evaluation
    warmup_steps=500,                # number of warmup steps for learning rate scheduler
    weight_decay=0.01,               # strength of weight decay
    logging_dir='./logs',            # directory for storing logs
    logging_steps=10,
    evaluation_strategy="epoch",     # evaluate at the end of each epoch
)

# Load the RoBERTa model
model = RobertaForSequenceClassification.from_pretrained('roberta-base')

# Initialize the Trainer
trainer = Trainer(
    model=model,                         # the instantiated model to be trained
    args=training_args,                  # training arguments, defined above
    train_dataset=train_dataset,         # training dataset
    eval_dataset=val_dataset             # evaluation dataset
)

# Train the model
trainer.train()

# You can save the model with
# model.save_pretrained('./your_model_directory')
