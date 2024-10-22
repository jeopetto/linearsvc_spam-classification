import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import re
from sklearn.model_selection import train_test_split
import autocorrect
from autocorrect import Speller

# PRÉ-PROCESSAMENTO DO DATASET
# Ler dataset
theData = pd.read_csv ("data.csv", sep=',', header=None, names=['label','message'])

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

ham = theData[theData['label'] == 'ham']
spam = theData[theData['label'] == 'spam']

'''
# Printa o dataset
print(theData)
print("\nHam: ")
print(ham)
print("\nspam:")
print(spam)
'''

# Limpeza dos textos do dataset
theData = theData.lower() # Deixa as letras minúsculas
theData = re.sub(r'[^\w\s]', '',theData) # Remove pontuações e caracteres especiais
theData = re.sub(r'\d', '',theData) # Remove números

# Tokenização do dataset
theData = word_tokenize(theData)

# Normalização do dataset
spell = Speller (lang='en')
theData = spell(theData)

# Eliminar stopwords do dataset
stopwords = nltk.corpus.stopwords.words('english')
theData = [x for x in word_tokenize(theData) if x not in stopwords]

# Realizar stemmerização (radicalização)
stemmer = PorterStemmer()
theData['message'] = theData['message'].apply(lambda x: ' '.join(stemmer.stem(word) for word in x.split() ) )

# Atribuir números às etiquetas (0 para ham, 1 para spam)
theData['label'] = theData['label'].map({'ham': 0, 'spam': 1})


# DIVISÃO DO DATASET EM: CONJUNTO DE TREINO E CONJUNTO DE AVALIAÇão
x = theData['message']
y = theData['label']
x_train, x_test, y_train, y_test = train_test_split(theData['message'], theData['label'], test_size = 0.3)
'''
X_train: conjunto de treino (mensagens)
y_train: conjunto de treino (etiquetas)
x_test: conjunto de avaliação (mensagens)
y_test: conjunto de avaliação (etiquetas)
'''