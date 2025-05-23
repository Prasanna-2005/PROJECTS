from string import punctuation
import pandas as pd
import numpy as np
# from sklearn.model_selection import train_test_split
pd.set_option('display.min_rows', 300)

# *********************************************************************************************************
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import Text

lemmatizer = WordNetLemmatizer()
Freq = FreqDist()
sent_analyzer = SentimentIntensityAnalyzer()

stop_words = set(stopwords.words('english'))
helpword = set(["a","a's","able","about","this","above","according","accordingly","across","actually","after","afterwards","again","against","ain't","all","allow","allows","almost","alone","along","already","also","although","always","am","among","amongst","an","and","another","any","anybody","anyhow","anyone","anything","anyway","anyways","anywhere","apart","appear","appreciate","appropriate","are","aren't","around","as","aside","ask","asking","associated","at","available","away","awfully","b","be","became","because","become","becomes","becoming","been","before","beforehand","behind","being","believe","below","beside","besides","best","better","between","beyond","both","brief","but","by","c","c'mon","c's","came","can","can't","cannot","cant","cause","causes","certain","certainly","changes","clearly","co","com","come","comes","concerning","consequently","consider","considering","contain","containing","contains","corresponding","could","couldn't","course","currently","d","definitely","described","despite","did","didn't","different","do","does","doesn't","doing","don't","done","down","downwards","during","e","each","edu","eg","eight","either","else","elsewhere","enough","entirely","especially","et","etc","even","ever","every","everybody","everyone","everything","everywhere","ex","exactly","example","except","f","far","few","fifth","first","five","followed","following","follows","for","former","formerly","forth","four","from","further","furthermore","g","get","gets","getting","given","gives","go","goes","going","gone","got","gotten","greetings","h","had","hadn't","happens","hardly","has","hasn't","have","haven't","having","he","he's","hello","help","hence","her","here","here's","hereafter","hereby","herein","hereupon","hers","herself","hi","him","himself","his","hither","hopefully","how","howbeit","however","i","i'd","i'll","i'm","i've","ie","if","ignored","immediate","in","inasmuch","inc","indeed","indicate","indicated","indicates","inner","insofar","instead","into","inward","is","isn't","it","it'd","it'll","it's","its","itself","j","just","k","keep","keeps","kept","know","known","knows","l","last","lately","later","latter","latterly","least","less","lest","let","let's","like","liked","likely","little","look","looking","looks","ltd","m","mainly","many","may","maybe","me","mean","meanwhile","merely","might","more","moreover","most","mostly","much","must","my","myself","n","name","namely","nd","near","nearly","necessary","need","needs","neither","never","nevertheless","new","next","nine","no","nobody","non","none","noone","nor","normally","not","nothing","novel","now","nowhere","o","obviously","of","off","often","oh","ok","okay","old","on","once","one","ones","only","onto","or","other","others","otherwise","ought","our","ours","ourselves","out","outside","over","overall","own","p","particular","particularly","per","perhaps","placed","please","plus","possible","presumably","probably","provides","q","que","quite","qv","r","rather","rd","re","really","reasonably","regarding","regardless","regards","relatively","respectively","right","s","said","same","saw","say","saying","says","second","secondly","see","seeing","seem","seemed","seeming","seems","seen","self","selves","sensible","sent","serious","seriously","seven","several","shall","she","should","shouldn't","since","six","so","some","somebody","somehow","someone","something","sometime","sometimes","somewhat","somewhere","soon","sorry","specified","specify","specifying","still","sub","such","sup","sure","t","t's","take","taken","tell","tends","th","than","thank","thanks","thanx","that","that's","thats","the","their","theirs","them","themselves","then","thence","there","there's","thereafter","thereby","therefore","therein","theres","thereupon","these","they","they'd","they'll","they're","they've","think","third","this","thorough","thoroughly","those","though","three","through","throughout","thru","thus","to","together","too","took","toward","towards","tried","tries","truly","try","trying","twice","two","u","un","under","unfortunately","unless","unlikely","until","unto","up","upon","us","use","used","useful","uses","using","usually","uucp","v","value","various","very","via","viz","vs","w","want","wants","was","wasn't","way","we","we'd","we'll","we're","we've","welcome","well","went","were","weren't","what","what's","whatever","when","whence","whenever","where","where's","whereafter","whereas","whereby","wherein","whereupon","wherever","whether","which","while","whither","who","who's","whoever","whole","whom","whose","why","will","willing","wish","with","within","without","won't","wonder","would","wouldn't","x","y","yes","yet","you","you'd","you'll","you're","you've","your","yours","yourself","yourselves","z","zero"])
stop_words = stop_words.union(set(punctuation),helpword)
# *************************************************************************************************************

