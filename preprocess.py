import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import re
from autocorrect import Speller

# Ler dataset
theData = pd.read_csv("data.csv", sep=',', header=None, names=['label','message'])

# PRÉ-PROCESSAMENTO DO DATASET
# Limpeza dos textos
theData['message'] = theData['message'].str.lower()  # Deixa as letras minúsculas
theData['message'] = theData['message'].apply(lambda x: re.sub(r'[^\w\s]', '', x))  # Remove pontuações e caracteres especiais
theData['message'] = theData['message'].apply(lambda x: re.sub(r'\d', '', x))  # Remove números

# Tokenização
theData['message'] = theData['message'].apply(word_tokenize)

# Normalização do dataset
spell = Speller(lang='en')
theData['message'] = theData['message'].apply(spell)

# Eliminação de stopwords
stopwords = nltk.corpus.stopwords.words('english')
theData['message'] = theData['message'].apply(lambda x: ' '.join([word for word in x.split() if word not in stopwords]))

# Stemmerização (radicalização)
stemmer = PorterStemmer()
theData['message'] = theData['message'].apply(lambda x: ' '.join(stemmer.stem(word) for word in x.split()))

# Atribuição de números às etiquetas (0 para ham, 1 para spam)
theData['label'] = theData['label'].map({'ham': 0, 'spam': 1})

# Salvar os dados pré-processados
theData.to_csv('preprocessed_data.csv', index=False)