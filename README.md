# Classificação de E-mails como Spam ou Não-Spam usando LinearSVC

Este projeto implementa um sistema de classificação de e-mails baseado no algoritmo de Machine Learning **LinearSVC** uma versão mais otimizada e focada em problemas lineares do **Support Vector Machine (SVM)**. Ele processa mensagens em tempo real e as classifica como spam ou não-spam, integrando-se à **API do Gmail**. O modelo foi projetado para operar em inglês, português e espanhol e utiliza técnicas de pré-processamento de texto.

---

## 📋 Funcionalidades

- Classificação de e-mails em **tempo real**.
- Integração com a **API do Gmail** para coleta e processamento de mensagens.
- Suporte a datasets multilíngues com pré-processamento automático.
- Alta performance com métricas de:
  - **Precisão**: 0.99
  - **Recall**: 0.96 para spam.
  - **F1-score**: 0.98 para spam.

---

## 🛠️ Tecnologias Utilizadas

- **Linguagem de programação**: Python
- **Bibliotecas**:
  - `scikit-learn` (implementação do SVM e GridSearch)
  - `NLTK` (tokenização, stemming, remoção de stopwords)
  - `pandas` (manipulação de dados)
  - **API do Gmail** para integração
- **Técnicas**:
  - Vetorização de texto com **TF-IDF**

---

## 📦 Estrutura do Projeto

```plaintext
├── data/                # Datasets utilizados
├── src/                 # Código-fonte
│   ├── preprocess.py    # Funções de pré-processamento
│   ├── model_train.py   # Treinamento do modelo
│   ├── results          # Resultados e métricas do modelo treinado
│   └── vetorização e salvaemnto do modelo treinado
├── gmail_implementation.py         # Integração do modelo treinado e vetorizado com a API do Gmail
├── README.md            # Documentação do projeto
└── requirements.txt     # Dependências do Python
