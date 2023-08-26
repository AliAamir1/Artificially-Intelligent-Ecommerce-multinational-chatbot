from nltk.stem import WordNetLemmatizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import warnings
import string  # to process standard python strings
import random
import io
import nltk
from flask import Flask, request, jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app)


print("before")
warnings.filterwarnings('ignore')

# nltk.download('punkt') # first-time use only
# nltk.download('wordnet') # first-time use only

print("before")
f = open('chatbot.txt', 'r', errors='ignore')
raw = f.read()
raw = raw.lower()  # converts to lowercase
print("after")
sent_tokens = nltk.sent_tokenize(raw)  # converts to list of sentences
word_tokens = nltk.word_tokenize(raw)  # converts to list of words

lemmer = nltk.stem.WordNetLemmatizer()

lemmer = nltk.stem.WordNetLemmatizer()
# WordNet is a semantically-oriented dictionary of English included in NLTK.


def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]


remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)


def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))


GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up", "hey",)
GREETING_RESPONSES = ["hi", "hey", "*nods*", "hi there",
                      "hello", "I am glad! You are talking to me"]


def greeting(sentence):

    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)


def response(user_response):
    robo_response = ''
    sent_tokens.append(user_response)
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx = vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if (req_tfidf == 0):
        robo_response = robo_response+"I am sorry! I don't understand you"
        return robo_response
    else:
        robo_response = robo_response+sent_tokens[idx]
        return robo_response


@app.route('/chatbot', methods=['POST'])
def chatbot():
    data = request.json
    user_response = data['user_response']
    user_response = user_response.lower()
    if (user_response != 'bye'):
        if (user_response == 'thanks' or user_response == 'thank you'):
            return jsonify({'response': 'ROBO: You are welcome..'})
        else:
            if (greeting(user_response) != None):
                return jsonify({'response': 'ROBO: '+greeting(user_response)})
            else:
                robo_response = response(user_response)
                sent_tokens.remove(user_response)
                return jsonify({'response': 'ROBO: ' + robo_response})
    else:
        return jsonify({'response': 'ROBO: Bye! take care..'})


if __name__ == '__main__':
    app.run()
