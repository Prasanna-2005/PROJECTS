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
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

# **************************         MAIN        ********************************************
df = pd.read_csv('amazon_review.csv')

# Cleaning and encoding overall col to 0/1 (label Y which is the pre-defined sentiment score) for training 
df['overall'] = pd.to_numeric(df['overall'], errors='coerce')
df.dropna(subset=['overall'], inplace=True)
cond = [df['overall']>3,df['overall']==3,df['overall']<3]
vals= [1,0,-1]
df['sentiment'] = np.select(cond,vals)


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

#fitting the input to train via lg model
lg_classifier = LogisticRegression()
lg_classifier.fit(X, y)

print("TRAINING SCORE ::: ",lg_classifier.score(X,y))


# **********************      Testing the model       *********************************************

#Taking entire summary column as test input so vectorising it first 
df['summary_preprocessed'] = df['summary'].apply(preprocess_text)
X_test = vectorizer.transform(df['summary_preprocessed'])

# Predict sentiment based on the summary column using the trained model
df['Resultant_sentiment'] = lg_classifier.predict(X_test)

#  ******************************************************************************************
conditions = [
    df['Resultant_sentiment'] == 1,
    df['Resultant_sentiment'] == -1,
    df['Resultant_sentiment'] == 0
]
choices = ['Positive', 'Negative', 'Neutral']
df['Sentiment'] = np.select(conditions, choices,default='Unknown')


report = classification_report(df['Resultant_sentiment'], y, output_dict=True)
accuracy = report['accuracy']
print(" TestAccuracy :::", accuracy)

result_df = df[['summary', 'Sentiment']]
result_df.to_excel('sentiment_results_lg.xlsx', index=False)

#accuracy :: 91.00%