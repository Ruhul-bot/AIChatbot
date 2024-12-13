import nltk
import numpy as np
import random
import json
import pickle

from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Download required NLTK resources
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('punkt_tab')
# Initialize lemmatizer
lemmatizer = WordNetLemmatizer()

# Load intents
with open('chat_app/intents.json', 'r') as file:
    intents = json.load(file)

# Prepare training data
words = []
classes = []
documents = []
ignore_chars = ['?', '!', '.', ',']

# Process intents
for intent in intents['intents']:
    for pattern in intent['patterns']:
        # Tokenize each word
        word_list = nltk.word_tokenize(pattern)
        words.extend(word_list)
        
        # Add documents for training
        documents.append((word_list, intent['tag']))
        
        # Add to classes if not already present
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

# Lemmatize and remove duplicates
words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_chars]
words = sorted(list(set(words)))
classes = sorted(list(set(classes)))

# Prepare training data
training = []
output_empty = [0] * len(classes)

for doc in documents:
    # Initialize bag of words
    bag = []
    
    # Lemmatize and process words
    word_patterns = doc[0]
    word_patterns = [lemmatizer.lemmatize(word.lower()) for word in word_patterns]
    
    # Create bag of words
    for w in words:
        bag.append(1) if w in word_patterns else bag.append(0)
    
    # Output row
    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1
    
    training.append([bag, output_row])

# Shuffle training data
random.shuffle(training)

# Separate features and labels
train_x = np.array([row[0] for row in training])
train_y = np.array([row[1] for row in training])

# Build neural network model
model = Sequential([
    Dense(128, input_shape=(len(train_x[0]),), activation='relu'),
    Dropout(0.5),
    Dense(64, activation='relu'),
    Dropout(0.5),
    Dense(len(train_y[0]), activation='softmax')
])

# Compile model
sgd = SGD(learning_rate=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

# Train model
model.fit(train_x, train_y, epochs=200, batch_size=5, verbose=1)

# Save model and preprocessing data
model.save('chat_app/chatbot_model.h5')
pickle.dump(words, open('chat_app/words.pkl', 'wb'))
pickle.dump(classes, open('chat_app/classes.pkl', 'wb'))

print("Model training completed successfully!")