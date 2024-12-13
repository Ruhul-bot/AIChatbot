import nltk
import random
import json
import pickle
import numpy as np
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Download necessary NLTK resources
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')

class CollegeChatbot:
    def __init__(self):
        # Lemmatizer for word processing
        self.lemmatizer = WordNetLemmatizer()
        
        # Load intents
        with open('chat_app/intents.json', 'r') as file:
            self.intents = json.load(file)
        
        # Load preprocessed data
        self.words = pickle.load(open('chat_app/words.pkl', 'rb'))
        self.classes = pickle.load(open('chat_app/classes.pkl', 'rb'))
        
        # Load trained model
        self.model = load_model('chat_app/chatbot_model.h5')
        
        # TF-IDF Vectorizer for fallback responses
        self.vectorizer = TfidfVectorizer()
        
    def clean_text(self, sentence):
        # Tokenize and lemmatize
        sentence_words = nltk.word_tokenize(sentence.lower())
        # sentence_words = [self.lemmatizer.lemmatize(word) for word word in sentence_words]
        sentence_words = [self.lemmatizer.lemmatize(word) for word in sentence_words]
        return sentence_words
    
    def bow_transformation(self, sentence):
        # Bag of words transformation
        sentence_words = self.clean_text(sentence)
        bag = [1 if word in sentence_words else 0 for word in self.words]
        return np.array(bag)
    
    def predict_class(self, sentence):
        # Predict intent
        bow = self.bow_transformation(sentence)
        res = self.model.predict(np.array([bow]))[0]
        ERROR_THRESHOLD = 0.25
        results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
        
        results.sort(key=lambda x: x[1], reverse=True)
        return_list = []
        for r in results:
            return_list.append({
                'intent': self.classes[r[0]],
                'probability': str(r[1])
            })
        return return_list
    
    def get_response(self, intents_list, intents_json):
        # Get response based on predicted intent
        tag = intents_list[0]['intent']
        for intent in intents_json['intents']:
            if intent['tag'] == tag:
                return random.choice(intent['responses'])
        return "I'm not sure how to respond to that."
    
    def fallback_response(self, query, corpus):
        # Fallback mechanism using cosine similarity
        corpus.append(query)
        tfidf_matrix = self.vectorizer.fit_transform(corpus)
        cosine_sim = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])
        most_similar_idx = cosine_sim[0].argmax()
        return corpus[most_similar_idx]