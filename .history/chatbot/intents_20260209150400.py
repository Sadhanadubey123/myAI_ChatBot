from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

class IntentClassifier:
    def __init__(self):
        self.vectorizer = CountVectorizer()
        self.model = LogisticRegression()
        self.intents = ["provision", "status", "optimize"]

    def train(self, training_data):
        texts = [item["text"] for item in training_data]
        labels = [item["intent"] for item in training_data]
        X = self.vectorizer.fit_transform(texts)
        self.model.fit(X, labels)

    def predict(self, text):
        X = self.vectorizer.transform([text])
        return self.model.predict(X)[0]