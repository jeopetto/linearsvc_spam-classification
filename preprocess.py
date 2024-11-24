# Importar bibliotecas necessárias
import pandas as pd
import re
import nltk
nltk.download('stopwords')
nltk.download('punkt_tab')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer

# Definir função de pré-processamento
def preprocess_dataset(df, language):

    # Configurar stemmer e stopwords para o idioma
    stemmer = SnowballStemmer(language)
    stop_words = set(stopwords.words(language))

    def preprocess_text(text):
        # Converter para letras minúsculas
        text = text.lower()
        # Remover caracteres especiais não relevantes
        text = re.sub(r'[^\w\s@$!%#?&/\\]', '', text)
        # Tokenizar o texto
        tokens = word_tokenize(text)
        # Remover stopwords
        tokens = [word for word in tokens if word not in stop_words]
        # Aplicar stemmização
        tokens = [stemmer.stem(word) for word in tokens]
        # Reconstruir o texto processado
        return ' '.join(tokens)

    # Aplicar a função de pré-processamento no dataset
    df['processed_text'] = df['message'].apply(preprocess_text)
    return df

# Carregar os três datasets
portuguese_df = pd.read_csv('dataset_pt.csv')
english_df = pd.read_csv('dataset_en.csv')
spanish_df = pd.read_csv('dataset_es.csv')

# Exibir as primeiras linhas de cada dataset
print(portuguese_df.head())
print(english_df.head())
print(spanish_df.head())

# Pré-processar cada dataset separadamente
portuguese_df = preprocess_dataset(portuguese_df, 'portuguese')
english_df = preprocess_dataset(english_df, 'english')
spanish_df = preprocess_dataset(spanish_df, 'spanish')

# Adicionar uma coluna indicando o idioma
portuguese_df['language'] = 'portuguese'
english_df['language'] = 'english'
spanish_df['language'] = 'spanish'

# Concatenar os datasets pré-processados
final_df = pd.concat([portuguese_df, english_df, spanish_df], ignore_index=True)

# Exibir as primeiras linhas do dataset
print(final_df.head())

# Salvar o dataset final em um arquivo CSV
final_df.to_csv('preprocessed_dataset.csv', index=False)
print("Dataset final salvo como 'preprocessed_dataset.csv'.")