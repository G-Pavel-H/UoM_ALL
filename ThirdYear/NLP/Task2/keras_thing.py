import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import f1_score
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, Bidirectional, LSTM, Dense

# Load your dataset
df = pd.read_csv('movie_plots.csv')

# Data preprocessing
X = df['plot_synopsis'].values
y = df[['comedy', 'cult', 'flashback', 'historical', 'murder', 'revenge', 'romantic', 'scifi', 'violence']].values

# Tokenize and pad the input sequences
max_words = 10000  # Adjust as needed
max_len = 200  # Adjust as needed
tokenizer = Tokenizer(num_words=max_words)
tokenizer.fit_on_texts(X)
X_seq = tokenizer.texts_to_sequences(X)
X_pad = pad_sequences(X_seq, maxlen=max_len)

# Define cross-validation parameters
n_splits = 5  # Adjust as needed
skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)

# Iterate over folds
for fold, (train_index, test_index) in enumerate(skf.split(X_pad, np.argmax(y, axis=1))):
    X_train, X_val = X_pad[train_index], X_pad[test_index]
    y_train, y_val = y[train_index], y[test_index]

    # Build the model
    model = Sequential()
    model.add(Embedding(input_dim=max_words, output_dim=100, input_length=max_len))
    model.add(Bidirectional(LSTM(64)))
    model.add(Dense(9, activation='sigmoid'))
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    # Train the model
    epochs = 5  # Initial value, adjust as needed
    batch_size = 32  # Initial value, adjust as needed

    # Iterate over different epochs and batch sizes
    for epoch in [5, 10, 15]:
        for batch_size in [16, 32, 64]:
            model.fit(X_train, y_train, epochs=epoch, batch_size=batch_size, validation_data=(X_val, y_val), verbose=0)

            # Predict on validation set
            y_pred = model.predict(X_val)

            # Convert probabilities to binary predictions
            y_pred_binary = np.round(y_pred)

            # Calculate F1-score
            f1 = f1_score(y_val, y_pred_binary, average='micro')  # You can choose 'macro' or 'weighted' as well

            print(f'Fold {fold + 1}, Epochs: {epoch}, Batch Size: {batch_size}, F1-Score: {f1:.4f}')

# You can use this information to choose the best combination of epochs and batch size based on F1-score.
