import base64
import time
import os
from google.oauth2.credentials import Credentials
import numpy as np
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import joblib
from email import message_from_bytes
from bs4 import BeautifulSoup
import logging

# Configuração de caminhos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'spam_classifier_model.joblib')
VECTORIZER_PATH = os.path.join(BASE_DIR, 'vectorizer.joblib')
CREDENTIALS_PATH = os.path.join(BASE_DIR, 'path', 'to', 'credentials.json')  

# Configuração de logging com caminho absoluto
LOG_PATH = os.path.join(BASE_DIR, 'spam_classifier.log')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_PATH),
        logging.StreamHandler()
    ]
)

class GmailSpamClassifier:
    def __init__(self, credentials_path=CREDENTIALS_PATH, 
                 model_path=MODEL_PATH, 
                 vectorizer_path=VECTORIZER_PATH):
        self.SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
        self.credentials_path = credentials_path
        
        # Verificação da existência de arquivos
        self._verify_files_exist(credentials_path, model_path, vectorizer_path)
        
        # Carregar modelo e vectorizer
        try:
            logging.info(f"Tentando carregar modelo de: {model_path}")
            self.model = joblib.load(model_path)
            logging.info(f"Tentando carregar vectorizer de: {vectorizer_path}")
            self.vectorizer = joblib.load(vectorizer_path)
            logging.info("Modelo e vectorizer carregados com sucesso")
        except Exception as e:
            logging.error(f"Erro ao carregar modelo ou vectorizer: {e}")
            raise

        # Autenticação com o Gmail
        try:
            self.service = self._authenticate()
            logging.info("Autenticação com Gmail realizada com sucesso")
        except Exception as e:
            logging.error(f"Erro na autenticação com Gmail: {e}")
            raise

        self.known_emails = set()

    def _verify_files_exist(self, credentials_path, model_path, vectorizer_path):
        """Verifica se todos os arquivos necessários existem"""
        files_to_check = {
            'Credenciais': credentials_path,
            'Modelo': model_path,
            'Vectorizer': vectorizer_path
        }
        
        missing_files = []
        for file_name, file_path in files_to_check.items():
            if not os.path.exists(file_path):
                missing_files.append(f"{file_name} ({file_path})")
        
        if missing_files:
            error_msg = "Arquivos não encontrados:\n" + "\n".join(missing_files)
            logging.error(error_msg)
            raise FileNotFoundError(error_msg)

    def _authenticate(self):
        # Realiza a autenticação com a API do Gmail
        try:
            flow = InstalledAppFlow.from_client_secrets_file(
                self.credentials_path, 
                self.SCOPES
            )
            creds = flow.run_local_server(port=0)
            return build('gmail', 'v1', credentials=creds)
        except Exception as e:
            logging.error(f"Erro durante a autenticação: {e}")
            raise

    def _extract_email_content(self, msg):
        # Extrai e combina diferentes partes do email"
        headers = msg.get('payload', {}).get('headers', [])
        subject = next((header['value'] for header in headers if header['name'].lower() == 'subject'), '')
        sender = next((header['value'] for header in headers if header['name'].lower() == 'from'), '')
        
        body = self._get_email_body(msg.get('payload', {}))
        
        full_content = f"{subject} {sender} {body}"
        return self._preprocess_email_content(full_content)

    def _get_email_body(self, payload):
        # Extrai o corpo do email recursivamente
        if 'body' in payload and 'data' in payload['body']:
            return base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8', errors='ignore')
        
        if 'parts' in payload:
            text_parts = []
            for part in payload['parts']:
                if part['mimeType'].startswith('text/'):
                    if 'data' in part['body']:
                        text_parts.append(base64.urlsafe_b64decode(part['body']['data']).decode('utf-8', errors='ignore'))
                elif 'parts' in part:
                    text_parts.append(self._get_email_body(part))
            return ' '.join(text_parts)
        
        return ''

    def _preprocess_email_content(self, content):
        # Pré-processamento do conteúdo do email
        if not content:
            return ""
        soup = BeautifulSoup(content, 'html.parser')
        text = soup.get_text()
        return text.lower().strip()

    def classify_email(self, email_content):
        # Classifica um email usando o modelo treinado
        try:
            content_vectorized = self.vectorizer.transform([email_content])
            prediction = self.model.predict(content_vectorized)[0]
            
            # Usa decision_function para obter a distância do hiperplano
            confidence_score = abs(self.model.decision_function(content_vectorized)[0])
            # Normaliza o score para algo entre 0 e 1 usando sigmoid
            confidence = 1 / (1 + np.exp(-confidence_score))
            
            return prediction, confidence
            
        except Exception as e:
            logging.error(f"Erro na classificação: {e}")
            return 'erro', 0.0

    def get_initial_unread_emails(self):
        # Obtém a lista inicial de emails não lidos
        try:
            results = self.service.users().messages().list(
                userId='me', 
                labelIds=['INBOX'], 
                q='is:unread'
            ).execute()
            
            self.known_emails = set(msg['id'] for msg in results.get('messages', []))
            logging.info(f"Identificados {len(self.known_emails)} emails não lidos iniciais")
        except Exception as e:
            logging.error(f"Erro ao obter emails iniciais: {e}")
            self.known_emails = set()

    def process_new_emails(self):
        # Processa novos emails não lidos
        try:
            results = self.service.users().messages().list(
                userId='me',
                labelIds=['INBOX'],
                q='is:unread'
            ).execute()
            
            messages = results.get('messages', [])
            if not messages:
                logging.info("Nenhum novo email encontrado")
                return
            
            for message in messages:
                if message['id'] in self.known_emails:
                    continue

                msg = self.service.users().messages().get(userId='me', id=message['id']).execute()
                self.known_emails.add(message['id'])

                email_content = self._extract_email_content(msg)
                prediction, confidence = self.classify_email(email_content)

                headers = msg.get('payload', {}).get('headers', [])
                subject = next((h['value'] for h in headers if h['name'].lower() == 'subject'), 'Sem Assunto')
                sender = next((h['value'] for h in headers if h['name'].lower() == 'from'), 'Remetente Desconhecido')



                logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Exibe os detalhes do e-mail no terminal de forma organizada
                logging.info("\n" + "="*50)
                logging.info(" Novo e-mail processado ")
                logging.info("="*50)
                logging.info(f"ID: {message['id']}")
                logging.info(f"De: {sender}")
                logging.info(f"Assunto: {subject}")
                logging.info(f"Corpo da mensagem:\n{email_content}\n")
                logging.info(f"Classificação: {prediction}")
                logging.info(f"Confiança: {confidence:.2%}")
                logging.info("="*50 + "\n")


        except Exception as e:
            logging.error(f"Erro ao processar novos emails: {e}")

    def run(self, check_interval=10):
        # Executa o monitoramento contínuo
        self.get_initial_unread_emails()
        logging.info("Iniciando monitoramento de emails...")
        
        try:
            while True:
                self.process_new_emails()
                time.sleep(check_interval)
        except KeyboardInterrupt:
            logging.info("Monitoramento interrompido pelo usuário")
        except Exception as e:
            logging.error(f"Erro durante o monitoramento: {e}")

if __name__ == "__main__":
    try:
        print("Iniciando classificador de spam...")
        print(f"Diretório base: {BASE_DIR}")
        print(f"Arquivo de credenciais: {CREDENTIALS_PATH}")
        
        classifier = GmailSpamClassifier()
        classifier.run()
    except FileNotFoundError as e:
        print("\nErro: Arquivos necessários não encontrados!")
        print(str(e))
    except Exception as e:
        print(f"\nErro inesperado: {e}")