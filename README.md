# <img src="https://raw.githubusercontent.com/caiython/achedom/dev/djangoapp/app/static/base/achedom.ico" width="20px" style="margin-right: 5px;"> Achedom <a href="https://opensource.org/license/mit"><img src='https://img.shields.io/badge/license-MIT-blue'></a><a href="https://www.docker.com//"> <img src='https://img.shields.io/badge/docker-26.1.3-blue?logo=docker'></a><br>

Achedom is an sophisticated open-source web application designed to streamline communication between DeskManager and WhatsApp. The project leverages cutting-edge technologies to simplify implementation and ensure scalable development.

## 1. Requirements

To run Achedom you'll need to have Docker installed on your machine. You can find installation instructions on the official Docker website: [Docker Installation Guide](https://docs.docker.com/get-docker/).

## 2. How to Use

1. Clone this repository to your environment:

```bash
git clone https://github.com/caiython/achedom.git
```

2. In the `dotenv_files` directory, rename the file `.env-example` to `.env`.

3. Open the renamed `.env` file with a text editor and edit the environment variables.

4. Within the root of the repository, run the command to build the Docker container:

```bash
docker compose up --build
```

5. Test the application by accessing the address `http://127.0.0.1:80` ir `http://localhost:80` in your browser.


> *If any errors occur, you can check the section **5. Knwon Issues***

## 3. Userful Commands
Here are some useful commands you can use.

### Running the Application
```bash
docker-compose up
```
This command starts the application.

### Create Superuser
```bash
docker-compose run djangoapp python manage.py createsuperuser
```
This command creates a superuser to access the Django admin panel.

### Update Dependencies
```bash
docker-compose run djangoapp pip install -r requirements.txt
```
This command updates the Python dependencies of your application based on the `requirements.txt` file.

### Access the Shell
```bash
docker-compose run djangoapp python manage.py shell
```
This command opens the Django interactive Python shell to interact with your application.

## 4. Contributions

If you encounter any issues or have suggestions for improvements, feel free to open an issue in this repository. I will be happy to receive contributions!

## 5. Licença

Este projeto está licenciado sob a [MIT License](https://opensource.org/license/mit).