df = pd.read_csv('amazon_review.csv')

df['overall'] = pd.to_numeric(df['overall'],errors='coerce')
df.dropna(subset=['overall'])
df['positive'] = np.where(df['overall']>3,1,0)  # creating a 2 way rating header 1-> +ve rating   0->-ve rating


def preprocess_text(text):
        # Tokenize the text
        tokens = word_tokenize(str(text).lower())
        
        # Remove stop words
        filtered_tokens = [token for token in tokens if token not in stop_words]
        for word in filtered_tokens:
            if(len(word) > 4):
                Freq[word]+=1
                
        processed_text = ' '.join(filtered_tokens)

        return processed_text

df['newReviewText'] = df['reviewText'].apply(preprocess_text) # pre - processing the review_text column
top_25_words = Freq.most_common(25)

print('-----TOP 25 FREQUENTLY USED WORDS -----')
print(f"{'S.NO'.ljust(5)}  {"WORD".ljust(15)} \t {'FREQUENCY'}")
print('----------------------------------------')
for index , val in enumerate(Freq.most_common(25)):
    print(f"{str(index+1).ljust(5)}  {str(val[0]).ljust(15)} \t {val[1]}")

# *****************************************************************************************

all_reviews = ' '.join(df['reviewText'].astype(str))
tokens = word_tokenize(all_reviews)
text = Text(tokens)

# Analyzing sentiment for the top 25 words 
sentList = []
for word,freq in top_25_words:
 
    concordance_list = text.concordance_list(word, width=30,lines=freq)
    
    
    sent = {'neg': 0, 'neu': 0, 'pos': 0, 'compound': 0}  # To store cumulative sentiment values
    
    for entry in concordance_list:
        context = ' '.join(entry.left + [word] + entry.right)       
        sentiment = sent_analyzer.polarity_scores(context)
     
        sent['neg'] += sentiment['neg']
        sent['neu'] += sentiment['neu']
        sent['pos'] += sentiment['pos']
        sent['compound'] += sentiment['compound']

    
    
    # Calculate the average sentiment scores 
    num_lines = len(concordance_list)
    
    if num_lines > 0:
        avg_sent = {key: sent[key] / num_lines for key in sent}  # Average for each sentiment score
    else:
        avg_sent = {'neg': 0, 'neu': 0, 'pos': 0, 'compound': 0}  # Handle edge case where no concordance is found
    
    overall_sentiment=''
    if avg_sent['compound'] > 0.05:
        overall_sentiment = "positive"
    elif avg_sent['compound'] < -0.05:
        overall_sentiment = "negative"
    else:
        overall_sentiment = "neutral"
    # Append the word and its average sentiment to sentList
    sentList.append((word, overall_sentiment))


# Print word -> sentiment score format
print('-----SENTIMENTAL ANALYSIS-----')
print(f"{"WORD".ljust(10)}   {'SENTIMENT'.ljust(15)}")
print('-------------------------------')
for word, sentiment in sentList:
    print(f"{word.ljust(10)} ->  {sentiment.ljust(20)}")


