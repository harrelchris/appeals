# Appeals

## Requirements

-   [Python](https://www.python.org/)
-   [Node.js](https://nodejs.org/en)
-   [Docker Desktop](https://www.docker.com/products/docker-desktop/)

## Development

### Initialize

```shell
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
cp example.env .env
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser --noinput --username user --email user@email.com
```

### Lint

```shell
ruff format
ruff check --fix
```

### Run

```shell
python manage.py runserver
```

## Docker

### Build image

```shell
docker build -t app .
```

### Run container

```shell
docker run --detach --publish 8080:8000 --name app --env-file ./.env app
```

### Execute command

```shell
docker exec -it app [your command here]
```

### Access shell

```shell
docker exec -it app bash
```

### Tear down

```shell
docker stop app
docker rm app
docker rmi app
```

## Compose

### Start

```shell
docker compose up -d
```

### Migrate

```shell
docker exec -it django python manage.py migrate
```

### Stop

```shell
docker compose down
```

## Deployment

### Clone Repository

-   ssh into EC2

```shell
ssh -i {ssh_key} {ec2_user}@{ec2_ip}
```

-   Install Git

```shell
sudo dnf install git
```

-   Setup git configurations to allow repo access

-   Clone repository

```shell
git clone https://gitlab.com/lonecypressai_admin/lcai_base_web_application.git}
```

-   Run infra and init scripts

```shell
cd lcai_base_web_application
./scripts/infra.sh
./scripts/init.sh
```

-   Use docker-compose to launch application

```shell
 sudo docker-compose up -d
```
