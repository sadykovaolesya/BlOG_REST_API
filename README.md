# BlOG_REST_API
Blog API with Django Rest Framewor, Postgresql, Redis

## Postgresql and Redis in Docker

### Project Settings

#### Create a virtual environment:

```bash
python -m venv env
```

Enter the virtual environment:
```bash
source env/bin/activate
```

#### Create a `.env` file at the root of the repository:

```bash
cp .env.example
```
Make adjustments to the environment variables as needed.

#### Install requirements

```bash
pip install -r requirements.txt
```

#### Building images and running containers

At the root of the repository, run the command:

```bash
docker-compose up --build
```

#### Applying migrations:

```bash
python manage.py migrate
```




