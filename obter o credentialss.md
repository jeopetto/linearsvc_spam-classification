# Passos para obter o credentials.json

## 1. Acesse a Google Cloud Console
- Vá para o [Google Cloud Console](https://console.cloud.google.com/).
- Faça login com a sua conta do Google.

## 2. Crie um novo projeto
- No menu superior, clique em "Selecionar um Projeto" e, em seguida, em "Novo Projeto".
- Dê um nome ao seu projeto, como "Spam Detection", e clique em "Criar".

## 3. Habilite a API que você precisa
- Após criar o projeto, vá para "Biblioteca de APIs" no menu lateral.
- Pesquise a API desejada (ex.: Gmail API) e clique em "Ativar".

## 4. Configure a tela de consentimento OAuth
- No menu lateral, vá para "APIs e Serviços" > "Tela de Consentimento OAuth".
- Escolha o tipo de usuário:
  - **Interno** (se for apenas para sua conta ou organização).
  - **Externo** (se for para usuários públicos).
- Preencha os campos obrigatórios:
  - Nome do aplicativo.
  - E-mail de suporte.
- Salve as alterações.

## 5. Crie credenciais de cliente OAuth
- Vá para "APIs e Serviços" > "Credenciais".
- Clique em "Criar Credenciais" > "ID do Cliente OAuth".
- Escolha o tipo de aplicação:
  - **Aplicativo da Web**: para apps hospedados em servidores ou frameworks web.
  - **Aplicativo Instalado**: para aplicativos de desktop, CLI ou localhost.
- Configure os URIs de redirecionamento autorizados:
  - Adicione `http://localhost` (para desenvolvimento local).
- Clique em "Criar".

## 6. Baixe o arquivo credentials.json
- Após criar as credenciais, você verá a opção de Baixar JSON.
- Salve o arquivo como `credentials.json` no diretório do seu projeto.