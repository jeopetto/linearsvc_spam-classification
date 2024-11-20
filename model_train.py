import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib

# Carregar dados pré-processados
data = pd.read_csv('preprocessed_dataset.csv')

# Separar features (X) e target (y)
X = data['processed_text']
y = data['label']

# Converter texto em features numéricas usando TF-IDF
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(X)

# Dividir em conjuntos de treino e teste (Proporção 80:20)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42)

# Criar e treinar o modelo SVM
svm = LinearSVC(random_state=42)
svm.fit(X_train, y_train)

# Fazer predições
y_pred = svm.predict(X_test)

# Avaliar o modelo
print("\nRelatório de Classificação:")
print(classification_report(y_test, y_pred))

# Salvar o modelo treinado e o vectorizer
joblib.dump(svm, 'spam_classifier_model.joblib')
joblib.dump(vectorizer, 'vectorizer.joblib')