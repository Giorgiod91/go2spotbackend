import imaplib
import os
import csv
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
from scipy.sparse import hstack
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import confusion_matrix, precision_recall_curve, roc_curve, auc
import joblib
import seaborn as sns
import matplotlib.pyplot as plt


data = []
csv_file = "locations.txt"



def train():
    df = pd.DataFrame({
        "vibe":  vibe,
        "budget": budget,
        "time": time,
        "groupsize": groupsize,
        "destination": destination,
        "location": location
    })

    #vectorize data
    vectorizer_vibe = TfidfVectorizer(stop_words="english")
    X_vibe = vectorizer_vibe.fit_transform(df["vibe"])

    vectorizer_budget = TfidfVectorizer(stop_words="english")
    X_budget = vectorizer_vibe.fit_transform(df["budget"])

    vectorizer_time = TfidfVectorizer(stop_words="english")
    X_time = vectorizer_vibe.fit_transform(df["time"])

    vectorizer_groupsize = TfidfVectorizer(stop_words="english")
    X_groupsize = vectorizer_vibe.fit_transform(df["groupsize"])

    vectorizer_destination = TfidfVectorizer(stop_words="english")
    X_destination = vectorizer_vibe.fit_transform(df["destination"])

    y = df["location"]

    X_train , X_test, y_train, y_test = train_test_split(X_time,X_budget,X_destination,X_groupsize,X_vibe ,y,test_size=0.2, random_state=42)


    model = LogisticRegression(C=0.1, class_weight='balanced')

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)


    
    print("Accuracy: ", accuracy_score(y_test, predictions))
    print("Classification Report:\n", classification_report(y_test, predictions))   