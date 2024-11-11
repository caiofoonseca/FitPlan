# Contribuindo para FitPlan
## Obrigado por considerar contribuir para o projeto FitPlan! Siga as etapas abaixo para configurar o ambiente de desenvolvimento e garantir que suas contribuições sejam bem-sucedidas.

## Requisitos
### Para começar, você precisará de:

#### - Python (versão 3.12)
#### - Django (instalado automaticamente com as dependências do projeto)
#### - Outros pacotes listados no requirements.txt

## Configuração do Ambiente

### Clone o repositório: 
### Clone o repositório FitPlan para o seu ambiente local executando:

#### - git clone https://github.com/caiofoonseca/FitPlan.git

### Ative o ambiente virtual:

#### - venv/Scripts/activate

## Instale as dependências: 
### Com o ambiente virtual já ativado, instale todas as dependências necessárias usando:

#### - pip install -r requirements.txt

## Configure o banco de dados: 
### Aplique as migrações para configurar o banco de dados inicial:

#### - python manage.py migrate

### - python manage.py makemigrations

## Execute o servidor local: 
### Inicie o servidor de desenvolvimento do Django para verificar se o ambiente está funcionando corretamente:

#### - python manage.py runserver

#### - Agora, você deve ser capaz de acessar o projeto em http://127.0.0.1:8000.

## Executando Testes
### Para executar os testes, você deve instalar o Selenium:

#### - pip install selenium

### E depois executar os testes:

#### - python manage.py test
