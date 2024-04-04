

# Django App Docker Base <img src='https://img.shields.io/badge/license-MIT-blue'> <img src='https://img.shields.io/badge/python-3.12.2-blue?logo=python'> 

Este repositório serve como uma base para a construção de aplicações Django em contêineres Docker. Ele fornece uma estrutura inicial e configuração básica para você começar a desenvolver seu aplicativo Django em um ambiente de contêiner.

## 1. Pré-requisitos

Certifique-se de ter o Docker instalado em sua máquina antes de prosseguir. Você pode encontrar instruções de instalação no site oficial do Docker: [Docker Installation Guide](https://docs.docker.com/get-docker/).

## 2. Como usar este repositório

1. Clone este repositório para o seu ambiente de desenvolvimento local:

```bash
git clone https://github.com/caiython/djangoapp-docker-base.git
```

2. No diretório `dotenv_files`, renomeie o arquivo `.env-example` para `.env`.

3. Abra o arquivo renomeado `.env` com um editor de texto e edite as variáveis de ambiente para corresponder ao seu.

4. Dentro da raíz do repositório, execute o comando para construir o contêiner Docker:

```bash
docker compose up --build
```

5. Teste a aplicação acessando o endereço `http://127.0.0.1:8000` ou `http://localhost:8000` no seu navegador. Se tudo ocorreu bem, a página deverá exibir a mensagem `Page not found`.

6. Se você chegou até aqui, basta começar a desenvolver a sua própria aplicação.

## 3. Estrutura do Projeto

A estrutura do projeto é a seguinte:

```
djangoapp-docker-base/
│
├── .dockerignore
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── README.md
├── .vscode/
│   └── settings.json
├── djangoapp/
│   ├── manage.py
│   ├── requirements.txt
│   └── project/
│       ├── __init__.py
│       ├── asgi.py
│       ├── settings.py
│       ├── urls.py
│       └── wsgi.py
├── dotenv_files/
│   └── .env-example
└── scripts/
    └── commands.sh
```

## 4. Comandos Úteis
Aqui estão alguns comandos úteis que você pode usar durante o desenvolvimento do seu aplicativo Django dentro do contêiner Docker.

### Executar o Servidor de Desenvolvimento
```bash
docker-compose up
```
Este comando inicia o servidor de desenvolvimento e expõe o aplicativo.

### Criar App Django
```bash
docker-compose run djangoapp python manage.py startapp meu_app
```
Este comando cria um app no seu projeto com o nome `meu_app`.

### Executar Migrações do Django
```bash
docker-compose run djangoapp python manage.py migrate
```
Este comando executa as migrações do Django no banco de dados.

### Criar Superusuário
```bash
docker-compose run djangoapp python manage.py createsuperuser
```
Este comando cria um superusuário para acessar o painel de administração do Django.

### Atualizar Dependências
```bash
docker-compose run djangoapp pip install -r requirements.txt
```
Este comando atualiza as dependências Python do seu aplicativo com base no arquivo `requirements.txt`.

### Acessar o Shell
```bash
docker-compose run djangoapp python manage.py shell
```
Este comando abre o shell Python interativo do Django para interagir com o seu aplicativo.

## 5. Contribuições

Se você encontrar problemas ou tiver sugestões de melhorias, sinta-se à vontade para abrir uma issue neste repositório. Estarei feliz em receber contribuições!

## 6. Agradecimentos Especiais

- Roberto Júnior (@betobraga)
- Fábio Solidade

Obrigado pelo apoio durante o desenvolvimento do projeto. Vocês são feras!

## 7. Baseado no Conteúdo de Otávio Miranda

Este repositório foi construído com base no conteúdo disponibilizado pelo Otávio Miranda no vídeo [Docker com Django, PostgreSQL e Compose para seu ambiente de desenvolvimento Python](https://docs.docker.com/get-docker/).

## 8. Licença

Este projeto está licenciado sob a [MIT License](https://opensource.org/license/mit).