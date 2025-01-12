from string import punctuation
import pandas as pd
import numpy as np
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk import Text
from nltk import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split , cross_val_score
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

# **************************         MAIN        ********************************************
df = pd.read_csv('amazon_review.csv')

# Cleaning and encoding overall col to 0/1 (label Y which is the pre-defined sentiment score) for training 
df['overall'] = pd.to_numeric(df['overall'], errors='coerce')
df.dropna(subset=['overall'], inplace=True)
df['sentiment'] = np.where(df['overall'] > 3, 1, 0)

def preprocess_text(text):
    tokens = word_tokenize(str(text).lower())
    filtered_tokens = [lemmatizer.lemmatize(re.sub('[^a-zA-Z]', ' ', token)) for token in tokens if token not in stop_words]
    processed_text = ' '.join(filtered_tokens)
    return processed_text

# Preprocess the reviewText column 
df['rev'] = df['reviewText'].apply(preprocess_text)

# Vectorize the input X for training using " bag  of words' method
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(df['rev'])

# y is the output label for the learning set
y = df['sentiment']

#fitting the input to train via bayes model
bayes_classifier = MultinomialNB()
bayes_classifier.fit(X, y)

print("TRAINING SCORE ::: ",bayes_classifier.score(X,y))


# **********************      Testing the model       *********************************************

#Taking entire summary column as test input so vectorising it first 
df['summary_preprocessed'] = df['summary'].apply(preprocess_text)
X_test = vectorizer.transform(df['summary_preprocessed'])

# Predict sentiment based on the summary column using the trained model
df['Resultant_sentiment'] = bayes_classifier.predict(X_test)

#  ********************************************* *********************************************
report = classification_report(df['Resultant_sentiment'], y, output_dict=True)
accuracy = report['accuracy']
print(" TestAccuracy :::", accuracy)

df['Resultant_sentiment'] = np.where(df['Resultant_sentiment']==1, 'POSITIVE', 'NEGATIVE')
result_df = df[['summary', 'Resultant_sentiment']]
result_df.to_excel('sentiment_results_bayes-1.xlsx', index=False)

#accuracy :: 92.7%