import pandas as pd
import os
import joblib
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report
from sklearn.feature_extraction.text import TfidfVectorizer
<<<<<<< HEAD
import joblib
import os
=======
>>>>>>> 899c4de1ac3ed8bb968e421c4331077a6a5558c2

# Carregar dados pré-processados
data = pd.read_csv('preprocessed_dataset.csv')

# Tratar valores ausentes na coluna de texto
data['processed_text'] = data['processed_text'].fillna('')

# Separar features (X) e target (y)
X = data['processed_text']
y = data['label']

# Converter texto em features numéricas usando TF-IDF
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(X)

# Configuração para GridSearch
param_grid = {'C': [0.01, 0.1, 1, 10, 100]}

# Dividir em conjuntos de treino e teste (Proporção 80:20)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Criar GridSearch com validação cruzada
svm = LinearSVC(random_state=42)
gridSearch = GridSearchCV(svm, param_grid, cv=5, scoring='accuracy', verbose = 2)
gridSearch.fit(X_train, y_train)

# Melhor modelo e parâmetros
print(f"Melhor parâmetro encontrado: {gridSearch.best_params_}")
print(f"Melhor precisão no treinamento: {gridSearch.best_score_}")

# Modelo otimizado
optimized_svm = gridSearch.best_estimator_

# Fazer predições com o modelo otimizado
y_pred = optimized_svm.predict(X_test)

# Avaliar o modelo
print("\nRelatório de Classificação do modelo:")
print(classification_report(y_test, y_pred))

# Definir caminhos para salvar os arquivos
MODEL_PATH = os.path.join(os.getcwd(), 'spam_classifier_model.joblib')
VECTORIZER_PATH = os.path.join(os.getcwd(), 'vectorizer.joblib')

# Salvar o modelo treinado e o vectorizer
try:
<<<<<<< HEAD
    joblib.dump(svm, MODEL_PATH)
=======
    joblib.dump(optimized_svm, MODEL_PATH)
>>>>>>> 899c4de1ac3ed8bb968e421c4331077a6a5558c2
    joblib.dump(vectorizer, VECTORIZER_PATH)
    print(f"Modelo salvo em: {MODEL_PATH}")
    print(f"Vectorizer salvo em: {VECTORIZER_PATH}")
except Exception as e:
<<<<<<< HEAD
    print(f"Erro ao salvar o modelo: {e}")
=======
    print(f"Erro ao salvar o modelo: {e}")
>>>>>>> 899c4de1ac3ed8bb968e421c4331077a6a5558c2
