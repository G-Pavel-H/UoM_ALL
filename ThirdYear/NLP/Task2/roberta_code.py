import torch
from torch.utils.data import Dataset, DataLoader
from transformers import RobertaTokenizer, RobertaForSequenceClassification, AdamW
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import pandas as pd

# Load the data
df = pd.read_csv("your_dataset.csv")

# Split the data into training and validation sets
train_df, val_df = train_test_split(df, test_size=0.1, random_state=42)

# Define a custom dataset
class MovieDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_len=512):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_len = max_len

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        text = str(self.texts[idx])
        labels = torch.tensor(self.labels[idx], dtype=torch.float32)

        encoding = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            max_length=self.max_len,
            padding="max_length",
        )

        return {
            "input_ids": encoding["input_ids"].flatten(),
            "attention_mask": encoding["attention_mask"].flatten(),
            "labels": labels,
        }

# Tokenizer and Model
tokenizer = RobertaTokenizer.from_pretrained("roberta-base")
model = RobertaForSequenceClassification.from_pretrained(
    "roberta-base", num_labels=len(df.columns[3:])
)

# Create datasets and dataloaders
train_dataset = MovieDataset(
    texts=train_df["plot_synopsis"].values,
    labels=train_df.iloc[:, 3:].values,
    tokenizer=tokenizer,
)

val_dataset = MovieDataset(
    texts=val_df["plot_synopsis"].values,
    labels=val_df.iloc[:, 3:].values,
    tokenizer=tokenizer,
)

train_dataloader = DataLoader(train_dataset, batch_size=8, shuffle=True)
val_dataloader = DataLoader(val_dataset, batch_size=8, shuffle=False)

# Training
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
optimizer = AdamW(model.parameters(), lr=2e-5)

for epoch in range(3):  # Adjust the number of epochs as needed
    model.train()
    for batch in train_dataloader:
        inputs = {
            "input_ids": batch["input_ids"].to(device),
            "attention_mask": batch["attention_mask"].to(device),
            "labels": batch["labels"].to(device),
        }

        optimizer.zero_grad()
        outputs = model(**inputs)
        loss = outputs.loss
        loss.backward()
        optimizer.step()

# Evaluation
model.eval()
all_preds = []
all_labels = []

with torch.no_grad():
    for batch in val_dataloader:
        inputs = {
            "input_ids": batch["input_ids"].to(device),
            "attention_mask": batch["attention_mask"].to(device),
        }

        outputs = model(**inputs)
        preds = torch.sigmoid(outputs.logits)
        all_preds.extend(preds.cpu().numpy())
        all_labels.extend(batch["labels"].cpu().numpy())

# Convert predictions to binary
all_preds_binary = (np.array(all_preds) > 0.5).astype(int)

# Print classification report
target_names = df.columns[3:]
print(classification_report(all_labels, all_preds_binary, target_names=target_names))
